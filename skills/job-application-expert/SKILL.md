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

## Output Folder Convention

**Always** create a dedicated subfolder before writing any artifact. Use this naming pattern:

```
~/job-applications/<company-name>-<role-slug>-<YYYY-MM-DD>/
```

Example: `~/job-applications/chefslist-pm-2026-05-16/`

Derive from the job description:
- `<company-name>`: lowercase, no spaces (hyphens ok)
- `<role-slug>`: short role identifier, e.g. `pm`, `sr-pm`, `head-of-product`
- `<YYYY-MM-DD>`: today's date

Create the folder at the start of Phase 6 (before writing the tailored CV JSON). All subsequent artifacts go into this folder:

| Artifact | Filename |
|----------|----------|
| CV JSON | `cv-tailored.json` |
| CV PDF | `cv-tailored.pdf` |
| Cover letter (Markdown) | `cover-letter.md` |
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

Phases 3, 4, 5, and 11 are read by the user as decision points. Always use **bullet points, minimal prose**. Less is more. No paragraphs of reasoning — the user wants to scan and decide, not read an essay.

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

1. **Strategic fit assessment** — for each of the top 2 company needs, map which parts of the CV demonstrate relevant capability. Be honest about gaps.
2. **Keyword alignment** — extract hard requirements from the job description and check CV coverage
3. **Tailoring strategy** — which CV sections to adjust, driven by needs, not keywords:
   - Rewrite the **professional summary** to position the candidate as the answer to the company's needs
   - Reorder/rephrase **experience bullet points** to surface the most relevant achievements first
   - Prioritize **skills** that directly address the identified needs
   - Add any genuinely missing keywords naturally (don't fabricate)

Present the strategy to the user for approval before proceeding.

### Phase 6 — Tailor the CV

If the target language differs from what was loaded in Phase 2, call `mcp_cv_workflow_get_full_cv` again with the correct language to get the CV in that language as a base.

**First**: create the output folder (see Output Folder Convention above).

Modify the CV JSON and save as `cv-tailored.json` in the output folder:
- Rewrite the **professional summary** to target this specific role
- Reorder and rephrase **experience bullet points** to emphasize relevant achievements
- Prioritize **skills** that match the job description
- Adjust **projects** section if relevant to the role
- Keep all factual information intact — never invent experience, titles, or dates

### Phase 7 — Validate CV Schema

Call `mcp_cv_workflow_validate_cv_schema` with the tailored CV JSON.

If validation fails, fix the issues and re-validate. Do not proceed until schema validation passes.

### Phase 8 — Write the Cover Letter

Write a cover letter as markdown text:

**Structure:**
1. **Header**: User's name, contact info, date, company name
2. **Opening paragraph**: Role being applied for, how they found it, one-sentence hook
3. **Body 1**: Why this company — show research, connect to company mission/values
4. **Body 2**: Why this role — map 2-3 specific CV achievements to job requirements
5. **Body 3**: What they'll bring — unique value proposition, cultural fit
6. **Closing**: Call to action, availability for interview, thank you

**Tone guidelines:**
- Confident but not arrogant
- Specific, not generic (reference actual job requirements)
- ~300-400 words (1 page)
- No AI clichés ("I am thrilled", "I believe I am the perfect fit")

Save the cover letter as `cover-letter.md` in the output folder.

### Phase 8b — Convert Cover Letter to PDF

Convert the cover letter markdown to PDF using Chromium headless:

1. Convert markdown to HTML using Python stdlib (regex-based — no external deps needed for simple cover letters with headers, bold, and paragraphs)
2. Write a minimal HTML wrapper with basic print-friendly CSS (Helvetica, 11pt, A4 margins)
3. Run: `chromium --headless --disable-gpu --print-to-pdf=<output-folder>/cover-letter.pdf --no-margins /tmp/cover-letter.html`

Save the resulting PDF as `cover-letter.pdf` in the output folder.

If Chromium is not available, skip this phase and note it in the final summary.

### Phase 9 — Validate Layout

Call `mcp_cv_workflow_validate_cv_layout` with the tailored CV JSON.

This checks that the CV fits within the 2-page PDF layout constraint.

If it fails:
- Trim or consolidate bullet points
- Remove less relevant entries
- Shorten the professional summary
- Re-validate until it passes

### Phase 10 — Generate PDF

Call `mcp_cv_workflow_request_cv_pdf` with the final tailored CV JSON.

Save the resulting PDF as `cv-tailored.pdf` in the output folder. Download from the server's `/downloads/` path.

### Phase 11 — Final Summary

Bullet points only:

- Path to tailored CV PDF
- Path to cover letter
- 2-3 key changes made (e.g. "reoriented summary toward B2B growth, added APAC negotiation example from off-book experience")
- Any caveats (missing evidence for a specific need, something the user should verify)

## Pitfalls

- **Never fabricate experience** — only rephrase, reorder, or re-emphasize existing content
- **Don't skip validation** — schema and layout checks catch real issues before PDF generation
- **Language consistency** — if the job is in French, output CV and cover letter in French
- **If MCP tools are unavailable**, first run `hermes mcp test cv-workflow` to check connectivity. If the test passes but tools still aren't in your function list (common after `/reload-mcp` or in sessions started before the MCP server was configured), use the raw MCP protocol fallback via `execute_code` — see the `native-mcp` skill's `references/fallback-mcp-calls.md` for the working SSE Python approach. The config is `transport: sse`, the token is in `~/.hermes/config.yaml` under `mcp_servers.cv-workflow.headers.Authorization`, and the endpoint sessions are per-call (no persistent session reuse).
