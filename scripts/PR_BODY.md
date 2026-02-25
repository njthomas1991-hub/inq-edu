Title: chore: add branch-migration helper scripts

Body:
This PR adds conservative helper scripts to assist contributors in migrating
local branches after the repository history was rewritten to remove
sensitive files. The scripts are dry-run by default and will only execute
destructive operations if run with an explicit flag.

Files added:
- `scripts/fix_local_branches.ps1` — PowerShell helper for Windows users.
- `scripts/fix_local_branches.sh` — POSIX shell helper for macOS/Linux.

Usage and guidelines are documented in each script. These helpers:
- fetch `origin` and list local branches that diverge from their remotes.
- recommend safe commands to create a `backup/<branch>` and rebase onto `origin/master`.
- provide an `--apply` / `-Apply` option to execute the recommended actions (creates backup branches first).

Please review before merging. I can also open the GitHub PR if you'd like — I just need permission or a token to create the PR automatically.
