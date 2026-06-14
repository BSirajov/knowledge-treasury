@echo off
cd /d "%~dp0"
python helpers\serve_site.py --bind 127.0.0.1 --port 8020