@echo off
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3 from https://www.python.org/downloads/
  echo During setup, enable "Add python.exe to PATH".
  pause
  exit /b 1
)

echo Starting Knowledge Treasury...
echo Browser will open at http://127.0.0.1:8020/index.html
echo Leave this window open while you browse the site.
echo.

python helpers\serve_site.py --bind 127.0.0.1 --port 8020 --open
if errorlevel 1 (
  echo.
  echo The server could not start. Port 8020 may already be in use.
  echo Close any other Knowledge Treasury server window and try again.
  pause
  exit /b 1
)
