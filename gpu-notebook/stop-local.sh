#!/usr/bin/env bash
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)

# Export default port to make compose file valid.
export JUPYTER_PORT=8888
docker-compose down
