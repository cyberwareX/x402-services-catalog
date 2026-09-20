#!/bin/bash
# Re-snapshot the live machine catalog and rebuild README.md. The site is the source of truth.
set -e
cd "$(dirname "$0")"
for f in agents.json services.json llms.txt; do curl -s "https://cyberwarex.com/$f" -o "$f"; done
curl -s "https://cyberwarex.com/.well-known/x402" -o well-known-x402.json
python3 build_readme.py
