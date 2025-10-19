@echo off
if "%~1"=="dashboard-profiles" goto DASH_PROFILES
python -m cb.cli %*
goto END

:DASH_PROFILES
REM One-click: build dashboard using Events and Profiles sheet names
python -m cb.cli dashboard --workbook "C:\Users\j-lot\Documents\Power Automate and Spreadsheets\Excel\De Ridder vs. Allen.xlsm" --events-sheet "Events" --fighters-sheet "Profiles" --visible
goto END

:END
