<div align="center">

```
 ____             _    ____ ___ _   _ _____
|  _ \  ___  _ __| | _/ ___|_ _| \ | |_   _|
| | | |/ _ \| '__| |/ \___ \| ||  \| | | |
| |_| | (_) | |  |   < ___) | || |\  | | |
|____/ \___/|_|  |_|\_\____/___|_| \_| |_|
```

**Terminal-first Google dork generator for authorized recon.**

Turn a search objective into structured, copy-ready Google dork queries — entirely from your shell.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-informational)
![Interface](https://img.shields.io/badge/interface-terminal--only-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

</div>

---

## Contents

- [About](#about)
- [Features](#features)
- [Install](#install)
  - [Arch Linux / Manjaro](#arch-linux--manjaro)
  - [Ubuntu / Debian / Kali / Mint](#ubuntu--debian--kali--mint)
  - [Fedora / RHEL / Rocky / Alma](#fedora--rhel--rocky--alma)
  - [openSUSE](#opensuse)
  - [Any Linux / macOS (pip)](#any-linux--macos-pip)
  - [Windows (PowerShell / CMD)](#windows-powershell--cmd)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Fast catalog discovery](#fast-catalog-discovery)
- [Flag reference](#flag-reference)
- [Power-user terminal recipes](#power-user-terminal-recipes)
- [Objectives](#objectives)
- [Catalog scope](#catalog-source-and-scope)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Legal and ethical notice](#legal-and-ethical-notice)

---

## About

DorkSINT is an open-source Python CLI that speeds up Google dorking by turning your search
objective into structured, paste-ready queries. It supports interactive prompts, non-interactive
flags for scripting, a curated catalog of 30+ vetted dorks, and quality-of-life helpers like
clipboard copy, browser launch, and greppable catalog search.

It runs natively in **Bash, Zsh, Fish, PowerShell, and CMD** with **zero third-party dependencies** —
only the Python standard library.

> **DorkSINT is entirely terminal-based.** There is no web app, static site, or browser-based UI in
> scope. Every interaction happens through the CLI.

Built for **legal, authorized** security research and defensive reconnaissance workflows.

---

## Features

- 🎯 **Objective-driven** — say what you're looking for; get tuned query variants.
- 🧩 **Curated catalog** — 30 security dorks across 20 categories (plus opt-in media dorks).
- 🔎 **Greppable discovery** — `--list` / `--search` dump the catalog as one line per entry, made for `grep`/`fzf`.
- ⚡ **Pipe-friendly** — `--plain` emits raw dorks, one per line, for scripting.
- 📋 **Clipboard & browser** — `--copy` and `--open` get you searching in one keystroke.
- 🎨 **Readable output** — boxed, color-aware panels that degrade gracefully on basic terminals.
- 🤖 **Automation-ready** — non-interactive flags, predictable exit codes, no network calls of its own.
- 🛡️ **Safe defaults** — security (`sec`) catalog entries by default; sensitive media dorks gated behind an explicit opt-in.

---

## Install

DorkSINT needs **Python 3.9+** and `git`. Pick your distro below. All commands are copy-paste ready.

### Arch Linux / Manjaro

```bash
sudo pacman -S --needed python git
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT

# Run instantly, no install:
PYTHONPATH=src python -m dorkgen.cli --interactive

# Or install the `dorkgen` command into an isolated environment:
python -m venv .venv && source .venv/bin/activate
pip install -e .
dorkgen --interactive
```

> Optional clipboard support: `sudo pacman -S wl-clipboard` (Wayland) or `xclip` (X11).

### Ubuntu / Debian / Kali / Mint

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT

python3 -m venv .venv && source .venv/bin/activate
pip install -e .
dorkgen --interactive
```

> Optional clipboard support: `sudo apt install xclip` (X11) or `wl-clipboard` (Wayland).

### Fedora / RHEL / Rocky / Alma

```bash
sudo dnf install -y python3 python3-pip git
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT

python3 -m venv .venv && source .venv/bin/activate
pip install -e .
dorkgen --interactive
```

> Optional clipboard support: `sudo dnf install xclip` or `wl-clipboard`.

### openSUSE

```bash
sudo zypper install python3 python3-pip git
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT

python3 -m venv .venv && source .venv/bin/activate
pip install -e .
dorkgen --interactive
```

### Any Linux / macOS (pip)

The cross-platform path. On macOS, `brew install python git` first if needed.

```bash
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT
python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS path: bin/, not Scripts/
pip install -e .
dorkgen --interactive
```

> macOS clipboard works out of the box (`pbcopy`). To open searches in your browser, `--open` uses the system default.

### Windows (PowerShell / CMD)

No install required — wrappers are included.

```powershell
git clone https://github.com/DiggityDooo/DorkSINT.git
cd DorkSINT
.\dorkgen.ps1 --interactive
```

```cmd
dorkgen.cmd --interactive
```

<details>
<summary>PowerShell gotchas</summary>

- If you hit an execution-policy error: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Run the script and its flags on **one line**. Don't press Enter after the script name.
- `".\dorkgen.ps1"` in quotes only **prints** the path — run it as `.\dorkgen.ps1 ...` or `& .\dorkgen.ps1 ...`.
- Quote CSV values so commas aren't split: `--filetypes "pdf,xlsx"` and `--exclude "sample,demo"`.

Optional install for the `dorkgen` command:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
dorkgen --interactive
```

</details>

---

## Quick start

```bash
# 1. Discover what's in the catalog (greppable)
dorkgen --list

# 2. Find dorks about a topic, fast
dorkgen --search s3

# 3. Run one and copy it to your clipboard
dorkgen --catalog-id sec.cloud-storage-exposure.amazon-s3-references --domain example.com --copy

# 4. Or generate a full set of variants for an objective
dorkgen --objective public-documents --domain example.com --keyword payroll
```

Sample output:

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│ DorkSINT Output                                                                │
│────────────────────────────────────────────────────────────────────────────────│
│ Generated dorks (copy and paste into Google):                                  │
│                                                                                │
│ 1. site:example.com payroll (filetype:pdf OR filetype:docx) intitle:"index of" │
│ 2. site:example.com intitle:payroll confidential                               │
│ 3. site:example.com inurl:payroll payroll filetype:pdf                         │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Usage

### Interactive mode

```bash
dorkgen --interactive
```

### Non-interactive (scripting)

```bash
dorkgen --objective public-documents --domain example.com --keyword payroll \
        --filetypes pdf,docx --exclude sample,test
```

### Catalog menu (guided browser)

```bash
dorkgen --menu
dorkgen --menu --include-file-hunter      # opt in to media dorks
```

### Run a catalog entry by id

```bash
dorkgen --catalog-id sec.attack-surface-mapping.exposed-login-endpoints --domain example.com --keyword auth
```

### Plain output, clipboard, and browser

```bash
dorkgen --objective login-portals --domain example.com --plain       # one dork per line
dorkgen --objective login-portals --domain example.com --copy        # copy first query
dorkgen --objective login-portals --domain example.com --open        # open first query in browser
```

---

## Fast catalog discovery

The fastest way to work is to keep everything in the terminal. `--list` and `--search` print
**one greppable line per entry** (`id  category / label  ::  dork`) to stdout, with a summary on
stderr so pipes stay clean.

```bash
dorkgen --list                       # everything (sec only by default)
dorkgen --list --include-file-hunter # include media dorks
dorkgen --search admin               # filter by id/category/label/dork
dorkgen --search s3 | awk '{print $1}'   # just the catalog ids
```

---

## Flag reference

| Flag | Description |
| --- | --- |
| `--objective KEY` | Generate variant dorks for an objective (see [Objectives](#objectives)). |
| `--domain DOMAIN` | Scope queries to a domain, e.g. `example.com`. |
| `--keyword TEXT` | Keyword/phrase to prioritize. |
| `--filetypes CSV` | Comma list of filetypes, e.g. `pdf,xlsx`. |
| `--exclude CSV` | Comma list of terms to exclude. |
| `--catalog-id ID` | Run one curated catalog entry by id. |
| `--menu` | Guided, numbered catalog browser. |
| `--include-file-hunter` | Include opt-in media (`FILE_HUNTER`) catalog entries. |
| `--list` | Print catalog entries as greppable lines and exit. |
| `--search TERM` | Filter the catalog by `TERM` and exit. |
| `--interactive` | Force interactive prompts. |
| `--plain` | Print dorks as plain lines (no box) — ideal for piping. |
| `--open` | Open the first generated query in your default browser. |
| `--copy` | Copy the first generated query to the system clipboard. |
| `--no-color` | Disable ANSI colors. |
| `--no-banner` | Suppress the startup banner. |
| `--version` | Print version and exit. |

Colors and the banner auto-disable when output is piped or when `NO_COLOR` is set, so scripted
output stays clean without extra flags.

---

## Power-user terminal recipes

```bash
# Fuzzy-pick a catalog id, run it, and copy the result
id=$(dorkgen --list | fzf | awk '{print $1}') && dorkgen --catalog-id "$id" --domain example.com --copy

# Pipe a generated dork straight to your clipboard helper
dorkgen --objective configuration-files --domain example.com --plain | head -1 | wl-copy

# Loop a single dork over many targets
for d in a.com b.com c.com; do dorkgen --catalog-id sec.exposed-documents.pdf-documents --domain "$d" --plain; done

# Handy shell alias (add to ~/.bashrc or ~/.zshrc)
alias dork='dorkgen'
alias dorks='dorkgen --list'
```

---

## Objectives

| Key | Generates |
| --- | --- |
| `public-documents` | Exposed documents, open directories, sensitive filetypes. |
| `login-portals` | Login / sign-in / admin entry points. |
| `public-backups` | Backups, archives, dumps, open directory listings. |
| `configuration-files` | Config files, env files, settings that may leak secrets. |

---

## Catalog source and scope

- The curated JSON catalog is adapted from open OSINT dork definitions and organized into DorkSINT categories.
- **30 security dorks** across **20 categories** ship enabled by default (`sec` / `CYBER_INTEL`).
- **6 media dorks** (`media` / `FILE_HUNTER`) are present but only available when you opt in with `--include-file-hunter`.

Browse them anytime with `dorkgen --list` or `dorkgen --search <term>`.

---

## Development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest
pytest
```

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for local setup and the PR checklist.

---

## License

MIT. See [`LICENSE`](LICENSE).

---

## Legal and ethical notice

This tool is provided for **legal, authorized** security research and defensive reconnaissance only.
You are responsible for following all applicable laws, terms of service, and policies in your
jurisdiction. Do not use this tool to access systems, data, or services without explicit permission.

`--include-file-hunter` may expose queries that are inappropriate in some environments. Use only
where policy and legal scope explicitly allow it.
