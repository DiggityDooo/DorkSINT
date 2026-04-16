# DorkSINT Terminal-Only Plan

## Summary
Build DorkSINT as a fully terminal-based Google dork generation tool with no webapp work at all. The plan keeps the current CLI workflow as the core experience, adds a terminal catalog browser, and uses `https://github.com/mitocondria40/OSINT-dork-tool.git` as the external reference for catalog structure and dork taxonomy, not as a frontend dependency.

## Implementation Changes
- Keep everything in the existing Python CLI and shell wrappers.
- Add or keep two terminal-first modes:
  - classic template generation
  - catalog browsing and catalog-id execution
- Make the catalog a local data source loaded from JSON, derived from the referenced GitHub repo’s dork definitions and organized into DorkSINT categories.
- Preserve the `sec` default behavior and gate `media` / FILE_HUNTER entries behind an explicit opt-in flag.
- Improve CLI ergonomics:
  - clear flag precedence and conflict handling
  - predictable exit codes
  - concise error messages for bad IDs, invalid domains, and empty selections
- Keep the console UI text-only:
  - boxed output for previews
  - numbered menus
  - browser-open prompt as an optional terminal action, not a web interface
- Preserve the Windows launcher behavior and make output encoding safe in interactive terminals.
- Update docs to describe terminal usage only and explicitly state that there is no webapp in scope.

## Test Plan
- Add tests for:
  - catalog loading with `sec` only vs opt-in `media`
  - catalog ID lookup
  - query composition rules for `sec` and `media`
  - menu/catalog flag precedence and conflict cases
  - terminal output helpers and fallback behavior
- Run the full pytest suite locally.
- Smoke-test the CLI entry points on Windows wrappers:
  - `dorkgen.cmd`
  - `dorkgen.ps1`
- Validate one classic flow and one catalog flow end-to-end from the terminal.

## Assumptions
- The repository to modify is the current DorkSINT CLI repo, not the external GitHub project itself.
- `https://github.com/mitocondria40/OSINT-dork-tool.git` is a reference source for catalog content and structure, but the delivered tool remains terminal-only.
- No webapp, static site, or browser-based UI will be added.
- If any future enhancement would require a browser UI, it is out of scope unless the scope changes later.
