#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Setup environment
# shellcheck disable=SC1091
source "${DIR}/env.sh"

# Build the notebook image
docker-compose -f "${DIR}/notebook.yml" build
