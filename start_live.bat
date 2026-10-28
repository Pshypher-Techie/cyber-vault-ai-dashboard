@echo off
title CYBER-VAULT LIVE LAUNCHER
echo ===============================================================
echo CYBER-VAULT :: AI-POWERED INTELLIGENCE DOSSIER (LIVE LAUNCHER)
echo ===============================================================
echo Starting local backend server...
start "Cyber-Vault Server" /B .venv\Scripts\python.exe run.py
timeout /t 2 /nobreak >nul
echo Starting public live tunnel...
cloudflared.exe tunnel --url http://127.0.0.1:8000
pause

