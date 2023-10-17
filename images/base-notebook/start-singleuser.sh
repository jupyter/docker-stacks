#!/bin/bash
# Shim to emit warning and call start-singleuser.py
echo "WARNING: Use start-singleuser.py instead"

exec /usr/local/bin/start-singleuser.py "$@"
