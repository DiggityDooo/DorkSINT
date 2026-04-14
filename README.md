# DorkSINT

An open-source Python CLI that asks what you are trying to find, takes your target details, and generates copy-ready Google dork queries to speed up search workflow.

## Features

- Interactive prompts for objective and target details.
- Non-interactive mode for scripts/automation.
- Multiple query variants per request (title-based, URL-based, filetype-based).
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

### Native CMD (no install)

```cmd
dorkgen.cmd --interactive
```

### Non-interactive mode

```bash
dorkgen --objective public-documents --domain example.com --keyword payroll --filetypes pdf,docx --exclude sample,test
```

## Objectives

- `public-documents`
- `login-portals`
- `public-backups`
- `configuration-files`

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
