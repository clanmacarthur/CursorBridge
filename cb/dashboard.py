import os
import shlex
import subprocess


def _ps_escape(path: str) -> str:
    return path.replace("'", "''")


def build_dashboard(workbook_path: str) -> None:
    if not os.path.exists(workbook_path):
        raise FileNotFoundError(workbook_path)

    p = _ps_escape(workbook_path)

    # PowerShell script builds Dashboard and Lists sheets, dynamic dropdowns,
    # and a placeholder pie chart area wired to dynamic lists.
    ps = f"$ErrorActionPreference='Stop';$path='{p}';"
    ps += r'''
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$wb = $xl.Workbooks.Open($path)

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

$wsEvents = $wb.Worksheets.Item('Events') 2>$null
$wsFighters = $wb.Worksheets.Item('fighters') 2>$null
$wsFights = $wb.Worksheets.Item('fights') 2>$null
if (-not $wsEvents -or -not $wsFighters) { throw 'Required sheets: Events and fighters' }

$eventIdColIdx = Get-ColIndexByHeader $wsEvents 'EventId'
if (-not $eventIdColIdx) { throw 'Events: missing EventId header' }
$fightersEventIdColIdx = Get-ColIndexByHeader $wsFighters 'EventId'
$fightersNameColIdx = (Get-ColIndexByHeader $wsFighters 'Name'); if (-not $fightersNameColIdx) { $fightersNameColIdx = (Get-ColIndexByHeader $wsFighters 'Fighter') }
if (-not $fightersEventIdColIdx -or -not $fightersNameColIdx) { throw 'fighters: missing EventId or Name/Fighter header' }

$fightsEventIdColIdx = $null; $fightsNameColIdx = $null
if ($wsFights) {
  $fightsEventIdColIdx = Get-ColIndexByHeader $wsFights 'EventId'
  $fightsNameColIdx = (Get-ColIndexByHeader $wsFights 'FightName'); if (-not $fightsNameColIdx) { $fightsNameColIdx = (Get-ColIndexByHeader $wsFights 'Bout') }
}

$eventColL = ColLetter $eventIdColIdx
$fightersEvColL = ColLetter $fightersEventIdColIdx
$fightersNameColL = ColLetter $fightersNameColIdx
if ($fightsEventIdColIdx) { $fightsEvColL = ColLetter $fightsEventIdColIdx }
if ($fightsNameColIdx) { $fightsNameColL = ColLetter $fightsNameColIdx }

# Ensure Lists sheet
$wsLists = $null
try { $wsLists = $wb.Worksheets.Item('Lists') } catch {}
if (-not $wsLists) { $wsLists = $wb.Worksheets.Add(); $wsLists.Name = 'Lists' }
$wsLists.Cells.Clear()
$wsLists.Range('A1').Value2 = 'EventIds'
$wsLists.Range('B1').Value2 = 'FightersByEvent'
$wsLists.Range('C1').Value2 = 'FightsByEvent'

$formulaEventIds = "=UNIQUE(FILTER(Events!$${eventColL}:$${eventColL}, Events!$${eventColL}:$${eventColL}<>\"\"))"
$wsLists.Range('A2').Formula = $formulaEventIds

$formulaFighters = "=UNIQUE(FILTER(fighters!$${fightersNameColL}:$${fightersNameColL}, fighters!$${fightersEvColL}:$${fightersEvColL}=Dashboard!$B$2))"
$wsLists.Range('B2').Formula = $formulaFighters

if ($wsFights -and $fightsEventIdColIdx -and $fightsNameColIdx) {
  $formulaFights = "=UNIQUE(FILTER(fights!$${fightsNameColL}:$${fightsNameColL}, fights!$${fightsEvColL}:$${fightsEvColL}=Dashboard!$B$2))"
  $wsLists.Range('C2').Formula = $formulaFights
}

# Ensure Dashboard sheet
$wsDash = $null
try { $wsDash = $wb.Worksheets.Item('Dashboard') } catch {}
if (-not $wsDash) { $wsDash = $wb.Worksheets.Add(); $wsDash.Name = 'Dashboard' }
$wsDash.Cells.Clear()
$wsDash.Range('B1').Value2 = 'EventId'
$wsDash.Range('C1').Value2 = 'Fighter'
$wsDash.Range('D1').Value2 = 'Fight'

# Data validation dropdowns
$xlValidateList = 3
$xlBetween = 1
$dv1 = $wsDash.Range('B2').Validation
$dv1.Delete(); $dv1.Add($xlValidateList, $xlBetween, 1, '=Lists!$A$2#')
$dv2 = $wsDash.Range('C2').Validation
$dv2.Delete(); $dv2.Add($xlValidateList, $xlBetween, 1, '=Lists!$B$2#')
try {
  $dv3 = $wsDash.Range('D2').Validation
  $dv3.Delete(); $dv3.Add($xlValidateList, $xlBetween, 1, '=Lists!$C$2#')
} catch {}

# Freeze panes (split screen feel)
$xl.ActiveWindow.SplitColumn = 1
$xl.ActiveWindow.SplitRow = 1
$xl.ActiveWindow.FreezePanes = $true

# Placeholder pie chart using fighter count for selected event
$wsLists.Range('E1').Value2 = 'Label'
$wsLists.Range('F1').Value2 = 'Value'
$wsLists.Range('E2').Formula = '=UNIQUE(fighters!$''' + $fightersNameColL + "''' :$''' + $fightersNameColL + ''' )'
$wsLists.Range('F2').Formula = '=IF(LEN(INDEX(E2#,ROW(E2:E1048576)-ROW(E2)+1))>0,1,"")'

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

    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


