$ErrorActionPreference = "Stop"
$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
$interactiveHost = $Host.Name -eq "ConsoleHost" -and -not [Console]::IsOutputRedirected
if ($interactiveHost) {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 -m dorkgen.cli @args
} else {
    python -m dorkgen.cli @args
}

