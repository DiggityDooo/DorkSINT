# DorkSINT

An open-source Python CLI that asks what you are trying to find, takes your target details, and generates copy-ready Google dork queries to speed up search workflow.

## About

DorkSINT is an open-source Python CLI that speeds up Google dorking by turning your search objective into structured, paste-ready queries.
It supports both interactive prompts and non-interactive flags, includes reusable query templates, and runs natively in both PowerShell and CMD.

Built for legal, authorized security research and defensive reconnaissance workflows.

**DorkSINT is entirely terminal-based.** There is no webapp, static site, or browser-based UI in scope. All interaction happens through the CLI.

## Features

- Interactive prompts for objective and target details.
- Menu-based catalog browser with prompt UI for CMD/PowerShell readability.
- Non-interactive mode for scripts/automation.
- Multiple query variants per request (title-based, URL-based, filetype-based).
- Curated catalog import from DorkSearch categories with security-first defaults.
- Basic input validation and sanitization.

## Install

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e .
```

## Usage

### Interactive mode

```bash
dorkgen --interactive
```

### Native PowerShell (no install)

```powershell
.\dorkgen.ps1 --interactive
```

If you get a script execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**PowerShell gotchas**

- Run the script and its arguments on **one line**. Do not press Enter after the script name; the flags belong to that same command.
- `".\dorkgen.ps1"` in quotes by itself only **prints text** — it does not run the script. To run: `.\dorkgen.ps1 ...` or `& .\dorkgen.ps1 ...`.
- If Windows PowerShell suggests `.\.\dorkgen.ps1`, you can ignore it and use `.\dorkgen.ps1` from the repo folder.
- Quote CSV values so commas are not split: `--filetypes "pdf,xlsx"` and `--exclude "sample,demo"`.

Example (copy as one block):

```powershell
.\dorkgen.ps1 --objective public-documents --domain contoso.com --keyword "quarterly report" --filetypes "pdf,xlsx" --exclude "sample,demo"
```

### Native CMD (no install)

```cmd
dorkgen.cmd --interactive
```

### Non-interactive mode

```bash
dorkgen --objective public-documents --domain example.com --keyword payroll --filetypes pdf,docx --exclude sample,test
```

### Catalog menu UI

```bash
dorkgen --menu
```

Enable FILE_HUNTER entries explicitly:

```bash
dorkgen --menu --include-file-hunter
```

### Non-interactive catalog mode

```bash
dorkgen --catalog-id sec.attack-surface-mapping.exposed-login-endpoints --domain example.com --keyword auth
```

## PowerShell Quick Start

### 1) Clone and enter the repo

```powershell
cd $env:USERPROFILE\Documents
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT
```

### 2) Run directly (no install)

```powershell
.\dorkgen.ps1 --interactive
```

### 3) Run with flags

```powershell
.\dorkgen.ps1 --objective public-documents --domain example.com --keyword payroll
```

### 4) Optional install for `dorkgen` command

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
dorkgen --interactive
```

## Objectives

- `public-documents`
- `login-portals`
- `public-backups`
- `configuration-files`

## Catalog source and scope

- The curated JSON catalog is adapted from [mitocondria40/OSINT-dork-tool](https://github.com/mitocondria40/OSINT-dork-tool), specifically the dork definitions in `script.js` (`dorksData` structure).
- DorkSINT defaults to `sec` (CYBER_INTEL) entries.
- `media` (FILE_HUNTER) entries are present but only available when the user opts in with `--include-file-hunter`.

## Development

```bash
pip install -e . pytest
pytest
```

## Contributing

See `CONTRIBUTING.md` for local setup and PR checklist.

## License

MIT. See `LICENSE`.

## Legal and Ethical Notice

This tool is provided for legal, authorized security research and defensive reconnaissance only. You are responsible for following all applicable laws, terms of service, and policies in your jurisdiction. Do not use this tool to access systems, data, or services without explicit permission.

`--include-file-hunter` may expose queries that are inappropriate in some environments. Use only where policy and legal scope explicitly allow it.
