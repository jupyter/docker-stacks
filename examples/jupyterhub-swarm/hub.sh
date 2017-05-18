#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Setup environment
source "$DIR/env.sh"

if [ -z "${GITHUB_CLIENT_ID:+x}" ]; then
  echo "ERROR: Must set GITHUB_CLIENT_ID environment variable"
  exit 1
fi

if [ -z "${GITHUB_CLIENT_SECRET:+x}" ]; then
  echo "ERROR: Must set GITHUB_CLIENT_SECRET environment variable"
  exit 1
fi

if [ -z "${OAUTH_CALLBACK_URL:+x}" ]; then
  echo "ERROR: Must set OAUTH_CALLBACK_URL environment variable"
  exit 1
fi

if [ -z "${SWARM_MANAGER:+x}" ]; then
  echo "ERROR: Must set SWARM_MANAGER environment variable"
  exit 1
fi

# Pass the DOCKER_HOST
DOCKER_HOST=$(docker-machine ip $SWARM_MANAGER):3376 \
  exec docker-compose -f jupyterhub.yml "$@"
