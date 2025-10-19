import os
import shlex
import subprocess


def _ps_escape(path: str) -> str:
    return path.replace("'", "''")


def build_dashboard(
    workbook_path: str,
    visible: bool = False,
    *,
    events_sheet: str = "Events",
    fighters_sheet: str = "fighters",
    fights_sheet: str = "fights",
) -> None:
    if not os.path.exists(workbook_path):
        raise FileNotFoundError(workbook_path)

    p = _ps_escape(workbook_path)
    ev = _ps_escape(events_sheet)
    fi = _ps_escape(fighters_sheet)
    ft = _ps_escape(fights_sheet)
    vis = "$true" if visible else "$false"

    # PowerShell script builds Dashboard and Lists sheets, dynamic dropdowns,
    # and a placeholder pie chart area wired to dynamic lists.
    ps = f"$ErrorActionPreference='Stop';$path='{p}';$vis={vis};$eventsName='{ev}';$fightersName='{fi}';$fightsName='{ft}';"
    ps += r'''
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $vis
$xl.DisplayAlerts = $false
$xl.AskToUpdateLinks = $false
$wb = $xl.Workbooks.Open($path, 0)  # UpdateLinks=0

function Get-ColIndexByHeader($ws, $header) {
  $ur = $ws.UsedRange
  $cols = $ur.Columns.Count
  for ($c = 1; $c -le $cols; $c++) {
    $val = [string]($ws.Cells.Item(1,$c).Value2)
    if ($val -eq $header) { return $c }
  }
  return $null
}

function ColLetter($n) {
  $s = ""
  while ($n -gt 0) {
    $n = $n - 1
    $s = [char](65 + ($n % 26)) + $s
    $n = [math]::Floor($n / 26)
  }
  return $s
}

# Ensure required sheets exist (create if missing)
$wsEvents = $null
try { $wsEvents = $wb.Worksheets.Item($eventsName) } catch {}
if (-not $wsEvents) { $wsEvents = $wb.Worksheets.Add(); $wsEvents.Name = $eventsName }

$wsFighters = $null
try { $wsFighters = $wb.Worksheets.Item($fightersName) } catch {}
if (-not $wsFighters) { $wsFighters = $wb.Worksheets.Add(); $wsFighters.Name = $fightersName }

# Optional fights sheet
$wsFights = $null
try { $wsFights = $wb.Worksheets.Item($fightsName) } catch {}

### Ensure headers and minimal sample data if sheets are empty
# Events headers
$eventIdColIdx = Get-ColIndexByHeader $wsEvents 'EventId'
if (-not $eventIdColIdx) { $wsEvents.Cells.Item(1,1).Value2 = 'EventId'; $eventIdColIdx = 1 }
$eventDisplayColIdx = (Get-ColIndexByHeader $wsEvents 'Card'); if (-not $eventDisplayColIdx) { $eventDisplayColIdx = (Get-ColIndexByHeader $wsEvents 'Event') }
if (-not $eventDisplayColIdx) { $eventDisplayColIdx = (Get-ColIndexByHeader $wsEvents 'EventName') }
if (-not $eventDisplayColIdx) { $eventDisplayColIdx = (Get-ColIndexByHeader $wsEvents 'Name') }
$eventsRowCount = $wsEvents.UsedRange.Rows.Count
if ($eventsRowCount -lt 3 -and -not [string]($wsEvents.Cells.Item(2,1).Value2)) {
  $wsEvents.Cells.Item(2,1).Value2 = 'E001'
  $wsEvents.Cells.Item(3,1).Value2 = 'E002'
}

# fighters headers
$fightersEventIdColIdx = Get-ColIndexByHeader $wsFighters 'EventId'
$fightersNameColIdx = (Get-ColIndexByHeader $wsFighters 'Name'); if (-not $fightersNameColIdx) { $fightersNameColIdx = (Get-ColIndexByHeader $wsFighters 'Fighter') }
if (-not $fightersEventIdColIdx) { $wsFighters.Cells.Item(1,1).Value2 = 'EventId'; $fightersEventIdColIdx = 1 }
if (-not $fightersNameColIdx) { $wsFighters.Cells.Item(1,2).Value2 = 'Name'; $fightersNameColIdx = 2 }
$fightersRowCount = $wsFighters.UsedRange.Rows.Count
if ($fightersRowCount -lt 3 -and -not [string]($wsFighters.Cells.Item(2,1).Value2)) {
  $wsFighters.Cells.Item(2,$fightersEventIdColIdx).Value2 = 'E001'
  $wsFighters.Cells.Item(2,$fightersNameColIdx).Value2 = 'Fighter A'
  $wsFighters.Cells.Item(3,$fightersEventIdColIdx).Value2 = 'E002'
  $wsFighters.Cells.Item(3,$fightersNameColIdx).Value2 = 'Fighter B'
}

$fightsEventIdColIdx = $null; $fightsNameColIdx = $null
if ($wsFights) {
  $fightsEventIdColIdx = Get-ColIndexByHeader $wsFights 'EventId'
  $fightsNameColIdx = (Get-ColIndexByHeader $wsFights 'FightName'); if (-not $fightsNameColIdx) { $fightsNameColIdx = (Get-ColIndexByHeader $wsFights 'Bout') }
  if (-not $fightsEventIdColIdx) { $wsFights.Cells.Item(1,1).Value2 = 'EventId'; $fightsEventIdColIdx = 1 }
  if (-not $fightsNameColIdx) { $wsFights.Cells.Item(1,2).Value2 = 'FightName'; $fightsNameColIdx = 2 }
  $fightsRowCount = $wsFights.UsedRange.Rows.Count
  if ($fightsRowCount -lt 3 -and -not [string]($wsFights.Cells.Item(2,1).Value2)) {
    $wsFights.Cells.Item(2,$fightsEventIdColIdx).Value2 = 'E001'
    $wsFights.Cells.Item(2,$fightsNameColIdx).Value2 = 'Bout 1'
    $wsFights.Cells.Item(3,$fightsEventIdColIdx).Value2 = 'E002'
    $wsFights.Cells.Item(3,$fightsNameColIdx).Value2 = 'Bout 2'
  }
}

$eventColL = ColLetter $eventIdColIdx
$eventDisplayColL = $null; if ($eventDisplayColIdx) { $eventDisplayColL = (ColLetter $eventDisplayColIdx) }
$fightersEvColL = ColLetter $fightersEventIdColIdx
$fightersNameColL = ColLetter $fightersNameColIdx
if ($fightsEventIdColIdx) { $fightsEvColL = ColLetter $fightsEventIdColIdx }
if ($fightsNameColIdx) { $fightsNameColL = ColLetter $fightsNameColIdx }

# Quoted sheet names for formulas
$eventsSheetName = $wsEvents.Name
$fightersSheetName = $wsFighters.Name
$qEvents = "'" + $eventsSheetName + "'"
$qFighters = "'" + $fightersSheetName + "'"
if ($wsFights) { $fightsSheetName = $wsFights.Name; $qFights = "'" + $fightsSheetName + "'" }

# Ensure Dashboard sheet FIRST (to avoid external link prompts when formulas reference it)
$wsDash = $null
try { $wsDash = $wb.Worksheets.Item('Dashboard') } catch {}
if (-not $wsDash) { $wsDash = $wb.Worksheets.Add(); $wsDash.Name = 'Dashboard' }
$wsDash.Cells.Clear()
$wsDash.Range('B1').Value2 = 'Event'
$wsDash.Range('C1').Value2 = 'Fighter'
$wsDash.Range('D1').Value2 = 'Fight'

# Now ensure Lists sheet and insert formulas referencing Dashboard
$wsLists = $null
try { $wsLists = $wb.Worksheets.Item('Lists') } catch {}
if (-not $wsLists) { $wsLists = $wb.Worksheets.Add(); $wsLists.Name = 'Lists' }
$wsLists.Cells.Clear()
$wsLists.Range('A1').Value2 = 'EventIds'
$wsLists.Range('B1').Value2 = 'FightersByEvent'
$wsLists.Range('C1').Value2 = 'FightsByEvent'
$wsLists.Range('D1').Value2 = 'SelectedEventId'
$wsLists.Range('G1').Value2 = 'EventNames'

$partsEvent = @("=UNIQUE(FILTER(", $qEvents, "!$", $eventColL, ":$", $eventColL, ", ", $qEvents, "!$", $eventColL, ":$", $eventColL, '<>""', "))")
$formulaEventIds = ($partsEvent -join "")
$wsLists.Range('A2').Formula = $formulaEventIds

$eventNamesAdded = $false
if ($eventDisplayColL) {
  $partsEventNames = @("=UNIQUE(FILTER(", $qEvents, "!$", $eventDisplayColL, ":$", $eventDisplayColL, ", ", $qEvents, "!$", $eventDisplayColL, ":$", $eventDisplayColL, '<>""', "))")
  $formulaEventNames = ($partsEventNames -join "")
  $wsLists.Range('G2').Formula = $formulaEventNames
  # Selected EventId from chosen Event name
  $partsSel = @("=IFERROR(XLOOKUP(Dashboard!$B$2, ", $qEvents, "!$", $eventDisplayColL, ":$", $eventDisplayColL, ", ", $qEvents, "!$", $eventColL, ":$", $eventColL, ', ""), "")')
  $formulaSelected = ($partsSel -join "")
  $wsLists.Range('D2').Formula = $formulaSelected
  $eventNamesAdded = $true
} else {
  # Fallback: use direct EventId selection
  $wsLists.Range('D2').Formula = '=Dashboard!$B$2'
}

$partsFighters = @("=UNIQUE(FILTER(", $qFighters, "!$", $fightersNameColL, ":$", $fightersNameColL, ", ", $qFighters, "!$", $fightersEvColL, ":$", $fightersEvColL, '=Lists!$D$2', "))")
$formulaFighters = ($partsFighters -join "")
$wsLists.Range('B2').Formula = $formulaFighters

if ($wsFights -and $fightsEventIdColIdx -and $fightsNameColIdx) {
  $partsFights = @("=UNIQUE(FILTER(", $qFights, "!$", $fightsNameColL, ":$", $fightsNameColL, ", ", $qFights, "!$", $fightsEvColL, ":$", $fightsEvColL, '=Lists!$D$2', "))")
  $formulaFights = ($partsFights -join "")
  $wsLists.Range('C2').Formula = $formulaFights
}

# Data validation dropdowns
$xlValidateList = 3
$xlBetween = 1
$dv1 = $wsDash.Range('B2').Validation
$dv1.Delete(); $dv1.Add($xlValidateList, $xlBetween, 1, '=Lists!$G$2#')
$dv2 = $wsDash.Range('C2').Validation
$dv2.Delete(); $dv2.Add($xlValidateList, $xlBetween, 1, '=Lists!$B$2#')
try {
  $dv3 = $wsDash.Range('D2').Validation
  $dv3.Delete(); $dv3.Add($xlValidateList, $xlBetween, 1, '=Lists!$C$2#')
} catch {}

# Freeze panes (split screen feel)
try {
  $xl.ActiveWindow.SplitColumn = 1
  $xl.ActiveWindow.SplitRow = 1
  $xl.ActiveWindow.FreezePanes = $true
} catch {}

# Placeholder pie chart using fighter count for selected event
$wsLists.Range('E1').Value2 = 'Label'
$wsLists.Range('F1').Value2 = 'Value'
# Build label and value formulas using the detected fighters name column
$partsLabels = @("=UNIQUE(", $qFighters, "!$", $fightersNameColL, ":$", $fightersNameColL, ")")
$formulaLabels = ($partsLabels -join "")
$wsLists.Range('E2').Formula = $formulaLabels
$wsLists.Range('F2').Formula = '=IF(LEN(E2#)>0,1,"")'

# Create chart on Dashboard linked to E2# / F2#
$charts = $wsDash.ChartObjects()
if ($charts.Count -gt 0) { $charts.Item(1).Delete() }
$co = $wsDash.ChartObjects().Add(300, 20, 360, 220)
$ch = $co.Chart
$ch.ChartType = 5  # xlPie
$ch.SetSourceData($wsLists.Range('F2').Resize(1000,1))
$ch.SeriesCollection(1).XValues = $wsLists.Range('E2').Resize(1000,1)
$ch.HasTitle = $true
$ch.ChartTitle.Text = 'Fighters (demo)'

$wb.Save()
$wb.Close($true)
$xl.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($wsDash) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($wsLists) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($wb) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
'''

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        # Surface PowerShell errors to help diagnose sheet/header issues
        raise RuntimeError(
            "PowerShell dashboard build failed.\n" +
            (f"STDOUT:\n{e.stdout}\n" if e.stdout else "") +
            (f"STDERR:\n{e.stderr}\n" if e.stderr else "")
        ) from e


