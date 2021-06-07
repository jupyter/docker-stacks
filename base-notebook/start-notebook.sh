#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
    wrapper="run-one-constantly"
fi

if [[ -n "${JUPYTERHUB_API_TOKEN}" ]]; then
    # launched by JupyterHub, use single-user entrypoint
    exec /usr/local/bin/start-singleuser.sh "$@"
elif [[ -n "${JUPYTER_ENABLE_LAB}" ]]; then
    # shellcheck disable=SC1091
    . /usr/local/bin/start.sh ${wrapper} jupyter lab "$@"
else
    echo "WARN: Jupyter Notebook deprecation notice https://github.com/jupyter/docker-stacks#jupyter-notebook-deprecation-notice."
    # shellcheck disable=SC1091
    . /usr/local/bin/start.sh ${wrapper} jupyter notebook "$@"
fi
