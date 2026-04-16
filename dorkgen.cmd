@echo off
setlocal
set "PYTHONPATH=%~dp0src"
if not defined CI (
  chcp 65001 >nul
)
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 -m dorkgen.cli %*
  goto :eof
)
python -m dorkgen.cli %*

