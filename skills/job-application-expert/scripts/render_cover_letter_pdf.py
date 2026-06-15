#!/usr/bin/env python3
"""Render cover-letter.md to cover-letter.html and cover-letter.pdf."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RENDER_SCRIPT = SCRIPT_DIR / "render_cover_letter.py"
VENV_PYTHON = SKILL_ROOT / ".venv" / "bin" / "python3"


def python_for_render() -> str:
    if VENV_PYTHON.is_file():
        return str(VENV_PYTHON)
    return sys.executable


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--application-dir",
        type=Path,
        required=True,
        help="Folder with cover-letter.md and optional cv-tailored.json",
    )
    parser.add_argument("--lang", choices=("en", "de", "fr"))
    args = parser.parse_args()

    app_dir = args.application_dir.expanduser().resolve()
    pdf_path = app_dir / "cover-letter.pdf"
    cmd = [
        python_for_render(),
        str(RENDER_SCRIPT),
        "--application-dir",
        str(app_dir),
        "--pdf",
    ]
    if args.lang:
        cmd.extend(["--lang", args.lang])

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        return result.returncode
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        print(f"cover-letter.pdf missing or empty: {pdf_path}", file=sys.stderr)
        return 2
    print(f"Wrote {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
