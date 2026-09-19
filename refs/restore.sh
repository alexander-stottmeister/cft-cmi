#!/bin/bash
# Restore the openly available source papers listed in refs/REFERENCES.md.
#   refs/restore.sh           list what would be fetched (default)
#   refs/restore.sh --fetch   download them via getref.sh
# Journal scans that are not openly available are reported as MANUAL.
set -u
cd "$(dirname "$0")"
MODE="${1:---list}"
ok=0; manual=0
while IFS= read -r line; do
  case "$line" in \|\ Short*|\|---*|"") continue;; \|*) ;; *) continue;; esac
  short=$(printf '%s' "$line" | awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}')
  src=$(printf '%s'  "$line" | awk -F'|' '{gsub(/^ +| +$/,"",$4); print $4}')
  [ -z "$short" ] && continue
  id=$(printf '%s' "$src" | grep -oE 'arXiv:[0-9]{4}\.[0-9]{4,5}|arXiv:[a-z-]+/[0-9]{7}' | head -1 | cut -d: -f2)
  url=$(printf '%s' "$src" | grep -oE 'https?://[^ ]+' | head -1)
  if [ -n "$id" ]; then
    ok=$((ok+1))
    if [ "$MODE" = "--fetch" ]; then ./getref.sh "$id" "$short"; else echo "arXiv   $short  ($id)"; fi
  elif [ -n "$url" ]; then
    ok=$((ok+1))
    if [ "$MODE" = "--fetch" ]; then ./getref.sh "$url" "$short"; else echo "open    $short  ($url)"; fi
  else
    manual=$((manual+1)); echo "MANUAL  $short  -- $src"
  fi
done < REFERENCES.md
echo "---"; echo "$ok fetchable, $manual need library access"
[ "$MODE" = "--list" ] && echo "run with --fetch to download"
exit 0
