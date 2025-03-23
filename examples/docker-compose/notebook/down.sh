#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Setup environment
# shellcheck source=examples/docker-compose/notebook/env.sh
source "${DIR}/env.sh"

# Bring down the notebook container, using container name as project name
docker-compose -f "${DIR}/notebook.yml" -p "${NAME}" down
