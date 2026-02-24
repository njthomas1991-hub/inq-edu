<#
PowerShell helper: inspect local branches after a force-push history rewrite

Usage:
  .\fix_local_branches.ps1       # dry-run: lists divergent branches and shows recommended commands
  .\fix_local_branches.ps1 -Apply # actually apply the safe migration for each branch (creates backups)

This script is conservative: by default it prints commands users should run. With
`-Apply` it will create a backup branch `backup/<branch>` and rebase the branch
onto `origin/master` using a merge-base strategy.
#>

param(
    [switch]$Apply
)

function Run($cmd) { Write-Host "> $cmd"; if ($Apply) { iex $cmd } }

Write-Host "Fetching origin..."
git fetch --all

$localBranches = git for-each-ref --format='%(refname:short)' refs/heads/ | Where-Object { $_ -ne 'master' -and $_ -ne 'main' }
if (-not $localBranches) { Write-Host "No local branches found."; exit 0 }

foreach ($b in $localBranches) {
    $remoteExists = git ls-remote --heads origin $b | Out-String
    if ($remoteExists -ne '') {
        # Compare local branch with origin/<branch>
        $ahead = git rev-list --count origin/$b..$b
        $behind = git rev-list --count $b..origin/$b
        if ($ahead -eq 0 -and $behind -eq 0) {
            Write-Host "Branch $b is up-to-date with origin/$b. Skipping."
            continue
        }
        Write-Host "Branch: $b  (ahead: $ahead, behind: $behind)"
        $backup = "backup/$b"
        $rebaseCmd = "git checkout $b; git branch -f $backup $b; git fetch origin; git rebase --onto origin/master $(git merge-base origin/master $b) $b"
        Write-Host "Recommended: create local backup branch '$backup' then rebase onto origin/master"
        Run $rebaseCmd
        Write-Host "---"
    } else {
        Write-Host "Branch $b has no matching remote branch; consider creating a fresh branch from origin/master and cherry-pick commits if needed."
    }
}

Write-Host "Done. Dry-run mode: $([bool]$Apply). If you ran with -Apply the commands were executed." 
