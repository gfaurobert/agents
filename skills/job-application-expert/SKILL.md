---
name: job-application-expert
description: "Tailor a CV and generate a cover letter + PDF for a specific job application using the cv-workflow MCP tools."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    triggers:
      - "apply to.*job"
      - "job application"
      - "tailor.*cv.*job"
      - "cover letter.*job"
      - "/job-application-expert"
---

# Job Application Expert

Guides the user through tailoring their CV and generating a cover letter + PDF for a specific job application.

**Prerequisites:** The `cv-workflow` MCP server must be configured and connected (4 tools: `get_full_cv`, `validate_cv_schema`, `validate_cv_layout`, `request_cv_pdf`).

---

## Helper Scripts (reuse every session)

Skill root: `~/.agents/skills/job-application-expert/scripts/`

| Script | Purpose |
|--------|---------|
| `validate_cv_layout.py` | `validate_cv_schema` + `validate_cv_layout` on `cv-tailored.json` |
| `download_cv_pdf.py` | Layout gate + `request_cv_pdf` + save PDF locally |
| `render_cover_letter_pdf.py` | `cover-letter.md` → `cover-letter.html` + `cover-letter.pdf` |
| `finalize_application.py` | Runs download + cover letter PDF in one step |

Auth is read from `~/.cursor/mcp.json` → `mcpServers.cv-workflow` (no manual token handling).

```bash
# Layout check only
python3 ~/.agents/skills/job-application-expert/scripts/validate_cv_layout.py \
  --application-dir ~/Nextcloud/Documents/CV/<company>-<role>-<YYYY-MM-DD>/ \
  --lang en

# CV PDF (validates layout first)
python3 ~/.agents/skills/job-application-expert/scripts/download_cv_pdf.py \
  --application-dir ~/Nextcloud/Documents/CV/<company>-<role>-<YYYY-MM-DD>/ \
  --output ~/Nextcloud/Documents/CV/<company>-<role>-<YYYY-MM-DD>/Gregor_Faurobert_PM_Company.pdf \
  --lang en

# Cover letter PDF
python3 ~/.agents/skills/job-application-expert/scripts/render_cover_letter_pdf.py \
  --application-dir ~/Nextcloud/Documents/CV/<company>-<role>-<YYYY-MM-DD>/ \
  --lang en

# Both PDFs
python3 ~/.agents/skills/job-application-expert/scripts/finalize_application.py \
  --application-dir ~/Nextcloud/Documents/CV/<company>-<role>-<YYYY-MM-DD>/ \
  --cv-filename Gregor_Faurobert_PM_Company.pdf \
  --lang en
```

**Completion gate:** `finalize_application.py` must exit 0 and both PDFs must exist and be non-empty. Prefer these scripts over hand-rolled curl/MCP calls.

---

## Output Folder Convention

**Always** create a dedicated subfolder before writing any artifact. Use this naming pattern:

```
~/Nextcloud/Documents/CV/<company-name>-<role-slug>-<YYYY-MM-DD>/
```

Example: `~/Nextcloud/Documents/CV/chefslist-pm-2026-05-16/`

Derive from the job description:
- `<company-name>`: lowercase, no spaces (hyphens ok)
- `<role-slug>`: short role identifier, e.g. `pm`, `sr-pm`, `head-of-product`
- `<YYYY-MM-DD>`: today's date

Create the folder at the start of Phase 6 (before writing the tailored CV JSON). All subsequent artifacts go into this folder:

| Artifact | Filename |
|----------|----------|
| CV JSON | `cv-tailored.json` |
| CV PDF | `Gregor_Faurobert_$role_$company.pdf` |
| Cover letter (Markdown) | `cover-letter.md` |
| Cover letter (HTML) | `cover-letter.html` |
| Cover letter (PDF) | `cover-letter.pdf` |

