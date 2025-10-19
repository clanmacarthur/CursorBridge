@echo off
if "%~1"=="dashboard-profiles" goto DASH_PROFILES
if "%~1"=="dashboard-safe" goto DASH_SAFE
python -m cb.cli %*
goto END

:DASH_PROFILES
REM One-click: build dashboard using Events and Profiles sheet names
python -m cb.cli dashboard --workbook "C:\Users\j-lot\Documents\Power Automate and Spreadsheets\Excel\De Ridder vs. Allen.xlsm" --events-sheet "Events" --fighters-sheet "Profiles" --visible
goto END

:DASH_SAFE
REM One-click: build minimal safe dashboard (no COM, no dynamic arrays)
REM Ensure openpyxl is available
python -c "import openpyxl" >nul 2>&1
if %errorlevel% neq 0 (
  python -m pip install --user openpyxl >nul 2>&1
)
python -m cb.cli dashboard --workbook "C:\Users\j-lot\Documents\Power Automate and Spreadsheets\Excel\De Ridder vs. Allen.xlsm" --events-sheet "Events" --fighters-sheet "Profiles" --safe
goto END

:END
