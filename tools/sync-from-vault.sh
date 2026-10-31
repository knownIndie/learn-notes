#!/bin/sh
# The notes live in the Obsidian vault. This copies them into content/,
# applies the reading order (series.py), and builds the site to check it.
# Publishing = run this, then commit and push (only when the user says so).
set -e
VAULT_NOTES="/Users/ana/obsidian/learn-notes/"
cd "$(dirname "$0")/.."
rsync -a --delete --exclude '.DS_Store' "$VAULT_NOTES" content/
python3 tools/series.py
npx quartz build
