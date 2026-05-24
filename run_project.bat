@echo off
title CareerForge AI Launcher
echo ==================================================
echo   🚀 CareerForge AI — Unified Startup Script
echo ==================================================
echo.

:: 1. Start Backend
echo [INFO] Starting FastAPI Backend...
start "CareerForge Backend" cmd /k "cd backend && ..\venv\Scripts\python.exe main.py"

:: 2. Check for Node.js / npm
:: 2. Start Frontend (requires Node.js)
echo [INFO] Starting Vite Frontend on http://localhost:5173...
start "CareerForge Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==================================================
echo   ✅ Startup sequence completed!
echo   - Backend   : http://localhost:8000
echo   - API Docs  : http://localhost:8000/docs
echo   - Frontend  : http://localhost:5173 (once Node is installed)
echo ==================================================
echo.
pause
