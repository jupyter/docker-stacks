#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
  echo "WARNING: use start-singleuser.sh instead of start-notebook.sh to start a server associated with JupyterHub."
  exec /usr/local/bin/start-singleuser.sh "$@"
  exit
fi

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
  wrapper="run-one-constantly"
fi

if [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
  exec /usr/local/bin/start.sh $wrapper $NOTEBOOK_ARGS jupyter lab "$@"
else
  exec /usr/local/bin/start.sh $wrapper $NOTEBOOK_ARGS jupyter notebook "$@"
fi
