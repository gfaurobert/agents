---
name: excalidraw-conventions
description: >-
  Personal Excalidraw workflow conventions for Cursor. Use when sketching UI
  wireframes, app workflows, 3D-part diagrams, flowcharts, or when the user
  mentions excalidraw, sketch, wireframe, or diagram. Enforces sketches/
  paths, port 3456, file-backed editing, and .excalidraw export rules on top
  of excalidraw-skill.
---

# Excalidraw conventions

Read and follow `excalidraw-skill` for canvas/CLI/MCP mechanics. Apply these
overrides for every sketch in this environment.

## File-backed editing (required)

The canvas is bound to a real `.excalidraw` file. Browser edits auto-save to
disk. Do **not** treat "Sync to Backend" as the source of truth.

Workflow every time:

1. Set sketches root to `<workspace-root>/sketches` (create if missing)
2. Open or create the named sketch
3. Give the user this URL:
   `http://127.0.0.1:3456/?root=<abs-sketches-dir>&file=<name>.excalidraw`
4. Prefer MCP tools: `set_sketches_root`, `list_sketches`, `open_sketch`,
   `new_sketch`, `save_sketch`
5. Manual `export_scene` is only a fallback if no file is bound

CLI equivalents:

```bash
export PATH="/home/gregoire/.local/share/fnm/node-versions/v24.16.0/installation/bin:$PATH"
export PORT=3456 HOST=127.0.0.1 EXPRESS_SERVER_URL=http://127.0.0.1:3456
BIN=/home/gregoire/Development/mcp_excalidraw/dist/bin.js
node "$BIN" workspace /abs/path/to/sketches
node "$BIN" new-sketch ui-for-login
node "$BIN" open-sketch smoke-test.excalidraw
node "$BIN" sketches
node "$BIN" save-sketch
```

## Paths and format

- Write files only under `<workspace-root>/sketches/` (create the directory if missing)
- Use plain `.excalidraw` JSON only (never Obsidian `.excalidraw.md`)
- Never write outside the current workspace sketches folder

## Naming

- If the user gives a name (e.g. `ui-for-login`), use `sketches/<name>.excalidraw`
- If no name, generate a random slug: `sketches/sketch-<6 alphanumeric chars>.excalidraw`
- If the target file already exists, open it (import/bind) first, then edit

## Canvas

- Canvas URL is always `http://127.0.0.1:3456` (not 3000)
- Prefer deep links with `?root=` and `file=` so the picker opens the right sketch
- The in-app Sketches panel lists files under the current root; user can switch files there
- If port 3456 is busy with a healthy canvas, reuse it; otherwise report the conflict

## Finish checklist

Before saying done:

1. Ensure the sketch is open/bound (`open_sketch` / `new_sketch`)
2. Confirm the `.excalidraw` file exists on disk
3. Give the user the deep-link URL above
4. Do **not** git commit the sketch unless the user explicitly asks

## Screenshots

Drawing and file save work without a browser tab. Screenshots may require the
user to keep the canvas URL open — say so when taking screenshots.
