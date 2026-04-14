$ErrorActionPreference = "Stop"
$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 -m dorkgen.cli @args
} else {
    python -m dorkgen.cli @args
}

