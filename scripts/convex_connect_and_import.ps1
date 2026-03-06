# Convex connect + schema apply + seed import
# Run this in an interactive terminal (not CI/non-interactive shell).

$ErrorActionPreference = "Stop"

$Workspace = "C:\code\Regenerative-Hive-Mind"
$Bridge = "C:\code\CursorBridge"

function Invoke-Step {
  param(
    [Parameter(Mandatory = $true)][string]$Label,
    [Parameter(Mandatory = $true)][string[]]$Command
  )

  Write-Host $Label -ForegroundColor Cyan
  & $Command[0] $Command[1..($Command.Length - 1)]
  if ($LASTEXITCODE -ne 0) {
    throw "Step failed: $Label"
  }
}

Write-Host "Step 1/4: Move to Convex workspace" -ForegroundColor Cyan
Set-Location $Workspace

Invoke-Step -Label "Step 2/4: Convex login (interactive)" -Command @("npx.cmd", "convex", "login")

Invoke-Step -Label "Step 3/4: Apply schema (interactive project link if needed)" -Command @("npx.cmd", "convex", "dev")

Set-Location $Bridge
Invoke-Step -Label "Step 4/4: Import prepared seed data" -Command @(
  "python",
  "scripts/import_convex_seed_with_cli.py",
  "--workspace",
  $Workspace,
  "--execute"
)

Write-Host ""
Write-Host "Done. Next: run runtime sanity checks and update readiness gates." -ForegroundColor Green
