#!/usr/bin/env python3
"""Minimal MCP SSE client for the cv-workflow server (stdlib only)."""

from __future__ import annotations

import json
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_MCP_CONFIG = Path.home() / ".cursor" / "mcp.json"


@dataclass(frozen=True)
class CvWorkflowConfig:
    base_url: str
    sse_url: str
    authorization: str


class CvWorkflowError(RuntimeError):
    pass


def load_cv_workflow_config(config_path: Path | None = None) -> CvWorkflowConfig:
    path = config_path or DEFAULT_MCP_CONFIG
    if not path.is_file():
        raise CvWorkflowError(f"MCP config not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    servers = raw.get("mcpServers") or raw.get("mcp_servers") or {}
    entry = servers.get("cv-workflow")
    if not entry:
        raise CvWorkflowError("cv-workflow server missing from MCP config")

    sse_url = entry.get("url") or entry.get("sse_url")
    if not sse_url:
        raise CvWorkflowError("cv-workflow url missing from MCP config")

    headers = entry.get("headers") or {}
    auth = headers.get("Authorization") or headers.get("authorization") or ""
    if not auth.startswith("Bearer "):
        raise CvWorkflowError("cv-workflow Authorization header must be Bearer <token>")

    parsed = urllib.parse.urlparse(sse_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    return CvWorkflowConfig(base_url=base_url, sse_url=sse_url, authorization=auth)


class McpSseClient:
    def __init__(self, config: CvWorkflowConfig, timeout_s: float = 120.0) -> None:
        self._config = config
        self._timeout_s = timeout_s
        self._session_url: str | None = None
        self._responses: dict[int, dict[str, Any]] = {}
        self._response_event = threading.Event()
        self._pending_id: int | None = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._next_id = 1
        self._lock = threading.Lock()

    def __enter__(self) -> McpSseClient:
        self.connect()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    @property
    def _headers(self) -> dict[str, str]:
        return {"Authorization": self._config.authorization}

    def connect(self) -> None:
        self._thread = threading.Thread(target=self._sse_loop, daemon=True)
        self._thread.start()

        deadline = time.time() + self._timeout_s
        while self._session_url is None and time.time() < deadline:
            if self._stop.is_set():
                raise CvWorkflowError("SSE connection failed before session endpoint")
            time.sleep(0.05)
        if not self._session_url:
            raise CvWorkflowError("Timed out waiting for MCP session endpoint")

        init_id = self._send(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "job-application-expert", "version": "1.0.0"},
            },
        )
        init_result = self._wait_for(init_id)
        if init_result.get("error"):
            raise CvWorkflowError(f"initialize failed: {init_result['error']}")
        self._notify("notifications/initialized", {})

    def close(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        req_id = self._send("tools/call", {"name": name, "arguments": arguments})
        result = self._wait_for(req_id)
        if result.get("error"):
            err = result["error"]
            message = err.get("message") if isinstance(err, dict) else str(err)
            raise CvWorkflowError(message or f"tools/call {name} failed")

        payload = result.get("result") or {}
        if payload.get("isError"):
            content = payload.get("content") or []
            text = content[0].get("text") if content else f"{name} failed"
            raise CvWorkflowError(text)

        content = payload.get("content") or []
        if not content:
            return ""
        return content[0].get("text", "")

    def _sse_loop(self) -> None:
        req = urllib.request.Request(self._config.sse_url, headers=self._headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self._timeout_s) as resp:
                event: str | None = None
                data_lines: list[str] = []
                for raw in resp:
                    if self._stop.is_set():
                        break
                    line = raw.decode("utf-8").rstrip("\r\n")
                    if line.startswith("event:"):
                        event = line[6:].strip()
                    elif line.startswith("data:"):
                        data_lines.append(line[5:].strip())
                    elif line == "":
                        if data_lines:
                            self._handle_sse_event(event, "\n".join(data_lines))
                        event = None
                        data_lines = []
        except Exception as exc:
            if not self._stop.is_set():
                self._stop.set()
                raise CvWorkflowError(f"SSE stream error: {exc}") from exc

    def _handle_sse_event(self, event: str | None, data: str) -> None:
        if event == "endpoint":
            endpoint = data
            if endpoint.startswith("/"):
                endpoint = urllib.parse.urljoin(self._config.base_url + "/", endpoint.lstrip("/"))
            self._session_url = endpoint
            return

        if event != "message":
            return

        try:
            message = json.loads(data)
        except json.JSONDecodeError:
            return

        if "id" not in message:
            return

        with self._lock:
            self._responses[int(message["id"])] = message
            if self._pending_id == int(message["id"]):
                self._response_event.set()

    def _send(self, method: str, params: dict[str, Any] | None = None) -> int:
        if not self._session_url:
            raise CvWorkflowError("MCP session not ready")

        with self._lock:
            req_id = self._next_id
            self._next_id += 1
            self._pending_id = req_id
            self._response_event.clear()

        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params

        body = json.dumps(payload).encode("utf-8")
        headers = {**self._headers, "Content-Type": "application/json"}
        req = urllib.request.Request(self._session_url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self._timeout_s):
                pass
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise CvWorkflowError(f"POST {method} failed ({exc.code}): {detail}") from exc

        return req_id

    def _notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        if not self._session_url:
            raise CvWorkflowError("MCP session not ready")

        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params

        body = json.dumps(payload).encode("utf-8")
        headers = {**self._headers, "Content-Type": "application/json"}
        req = urllib.request.Request(self._session_url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=self._timeout_s):
            pass

    def _wait_for(self, req_id: int) -> dict[str, Any]:
        deadline = time.time() + self._timeout_s
        while time.time() < deadline:
            with self._lock:
                if req_id in self._responses:
                    return self._responses.pop(req_id)
            if self._stop.is_set():
                break
            self._response_event.wait(timeout=0.1)
        raise CvWorkflowError(f"Timed out waiting for MCP response id={req_id}")


def parse_download_path(tool_text: str) -> str:
    match = re.search(r"URL:\s*(\S+)", tool_text)
    if not match:
        raise CvWorkflowError(f"No download URL in tool response:\n{tool_text}")
    return match.group(1)


def download_file(config: CvWorkflowConfig, url_path: str, dest: Path) -> Path:
    if url_path.startswith("http"):
        full_url = url_path
    else:
        full_url = urllib.parse.urljoin(config.base_url + "/", url_path.lstrip("/"))

    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(full_url, headers={"Authorization": config.authorization})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if not data:
        raise CvWorkflowError(f"Downloaded file is empty: {full_url}")
    dest.write_bytes(data)
    return dest


def load_cv_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise CvWorkflowError(f"CV JSON not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(client: McpSseClient, data: dict[str, Any]) -> None:
    text = client.call_tool("validate_cv_schema", {"data": data})
    if text.strip() != "valid":
        raise CvWorkflowError(text)


def validate_layout(client: McpSseClient, data: dict[str, Any], lang: str) -> str:
    text = client.call_tool("validate_cv_layout", {"data": data, "lang": lang})
    if not text.startswith("Layout OK"):
        raise CvWorkflowError(text)
    return text


def request_and_download_cv_pdf(
    application_dir: Path,
    dest: Path,
    *,
    lang: str = "en",
    skip_layout: bool = False,
    config_path: Path | None = None,
) -> Path:
    application_dir = application_dir.expanduser().resolve()
    dest = dest.expanduser().resolve()
    data = load_cv_json(application_dir / "cv-tailored.json")
    config = load_cv_workflow_config(config_path)

    with McpSseClient(config) as client:
        validate_schema(client, data)
        layout_msg = None
        if not skip_layout:
            layout_msg = validate_layout(client, data, lang)
        tool_text = client.call_tool(
            "request_cv_pdf",
            {"data": data, "lang": lang, "filename": dest.name},
        )

    download_file(config, parse_download_path(tool_text), dest)
    if layout_msg:
        print(layout_msg, file=sys.stderr)
    print(f"Wrote {dest}")
    print(tool_text)
    return dest
