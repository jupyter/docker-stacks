#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

# Initialize the TENSORBOARD_PROXY_URL with the appropriate path
# to use jupyter-server-proxy.

export TENSORBOARD_PROXY_URL="${JUPYTERHUB_SERVICE_PREFIX:-/}proxy/%PORT%/"
