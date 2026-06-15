#!/usr/bin/env python3
"""Render cover-letter.md into HTML/PDF using the skill HTML template."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_ROOT / "templates" / "cover-letter.template.html"

SALUTATION_RE = re.compile(
    r"^(Dear\b|Sehr geehrte|Sehr geehrtes|Guten Tag|Madame,|Monsieur,|Bonjour\b)",
    re.IGNORECASE,
)
CLOSING_RE = re.compile(
    r"^(Sincerely,?|Mit freundlichen Grüßen,?|Cordialement,?|Best regards,?|Kind regards,?)\s*$",
    re.IGNORECASE,
)
SUBJECT_RE = re.compile(r"^\*\*(.+)\*\*\s*$")
DATE_LINE_RE = re.compile(
    r"^(\d{1,2}[./]\s*\w+\s+\d{4}|\d{1,2}\s+\w+\s+\d{4}|\d{4}-\d{2}-\d{2}).*$",
    re.IGNORECASE,
)

MONTHS_EN = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
MONTHS_DE = (
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
)
MONTHS_FR = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)

DEFAULTS_BY_LANG = {
    "en": {
        "salutation": "Dear Hiring Team,",
        "closing": "Sincerely,",
    },
    "de": {
        "salutation": "Sehr geehrte Damen und Herren,",
        "closing": "Mit freundlichen Grüßen,",
        "subject_prefix": "Betreff: ",
    },
    "fr": {
        "salutation": "Madame, Monsieur,",
        "closing": "Cordialement,",
        "subject_prefix": "Objet : ",
    },
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n", 1)
    if len(parts) < 2:
        return {}, text
    rest = parts[1]
    end = rest.find("\n---")
    if end == -1:
        return {}, text
    block = rest[:end]
    body = rest[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body


def format_date(value: str | None, lang: str) -> str:
    if value and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        return value.strip()

    if value:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            parsed = date.today()
    else:
        parsed = date.today()

    lang = lang.lower()
    if lang == "de":
        return f"{parsed.day}. {MONTHS_DE[parsed.month - 1]} {parsed.year}"
    if lang == "fr":
        return f"{parsed.day} {MONTHS_FR[parsed.month - 1]} {parsed.year}"
    return f"{parsed.day} {MONTHS_EN[parsed.month - 1]} {parsed.year}"


def load_cv(cv_path: Path | None) -> dict[str, Any]:
    if not cv_path or not cv_path.is_file():
        return {}
    return json.loads(cv_path.read_text(encoding="utf-8"))


def sender_from_cv(cv: dict[str, Any]) -> tuple[str, str]:
    basic = cv.get("basic", {})
    contact = cv.get("contact", {})
    name = basic.get("name", "").strip()
    bits = [
        contact.get("location", "").strip(),
        contact.get("email", "").strip(),
        contact.get("phone", "").strip(),
        contact.get("website", "").strip(),
    ]
    bits = [b for b in bits if b]
    separator = " · " if any("@" in b or b.startswith("+") for b in bits[1:]) else " | "
    if len(bits) >= 2 and "@" in bits[1]:
        separator = " · "
    contact_line = separator.join(bits)
    return name, contact_line


def inline_markdown(text: str) -> str:
    escaped = html.escape(text.strip())
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def paragraphs_to_html(block: str) -> str:
    chunks = [p.strip() for p in re.split(r"\n\s*\n", block.strip()) if p.strip()]
    return "".join(f"<p>{inline_markdown(p)}</p>" for p in chunks)


def fields_from_meta(meta: dict[str, str], body: str, cv: dict[str, Any]) -> dict[str, str]:
    name, contact = sender_from_cv(cv)
    name = meta.get("name", name)
    contact = meta.get("contact", contact)
    lang = meta.get("lang", "en").lower()
    defaults = DEFAULTS_BY_LANG.get(lang, DEFAULTS_BY_LANG["en"])

    address_html = ""
    company_address = meta.get("company_address", "")
    if company_address:
        for part in company_address.splitlines():
            part = part.strip()
            if part:
                address_html += f"<p>{html.escape(part)}</p>"

    return {
        "name": name,
        "contact": contact,
        "date": meta.get("date", ""),
        "company": meta.get("company", ""),
        "recipient_extra": address_html,
        "subject": meta.get("subject", ""),
        "salutation": meta.get("salutation", defaults["salutation"]),
        "closing": meta.get("closing", defaults["closing"]),
        "signature": meta.get("signature", name),
        "body": body.strip(),
        "lang": lang,
    }


def parse_legacy_markdown(body: str, meta: dict[str, str], cv: dict[str, Any]) -> dict[str, str]:
    lines = [ln.rstrip() for ln in body.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)

    name = meta.get("name", "")
    contact_line = meta.get("contact", "")
    letter_date = meta.get("date", "")
    company = meta.get("company", "")
    company_address = meta.get("company_address", "")
    subject = meta.get("subject", "")
    salutation = meta.get("salutation", "")
    closing = meta.get("closing", "")
    signature = meta.get("signature", "")

    idx = 0
    if not name and lines:
        name = lines[idx].lstrip("# ").strip()
        idx += 1

    header_lines: list[str] = []
    while idx < len(lines) and lines[idx].strip():
        header_lines.append(lines[idx].strip())
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    if not contact_line and header_lines:
        contact_line = " · ".join(header_lines)
        header_lines = []

    if not letter_date and header_lines and DATE_LINE_RE.match(header_lines[0]):
        letter_date = header_lines[0]
        header_lines = header_lines[1:]

    body_lines = lines[idx:]
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    salutation_idx = None
    for i, line in enumerate(body_lines):
        if SALUTATION_RE.match(line.strip()):
            salutation_idx = i
            if not salutation:
                salutation = line.strip()
            break

    if salutation_idx is not None:
        middle_lines = body_lines[:salutation_idx]
        body_lines = body_lines[salutation_idx + 1 :]
    else:
        middle_lines = []

    recipient_source: list[str] = []
    for line in header_lines + middle_lines:
        text = line.strip()
        if not text or looks_like_contact(text):
            continue
        if not letter_date and DATE_LINE_RE.match(text):
            letter_date = text
            continue
        recipient_source.append(text)

    block_company, block_extra, block_subject = parse_recipient_block(recipient_source)
    if not company:
        company = block_company
    if not subject:
        subject = block_subject
    if block_extra and not company_address:
        company_address = block_extra

    non_empty_tail = [(i, ln.strip()) for i, ln in enumerate(body_lines) if ln.strip()]
    if len(non_empty_tail) >= 2 and CLOSING_RE.match(non_empty_tail[-2][1]):
        if not closing:
            closing = non_empty_tail[-2][1]
        if not signature:
            signature = non_empty_tail[-1][1]
        body_lines = body_lines[: non_empty_tail[-2][0]]
    elif non_empty_tail:
        if not signature:
            signature = non_empty_tail[-1][1]
        body_lines = body_lines[: non_empty_tail[-1][0]]

    body_text = "\n\n".join(p.strip() for p in re.split(r"\n\s*\n", "\n".join(body_lines)) if p.strip())

    cv_name, cv_contact = sender_from_cv(cv)
    if not name:
        name = cv_name
    if not contact_line:
        contact_line = cv_contact
    if not signature:
        signature = name or cv_name

    lang = meta.get("lang", "en").lower()
    defaults = DEFAULTS_BY_LANG.get(lang, DEFAULTS_BY_LANG["en"])
    if not salutation:
        salutation = defaults["salutation"]
    if not closing:
        closing = defaults["closing"]

    address_html = ""
    if company_address:
        for part in company_address.splitlines():
            part = part.strip()
            if part:
                address_html += f"<p>{html.escape(part)}</p>"

    return {
        "name": name,
        "contact": contact_line,
        "date": letter_date,
        "company": company,
        "recipient_extra": address_html,
        "subject": subject,
        "salutation": salutation,
        "closing": closing,
        "signature": signature,
        "body": body_text,
        "lang": lang,
    }


def build_recipient_html(company: str, extra_html: str) -> str:
    parts = []
    if company.strip():
        parts.append(f"<p>{html.escape(company.strip())}</p>")
    if extra_html:
        parts.append(extra_html)
    return "".join(parts) if parts else "<p>&nbsp;</p>"


def subject_block(subject: str, lang: str) -> str:
    subject = subject.strip()
    if not subject:
        return ""
    lang = lang.lower()
    prefix = DEFAULTS_BY_LANG.get(lang, {}).get("subject_prefix", "")
    if prefix and not subject.lower().startswith(prefix.strip().lower()[:4]):
        display = f"{prefix}{html.escape(subject)}"
    else:
        display = html.escape(subject)
    return f'<p class="subject">{display}</p>'


def render_html(fields: dict[str, str], template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    lang = fields.get("lang", "en").lower()
    letter_date = format_date(fields.get("date") or None, lang)

    replacements = {
        "{{LANG}}": html.escape(lang),
        "{{NAME}}": html.escape(fields.get("name", "")),
        "{{SENDER_NAME}}": html.escape(fields.get("name", "")),
        "{{SENDER_CONTACT}}": html.escape(fields.get("contact", "")),
        "{{RECIPIENT_HTML}}": build_recipient_html(
            fields.get("company", ""), fields.get("recipient_extra", "")
        ),
        "{{DATE}}": html.escape(letter_date),
        "{{SUBJECT_BLOCK}}": subject_block(fields.get("subject", ""), lang),
        "{{SALUTATION}}": html.escape(fields.get("salutation", "")),
        "{{BODY_HTML}}": paragraphs_to_html(fields.get("body", "")),
        "{{CLOSING}}": html.escape(fields.get("closing", "")),
        "{{SIGNATURE}}": html.escape(fields.get("signature", "")),
    }
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def looks_like_contact(text: str) -> bool:
    return "@" in text or re.search(r"\+\d{6,}", text) is not None


def parse_recipient_block(lines: list[str]) -> tuple[str, str, str]:
    company_parts: list[str] = []
    subject = ""

    for line in lines:
        text = line.strip()
        if not text:
            continue
        bold = SUBJECT_RE.match(text)
        if bold:
            inner = bold.group(1).strip()
            if re.match(r"^(Re:|Bewerbung|Application|Objet\s*:)", inner, re.IGNORECASE):
                subject = inner
            else:
                company_parts.append(inner)
            continue
        if re.match(r"^(Re:|Bewerbung|Application|Objet\s*:)", text, re.IGNORECASE):
            subject = text
            continue
        company_parts.append(text.lstrip("# ").strip())

    company = company_parts[0] if company_parts else ""
    extra = "\n".join(company_parts[1:]) if len(company_parts) > 1 else ""
    return company, extra, subject


def find_chromium() -> str | None:
    for name in (
        "chromium",
        "chromium-browser",
        "google-chrome-stable",
        "google-chrome",
        "chrome",
    ):
        path = shutil.which(name)
        if path:
            return path
    for candidate in (
        "/usr/bin/chromium",
        "/usr/bin/google-chrome-stable",
        "/opt/google/chrome/google-chrome",
    ):
        if Path(candidate).is_file():
            return candidate
    return None


def print_pdf_chromium(chromium: str, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chromium,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        str(html_path.resolve()),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def print_pdf_weasyprint(html_path: Path, pdf_path: Path) -> None:
    from weasyprint import HTML

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(html_path.resolve())).write_pdf(str(pdf_path.resolve()))


def print_pdf_wkhtmltopdf(wkhtml: str, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [wkhtml, "--enable-local-file-access", str(html_path.resolve()), str(pdf_path.resolve())],
        check=True,
        capture_output=True,
        text=True,
    )


def write_pdf(html_path: Path, pdf_path: Path) -> str:
    """Return the backend name used, or raise RuntimeError if none worked."""
    chromium = find_chromium()
    if chromium:
        print_pdf_chromium(chromium, html_path, pdf_path)
        return "chromium"

    try:
        print_pdf_weasyprint(html_path, pdf_path)
        return "weasyprint"
    except ImportError:
        pass

    wkhtml = shutil.which("wkhtmltopdf")
    if wkhtml:
        print_pdf_wkhtmltopdf(wkhtml, html_path, pdf_path)
        return "wkhtmltopdf"

    raise RuntimeError(
        "No PDF backend available. Install one of: chromium, weasyprint "
        "(pip install weasyprint), or wkhtmltopdf."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--application-dir",
        type=Path,
        help="Folder with cover-letter.md and optional cv-tailored.json",
    )
    parser.add_argument("--md", type=Path, help="Path to cover-letter.md")
    parser.add_argument("--cv", type=Path, help="Path to cv-tailored.json (contact fallback)")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--lang", choices=("en", "de", "fr"), help="Override letter language")
    parser.add_argument("--html", type=Path, help="Output HTML path")
    parser.add_argument("--pdf", action="store_true", help="Also write cover-letter.pdf")
    parser.add_argument("--pdf-path", type=Path, help="PDF output path")
    args = parser.parse_args()

    app_dir = args.application_dir
    md_path = args.md or (app_dir / "cover-letter.md" if app_dir else None)
    if not md_path or not md_path.is_file():
        parser.error("cover-letter.md not found (use --md or --application-dir)")

    cv_path = args.cv or (app_dir / "cv-tailored.json" if app_dir else None)
    cv = load_cv(cv_path)

    raw = md_path.read_text(encoding="utf-8")
    has_frontmatter = raw.startswith("---")
    meta, body = parse_frontmatter(raw)
    if args.lang:
        meta["lang"] = args.lang

    if has_frontmatter:
        fields = fields_from_meta(meta, body, cv)
    else:
        fields = parse_legacy_markdown(raw, meta, cv)
    if args.lang:
        fields["lang"] = args.lang

    if not fields.get("name"):
        fields["name"], fields["contact"] = sender_from_cv(cv)

    html_out = args.html or (app_dir / "cover-letter.html" if app_dir else md_path.with_suffix(".html"))
    pdf_out = args.pdf_path or (app_dir / "cover-letter.pdf" if app_dir else md_path.with_suffix(".pdf"))

    if not args.template.is_file():
        print(f"Template missing: {args.template}", file=sys.stderr)
        return 1

    rendered = render_html(fields, args.template)
    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(rendered, encoding="utf-8")
    print(f"Wrote {html_out}")

    if args.pdf:
        try:
            backend = write_pdf(html_out, pdf_out)
            print(f"Wrote {pdf_out} ({backend})")
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            print("HTML written but cover-letter.pdf is missing.", file=sys.stderr)
            return 2
        if not pdf_out.is_file() or pdf_out.stat().st_size == 0:
            print(f"PDF generation failed: {pdf_out}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
