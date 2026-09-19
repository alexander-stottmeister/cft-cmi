#!/bin/bash
# Usage: getref.sh <arxiv-id-or-URL> <shortname>   -> refs/<shortname>_<id>.pdf   (arXiv ids are fetched from arxiv.org/pdf)
set -e; cd "$(dirname "$0")"
ID="$1"; NAME="$2"
if [[ "$ID" == http* ]]; then URL="$ID"; OUT="${NAME}.pdf"; else URL="https://arxiv.org/pdf/${ID}"; OUT="${NAME}_${ID//\//-}.pdf"; fi
[ -s "$OUT" ] && { echo "exists: $OUT"; exit 0; }
curl -sL -A "Mozilla/5.0" -o "$OUT" "$URL" && file "$OUT" | grep -q PDF && echo "ok: $OUT" || { echo "FAILED: $URL"; rm -f "$OUT"; exit 1; }
