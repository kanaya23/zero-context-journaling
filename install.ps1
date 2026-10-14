# Install script for zero-context-journaling Antigravity skill
param(
    [switch]$Workspace
)

$ErrorActionPreference = "Stop"
$sourceDir = $PSScriptRoot

if ($Workspace) {
    $targetDir = Join-Path (Get-Location) ".agents\skills\zero-context-journaling"
    Write-Host "Installing zero-context-journaling skill to workspace .agents..." -ForegroundColor Cyan
} else {
    $targetDir = Join-Path $env:USERPROFILE ".gemini\config\skills\zero-context-journaling"
    Write-Host "Installing zero-context-journaling skill to global Antigravity config..." -ForegroundColor Cyan
}

Write-Host "Source: $sourceDir"
Write-Host "Target: $targetDir"

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Copy-Item -Path "$sourceDir\*" -Destination $targetDir -Recurse -Force

Write-Host "`nSkill successfully installed! Antigravity will automatically discover zero-context-journaling." -ForegroundColor Green