If the folder already exists, reuse it (don't overwrite unless the user confirms).

---

- **Conversation with the user is always in English**, regardless of what language the job description or CV is in.
- **Ask explicitly** before generating the CV and cover letter: "Should I generate the CV and cover letter in English, German, or French?" Never infer from the job description.

---

### Phase 1 — Gather Inputs

The user must provide a **full job description** (copy-paste the listing — any language is fine).

Optional inputs:
- Company research notes
- Any specific skills or experiences to emphasize

Do not ask about language yet — that comes after analysis, before generation.

### Phase 2 — Load Existing CV

Call `mcp_cv_workflow_get_full_cv`. Try `en` first. If the user's CV has versions in multiple languages, load whichever is available. Present a brief summary.

## Output Style (Critical)

Phases 3, 4, 5, and 12 are read by the user as decision points. Always use **bullet points, minimal prose**. Less is more. No paragraphs of reasoning — the user wants to scan and decide, not read an essay.

Good:
```
Top 2 needs:
• Need to unblock APAC vendor deals — VP stretched, pipeline stalled in 3 countries
• Need product-market fit validation for EU launch — they're guessing, no framework

Ideal profile: someone who's done B2B negotiations in regulated markets and run structured discovery
```

Bad (do not do this):
```
After carefully analyzing the job description, I believe the company's primary needs
revolve around their expansion into the APAC region, where they are currently facing
challenges with vendor negotiations that have resulted in stalled pipelines across
three key markets. This is exacerbated by the VP being stretched thin across multiple...
```

---

### Phase 3 — Company Needs Analysis (Strategic Framing)

Before looking at the CV at all, analyze the job description to answer:

**What are the company's top 2 needs behind this hire?**

This is not a keyword extraction exercise. Step back and think strategically:

1. **Read between the lines** — what problem is this role solving?
2. **Identify the top 2 needs** — be specific. Not "needs leadership" but "needs someone who can take over APAC vendor negotiations so the VP can focus on US expansion."
3. **Define the ideal candidate profile** — based on those 2 needs, who succeeds in the first 90 days?

Present as bullet points. User discusses and refines. This framing guides every decision that follows.

### Phase 4 — Surface Hidden Experience

**The CV is a curated snapshot, not the full story.** Ask questions one at a time, waiting for the user's reply before the next. Let the conversation breathe — don't dump a list of questions.

Example flow:
1. "For [Need 1], is there anything relevant you've done that isn't on your CV?"
2. [user replies] → "And for [Need 2]?"
3. [user replies] → "Any side projects, consulting, or adjacent domain experience worth mentioning?"

Adapt questions to the actual needs. Stop when the user has nothing more to add.

### Phase 5 — Analyze Fit & Build Strategy

Map the CV + hidden experience against the company's top 2 needs. Present as bullets:

- Strong matches (where the candidate clearly fits a need)
- Gaps or stretches (needs with weak or missing evidence)
- Tailoring strategy: 3-4 concrete changes to make (summary rewrite, reorder X, add Y from hidden experience)

Ask user to approve before touching the CV. Also ask: "Should I generate the CV and cover letter in English, German, or French?"

### Phase 6 — Tailor the CV

If the target language differs from what was loaded in Phase 2, call `mcp_cv_workflow_get_full_cv` again with the correct language to get the CV in that language as a base.

**First**: create the output folder (see Output Folder Convention above).

Modify the CV JSON and save as `cv-tailored.json` in the output folder:
- Rewrite the **professional summary** to target this specific role
- Rephrase **experience bullet points** to emphasize relevant achievements
- Prioritize **skills** that match the job description
- Adjust **projects** section if relevant to the role
- Keep all factual information intact — never invent experience, titles, or dates

**Critical — experience order:** Keep `experience.items` in **reverse chronological order** (newest first). The PDF renderer splits at `floor(n/2)` across two pages; reordering entries breaks page 2 even when layout validation reports OK. Tailor by rewriting bullets, not by moving entries.

### Phase 7 — Validate CV Schema

Call `validate_cv_schema` (MCP or `validate_cv_layout.py` which also runs schema) with the full `cv-tailored.json` object as `data`.

If validation fails, fix the issues and re-validate. Do not proceed until schema validation passes.

### Phase 8 — Validate CV Layout (mandatory gate)

Call `validate_cv_layout` with the same full `data` object and matching `lang`.

**Or run:** `validate_cv_layout.py --application-dir … --lang en`

**This must pass before any CV PDF is generated.** Do not call `request_cv_pdf` or `download_cv_pdf.py` until the result is `Layout OK` (exit 0, not `isError`).

If validation fails, follow the remediation message, then re-validate until it passes.

**Page 2 hygiene:** The tool only blocks page 1 overflow. If `page2_overflow` is high (>15mm), shorten bullets in later experience entries and sidebar text even when page 1 is OK.

### Phase 9 — Download CV PDF

**Prefer:** `download_cv_pdf.py` (runs layout validation + `request_cv_pdf` + local save).

Save as `Gregor_Faurobert_$role_$company.pdf` in the application folder. Verify the file exists and is non-empty.

### Phase 10 — Write the Cover Letter

Write letter content only. Layout/CSS handled by the skill template — do not write HTML.

**Mandatory: run the `witty-writer` skill on the letter body before saving.** Agents cannot invoke skills automatically, but you must follow both workflows in sequence:

1. **Draft** (`job-application-expert` — this phase): structure, facts, role fit, ~300–400 words. Use frontmatter + body paragraphs. No HTML.
2. **Voice pass** (`witty-writer` at `~/.agents/skills/witty-writer/SKILL.md`): read that skill fully, then rewrite **only the body paragraphs** (content after the closing `---` of frontmatter, or everything after the salutation in legacy format). Keep every fact, metric, company name, and claim from the draft; do not add new experience. Make it punchy, specific, and human — cut template phrasing and AI clichés. Preserve `lang` and formal business tone for DE/FR.
3. **Save** the witty-writer output as `cover-letter.md` in the application folder.

If the user wants to compare drafts, also save the pre–witty-writer version as `cover-letter.draft.md` (optional, only when asked).

Do not skip the witty-writer pass to save time.

**Preferred format** (`cover-letter.md` with YAML frontmatter + body paragraphs):

```markdown
---
lang: en
date: 2026-05-18
company: Example GmbH
subject: "Re: Senior Product Manager"
salutation: "Dear Hiring Team,"
closing: "Sincerely,"
signature: "Gregor Faurobert"
---

Opening paragraph...

Body paragraphs (blank line between each)...
```

- `lang`: `en`, `de`, or `fr` (same as CV/cover letter language)
- `date`: `YYYY-MM-DD` preferred; script formats for locale
- `company` / optional `company_address`: recipient block
- `subject`: optional; DE adds `Betreff:`, FR adds `Objet :`
- Omit `name` / `contact` when `cv-tailored.json` is in the same folder (filled from CV)

**Legacy format** (still supported): markdown with name, contact, date, company, bold or `Re:` subject line, salutation, paragraphs, closing, signature — same structure as past applications.

**Content structure:**
1. Opening: role, hook
2. Why this company
3. Why this role (2–3 CV proofs)
4. What you bring
5. Close: interview availability, thanks

**Tone (after witty-writer):** confident, direct, specific, ~300–400 words — see `witty-writer` skill for rhythm and anti-boilerplate rules.

Final artifact: `cover-letter.md` (post–witty-writer). Render that file in Phase 11, not the draft.

### Phase 11 — Render Cover Letter PDF (mandatory)

Do **not** hand-build HTML. Use `render_cover_letter_pdf.py` (wraps `render_cover_letter.py`).

**`cover-letter.pdf` is required.** The render script tries Chromium, then WeasyPrint, then wkhtmltopdf. One-time setup if no browser is installed:

```bash
python3 -m venv ~/.agents/skills/job-application-expert/.venv
~/.agents/skills/job-application-expert/.venv/bin/pip install weasyprint
```

`render_cover_letter_pdf.py` uses that venv automatically when present.

Do **not** finish with HTML only.

### Phase 12 — Final Summary

**Completion gate:** Both `Gregor_Faurobert_$role_$company.pdf` and `cover-letter.pdf` must exist in the application folder. `finalize_application.py` exit 0 is the preferred check.

Bullet points only:

- Path to tailored CV PDF
- Path to cover letter PDF
- Layout validation result (page1/page2 overflow)
- 2-3 key changes made
- Any caveats

## Pitfalls

- **Never fabricate experience** — only rephrase or re-emphasize; never reorder experience out of reverse chronological order
- **Don't skip layout validation** — must pass before `download_cv_pdf.py` / `request_cv_pdf`; pass full `data`, not just `lang`
- **Don't hand-download PDFs** — use `download_cv_pdf.py` instead of raw curl with tokens
- **Language consistency** — if the job is in French, output CV and cover letter in French
- **If MCP tools are unavailable in the agent**, use the helper scripts (`cv_workflow_client.py` via `download_cv_pdf.py` / `validate_cv_layout.py`) — they call the same SSE endpoint using `~/.cursor/mcp.json`.
