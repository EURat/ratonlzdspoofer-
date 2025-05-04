@echo off
REM Build the Flask app into a single executable without --uac-admin flag
REM Manifest embedding step removed temporarily due to errors

REM Check if PyInstaller is installed, install if not
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Check if pywebview is installed, install if not
pip show pywebview >nul 2>&1
if errorlevel 1 (
    echo Installing pywebview...
    pip install pywebview
)

REM Build without icon to avoid missing icon error
python -m PyInstaller --noconfirm --onefile --windowed --add-data "templates;templates" --add-data "static;static" --name ratonlzd app.py

echo Build complete. The executable 'ratonlzd.exe' is in the dist folder.

pause
