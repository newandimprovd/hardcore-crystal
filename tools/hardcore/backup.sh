#!/bin/bash
# Snapshot the working tree into the user's GitHub repo (newandimprovd/hardcore-crystal) and push.
# usage: backup.sh "commit message" [path-to-rom-to-include]
# Never pushes to pret. The pokecrystal working repo has no remote on purpose.
set -e
SRC=/home/claude/pokecrystal
DST=/home/claude/hardcore-crystal
MSG=${1:?commit message}
ROM=${2:-}
BR=claude/work
cd "$DST"
git fetch -q origin 2>/dev/null || true
if git show-ref -q --verify refs/heads/$BR; then git checkout -q $BR; else
  if git show-ref -q --verify refs/remotes/origin/$BR; then git checkout -q -b $BR origin/$BR; else git checkout -q -b $BR origin/main; fi
fi
# replace working files with the current tree (tracked + untracked, minus ignored build output)
find . -mindepth 1 -maxdepth 1 ! -name .git ! -name releases -exec rm -rf {} +
( cd "$SRC" && git ls-files -co --exclude-standard -z | tar --null -T - -cf - ) | tar -xf -
if [ -n "$ROM" ] && [ -f "$ROM" ]; then
  mkdir -p releases; cp "$ROM" releases/; [ -f "${ROM%.gbc}.sym" ] && cp "${ROM%.gbc}.sym" releases/ || true
fi
git add -A
git add -f releases 2>/dev/null || true
if git diff --cached --quiet; then echo "backup: nothing to commit"; else
  git commit -q -m "$MSG

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01725Um4e2odPdkDFwv4XM8D"
fi
git push -q -u origin $BR 2>&1 | grep -v "^remote:" || true
echo "backup: $(git rev-parse --short HEAD) on origin/$BR ($(git ls-remote origin refs/heads/$BR | cut -c1-7))"
