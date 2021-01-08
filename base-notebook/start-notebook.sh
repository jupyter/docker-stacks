#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
    wrapper="run-one-constantly"
fi

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    # launched by JupyterHub, use single-user entrypoint
    exec /usr/local/bin/start-singleuser.sh "$@"
elif [[ ! -z "${JUPYTER_ENABLE_NB}" ]]; then
    echo "WARN: We encourage users to transition to JupyterLab, Notebook support could be removed"
    . /usr/local/bin/start.sh $wrapper jupyter notebook "$@"
else
    if [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
        echo "WARN: The JUPYTER_ENABLE_LAB environment variable is not required anymore"
    fi
    . /usr/local/bin/start.sh $wrapper jupyter lab "$@"
fi
