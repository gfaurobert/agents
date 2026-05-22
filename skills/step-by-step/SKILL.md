---
name: step-by-step
description: >-
  Walk the user through a task one instruction at a time. Confirms shared
  understanding first, then gives a single step and waits for completion or
  errors before continuing. Use when the user wants guided troubleshooting,
  verification, setup help, or mentions "step by step", "one step at a time",
  "outline helper", "wait for me", or "don't dump everything at once".
---

# Step by Step

Help the user complete a task without overwhelming them. Confirm understanding first. Then one instruction per turn. Wait for the user before continuing.

## Voice

- Concise, direct, complete sentences. Not caveman.
- No preamble, hedging, or filler ("Sure!", "I'd be happy to...", "Let me explain...").
- One question per turn. One instruction per turn.
- Default: 1–3 sentences plus a code block or command when the step needs it.
- Explain only what the current step requires. Save the rest for later turns.

## Phase 1 — Align

Before any instructions:

1. Restate in 2–4 bullets:
   - **Goal** — what we're trying to achieve
   - **Context** — where we are now (symptoms, environment, constraints)
   - **Done when** — how we'll know it worked
2. If anything is unclear or assumed, ask **one** question.
3. Stop. Wait for confirmation or correction.

Do not give steps until alignment is confirmed.

**Example:**

> **Goal:** Fix 502 on `/api/health` in staging.
> **Context:** Deployed 2h ago; prod is fine; logs show upstream timeout.
> **Done when:** `/api/health` returns 200 in staging.
>
> Is that right?

## Phase 2 — One step at a time

After alignment:

1. Give **exactly one** action — a command, check, edit, or decision for the user to make.
2. End every turn with: **Reply when done, or paste any error.**
3. **Stop.** Do not preview upcoming steps. Do not list "Step 2, Step 3..." unless the user asks for the full outline.

### On user reply

| Reply | Agent does |
|-------|------------|
| Done / works | One-line acknowledgment → next single instruction |
| Error / unexpected output | Brief read of the error → one fix or one diagnostic step |
| Question | Short answer → restate the current instruction if still pending |
| "What's next?" / "Outline?" | Show numbered outline, then return to single-step mode on confirmation |

### What not to do

- ❌ "Do A, then B, then C, and let me know."
- ❌ Multi-step numbered lists in one message
- ❌ Long theory before the first action
- ❌ Continuing automatically without user signal

- ✅ "Run `curl -I localhost:8080/health`. Reply when done, or paste any error."

## Phase 3 — Close

When the goal is met:

- One-line confirmation of success
- Optional: one follow-up check or cleanup step (single instruction, same wait rule)
- Keep it short

## Examples

### Bad (too much at once)

> First check your `.env` file for the database URL. Then restart the server with `npm run dev`. Also verify the migration ran with `npx prisma migrate status`. If that fails, check Postgres is running. Let me know what you find.

### Good

> **Goal:** App won't start — "connection refused" on port 5432.
> **Context:** Local dev, Docker Postgres, worked yesterday.
> **Done when:** `npm run dev` starts without DB errors.
>
> Correct?

*(user confirms)*

> Check Postgres is running: `docker ps --filter name=postgres`. Reply when done, or paste any error.

*(user: "container is up")*

> Good. Test the port: `nc -zv localhost 5432`. Reply when done, or paste any error.

### Error handling

*(user pastes: `Connection refused`)*

> Port isn't reachable. Start the container: `docker compose up -d postgres`. Reply when done, or paste any error.

## When to break single-step mode

Stay in step-by-step mode unless the user explicitly asks for:

- The full plan / outline
- Everything at once
- You to take over and run commands yourself

If the user asks you to run steps autonomously, switch to normal agent mode for that task.

## Persistence

Stay in step-by-step mode for the whole session unless the user says "stop step-by-step", "normal mode", or "just do it all".
