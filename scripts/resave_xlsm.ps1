$ErrorActionPreference = 'Stop'

param(
    [Parameter(Mandatory=$true)]
    [string]$Src,

    [Parameter(Mandatory=$true)]
    [string]$Dst
)

Write-Host "Resaving: $Src -> $Dst"

Get-Process EXCEL -ErrorAction SilentlyContinue | Stop-Process -Force

$excel = New-Object -ComObject Excel.Application
$excel.DisplayAlerts = $false
$excel.AskToUpdateLinks = $false

try {
    $wb = $excel.Workbooks.Open($Src, 0, $false)
    # 52 = xlOpenXMLWorkbookMacroEnabled (.xlsm)
    $wb.SaveAs($Dst, 52)
    $wb.Close($false)
    Write-Host "Saved: $Dst"
}
finally {
    $excel.Quit()
}


