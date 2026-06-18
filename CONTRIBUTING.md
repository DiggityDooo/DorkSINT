# Contributing

Thanks for contributing to Google Dork CLI.

## Ground rules

- Keep changes focused and small.
- Add or update tests for behavior changes.
- Preserve legal/ethical language and avoid unsafe defaults.
- Use clear commit messages that explain why.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .\.venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -e . pytest
```

## Run checks

```bash
pytest
```

## Pull request checklist

- [ ] Tests pass locally
- [ ] README and examples updated (if needed)
- [ ] No secrets or local files committed
- [ ] Changes remain compatible with PowerShell and CMD launchers

