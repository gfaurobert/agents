#!/usr/bin/env python3
"""Run validate_cv_schema + validate_cv_layout on cv-tailored.json via cv-workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cv_workflow_client import (
    CvWorkflowError,
    McpSseClient,
    load_cv_json,
    load_cv_workflow_config,
    validate_layout,
    validate_schema,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--application-dir", type=Path, required=True)
    parser.add_argument("--lang", choices=("en", "de", "fr"), default="en")
    parser.add_argument("--mcp-config", type=Path)
    args = parser.parse_args()

    app_dir = args.application_dir.expanduser().resolve()
    data = load_cv_json(app_dir / "cv-tailored.json")

    try:
        config = load_cv_workflow_config(args.mcp_config)
        with McpSseClient(config) as client:
            validate_schema(client, data)
            print("Schema: valid")
            print(validate_layout(client, data, args.lang))
    except CvWorkflowError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
