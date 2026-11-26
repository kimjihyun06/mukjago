@echo off
cd /d "%~dp0"
echo [1/2] ø¢ºø -> ªÛ«∞ ∏∏µÈ±‚ (..\¿⁄∑·\ø¢ºø ¿« √÷Ω≈ xlsx)
python tools\import_excel.py %1
if errorlevel 1 goto end
echo.
echo [2/2] ¡°∞À
python tools\state.py check
:end
pause
