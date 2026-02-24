#!/usr/bin/env bash
# POSIX helper: inspect local branches after a force-push history rewrite
# Usage:
#   ./fix_local_branches.sh       # dry-run: list divergent branches and show recommended commands
#   ./fix_local_branches.sh --apply # actually apply the safe migration (creates backups)

APPLY=0
if [ "$1" = "--apply" ]; then
  APPLY=1
fi

echo "Fetching origin..."
git fetch --all

for b in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  if [ "$b" = "master" ] || [ "$b" = "main" ]; then
    continue
  fi
  if git show-ref --verify --quiet refs/remotes/origin/$b; then
    ahead=$(git rev-list --count origin/$b..$b)
    behind=$(git rev-list --count $b..origin/$b)
    if [ "$ahead" -eq 0 ] && [ "$behind" -eq 0 ]; then
      echo "Branch $b is up-to-date with origin/$b. Skipping."
      continue
    fi
    echo "Branch: $b  (ahead: $ahead, behind: $behind)"
    backup="backup/$b"
    echo "Recommended: create backup branch '$backup' and rebase onto origin/master"
    echo "Commands:"
    echo "  git checkout $b"
    echo "  git branch -f $backup $b"
    echo "  git fetch origin"
    echo "  git rebase --onto origin/master \\$(git merge-base origin/master $b) $b"
    if [ $APPLY -eq 1 ]; then
      git checkout $b
      git branch -f $backup $b
      git fetch origin
      git rebase --onto origin/master $(git merge-base origin/master $b) $b
    fi
    echo "---"
  else
    echo "Branch $b has no matching remote branch; consider creating a fresh branch from origin/master and cherry-pick commits if needed."
  fi
done

echo "Done. APPLY=$APPLY"
