@echo off
setlocal

REM Kill any stuck Excel instance silently
for /f "tokens=2" %%P in ('tasklist ^| find /I "EXCEL.EXE"') do (
  taskkill /PID %%P /F >nul 2>&1
)

REM Ensure openpyxl is installed
python -c "import openpyxl" >nul 2>&1
if %errorlevel% neq 0 (
  echo Installing openpyxl...
  python -m pip install --user openpyxl >nul 2>&1
)

REM Run safe-mode builder (no COM, no dynamic arrays)
python -m cb.cli dashboard --workbook "C:\Users\j-lot\Documents\Power Automate and Spreadsheets\Excel\De Ridder vs. Allen.xlsm" --events-sheet "Events" --fighters-sheet "Profiles" --safe
if %errorlevel% neq 0 (
  echo Build failed. See above for errors.
  exit /b %errorlevel%
)

echo Done. Open your workbook and check Dashboard!B2 for the Event dropdown.
endlocal
