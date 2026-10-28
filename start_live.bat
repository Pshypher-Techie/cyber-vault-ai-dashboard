@echo off
title CYBER-VAULT LIVE LAUNCHER
echo ===============================================================
echo CYBER-VAULT :: BISWAJEET SHADANGI (LIVE LAUNCHER)
echo ===============================================================

:: 1. Terminate any previous orphaned instances cleanly
taskkill /F /IM cloudflared.exe >nul 2>&1

echo [1/2] Starting local Python backend server on http://127.0.0.1:8000 ...
start "Cyber-Vault Server" /B .venv\Scripts\python.exe run.py
timeout /t 3 /nobreak >nul

echo [2/2] Connecting high-speed public tunnel...
echo Look for the public HTTPS URL below (e.g., https://xxxx.trycloudflare.com):
echo ===============================================================
cloudflared.exe tunnel --edge-ip-version 4 --url http://127.0.0.1:8000
pause
