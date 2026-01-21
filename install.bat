@echo off
echo ========================================
echo    Installation AutoDoc
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe.
    echo Telecharge Python sur https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detecte

:: Install backend dependencies
echo.
echo Installation des dependances backend...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)
echo [OK] Dependances installees

:: Install Playwright browser
echo.
echo Installation du navigateur Playwright (pour PDF)...
playwright install chromium
if errorlevel 1 (
    echo [ATTENTION] Playwright n'a pas pu installer Chromium
    echo Le PDF pourrait ne pas fonctionner
)
echo [OK] Playwright installe

cd ..

echo.
echo ========================================
echo    Installation terminee !
echo ========================================
echo.
echo Pour lancer l'application, double-clique sur start.bat
echo.
pause
