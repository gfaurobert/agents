#!/usr/bin/env python3
"""Validate cv-tailored.json and download the CV PDF from cv-workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cv_workflow_client import CvWorkflowError, request_and_download_cv_pdf


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--application-dir",
        type=Path,
        required=True,
        help="Folder containing cv-tailored.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output PDF path (default: <application-dir>/Gregor_Faurobert_CV.pdf)",
    )
    parser.add_argument("--lang", choices=("en", "de", "fr"), default="en")
    parser.add_argument(
        "--skip-layout",
        action="store_true",
        help="Skip validate_cv_layout (not recommended)",
    )
    parser.add_argument(
        "--mcp-config",
        type=Path,
        help="Path to mcp.json (default: ~/.cursor/mcp.json)",
    )
    args = parser.parse_args()

    app_dir = args.application_dir.expanduser().resolve()
    dest = args.output.expanduser().resolve() if args.output else app_dir / "Gregor_Faurobert_CV.pdf"

    try:
        request_and_download_cv_pdf(
            app_dir,
            dest,
            lang=args.lang,
            skip_layout=args.skip_layout,
            config_path=args.mcp_config,
        )
    except CvWorkflowError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
