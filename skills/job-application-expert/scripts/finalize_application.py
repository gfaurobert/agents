#!/usr/bin/env python3
"""Validate CV layout, download CV PDF, and render cover-letter.pdf for one application folder."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--application-dir", type=Path, required=True)
    parser.add_argument(
        "--cv-filename",
        default="Gregor_Faurobert_CV.pdf",
        help="CV PDF filename inside application dir",
    )
    parser.add_argument("--lang", choices=("en", "de", "fr"), default="en")
    parser.add_argument("--mcp-config", type=Path)
    args = parser.parse_args()

    app_dir = args.application_dir.expanduser().resolve()
    py = sys.executable

    cv_dest = app_dir / args.cv_filename
    steps = [
        [
            py,
            str(SCRIPT_DIR / "download_cv_pdf.py"),
            "--application-dir",
            str(app_dir),
            "--lang",
            args.lang,
            "--output",
            str(cv_dest),
        ],
        [
            py,
            str(SCRIPT_DIR / "render_cover_letter_pdf.py"),
            "--application-dir",
            str(app_dir),
            "--lang",
            args.lang,
        ],
    ]
    if args.mcp_config:
        steps[0].extend(["--mcp-config", str(args.mcp_config)])

    for cmd in steps:
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return result.returncode

    cv_pdf = app_dir / args.cv_filename
    cover_pdf = app_dir / "cover-letter.pdf"
    print(f"Done: {cv_pdf}")
    print(f"Done: {cover_pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
