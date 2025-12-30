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

REM Run one-shot safe dashboard builder (Connector -> Dropdowns -> Stats -> Charts)
python scripts\build_dashboard_safe.py --workbook "C:\Users\j-lot\Documents\Power Automate and Spreadsheets\Excel\De Ridder vs. Allen.xlsm" --events-sheet "Events" --profiles-sheet "Profiles" --stats-sheet "FightsStats"
if %errorlevel% neq 0 (
  echo Build failed. See above for errors.
  exit /b %errorlevel%
)

echo Done. Open your workbook and check Dashboard!B2/C2 and stats/charts on the Dashboard.
endlocal
