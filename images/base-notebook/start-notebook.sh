#!/bin/bash
# Shim to emit warning and call start-notebook.py
echo "WARNING: Use start-notebook.py instead"

exec /usr/local/bin/start-notebook.py "$@"
