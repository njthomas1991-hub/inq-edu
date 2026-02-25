$root = "D:\vs-projects\inq-ed\inq-ed site\inclusive_quest_education"
Set-Location $root
$patterns = @('truffle_results*', '.secrets*')
$found = Get-ChildItem -Path $root -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { foreach ($p in $patterns) { if ($_.Name -like $p) { return $true } }; return $false }
if ($found -and $found.Count -gt 0) {
    New-Item -ItemType Directory -Path "$root\cleanup_backups\scan_artifacts" -Force | Out-Null
    $dest = "$root\cleanup_backups\scan_artifacts"
    foreach ($f in $found) {
        Move-Item -LiteralPath $f.FullName -Destination $dest -Force
    }
    $zip = "$root\cleanup_backups\scan_artifacts_$(Get-Date -Format yyyyMMddHHmmss).zip"
    Compress-Archive -Path "$dest\*" -DestinationPath $zip -Force
    # Remove moved files (keep only the zip)
    Get-ChildItem -Path $dest -File | Where-Object { $_.FullName -ne $zip } | Remove-Item -Force
    Write-Output "Archived to: $zip"
} else {
    Write-Output "No scan artifacts found."
}
