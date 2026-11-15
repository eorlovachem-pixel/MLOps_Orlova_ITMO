$ErrorActionPreference = "Stop"
# Run from HW3 project root in PowerShell.
uv sync
if ($LASTEXITCODE -ne 0) { throw "uv sync failed" }
python scripts/bootstrap_remote.py
if ($LASTEXITCODE -ne 0) { throw "Failed to restore local DVC remote" }
uv run dvc pull
if ($LASTEXITCODE -ne 0) { throw "Failed: dvc pull" }
$commands = @(
    @("dvc", "status"), @("dvc", "repro"), @("dvc", "dag"),
    @("dvc", "metrics", "show"), @("dvc", "push"), @("dvc", "status", "-c")
)
foreach ($cmd in $commands) {
    & uv run @cmd
    if ($LASTEXITCODE -ne 0) { throw "Failed: uv run $($cmd -join ' ')" }
}
Write-Host "Commit uv.lock and DVC metadata after successful execution."
