@echo off
echo ========================================
echo    Demarrage AutoDoc
echo ========================================
echo.

:: Start backend in new window
echo Demarrage du backend...
start "AutoDoc Backend" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"

:: Wait a bit for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in new window
echo Demarrage du frontend...
start "AutoDoc Frontend" cmd /k "cd frontend && python -m http.server 3000"

:: Wait a bit
timeout /t 2 /nobreak >nul

:: Open browser
echo Ouverture du navigateur...
start http://localhost:3000

echo.
echo ========================================
echo    AutoDoc demarre !
echo ========================================
echo.
echo Backend : http://localhost:8000
echo Frontend : http://localhost:3000
echo.
echo Fermez cette fenetre pour arreter les serveurs.
echo.
pause
