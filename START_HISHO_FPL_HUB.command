#!/bin/bash
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 20+ is required."
  exit 1
fi
[ -d node_modules ] || npm install
(sleep 2; open http://localhost:4173) &
npm start
