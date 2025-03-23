#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shlex
import sys

# Entrypoint is start.sh
command = ["jupyterhub-singleuser"]

# JupyterHub singleuser arguments are set using environment variables

# Append any optional NOTEBOOK_ARGS we were passed in.
# This is supposed to be multiple args passed on to the notebook command,
# so we split it correctly with shlex
if "NOTEBOOK_ARGS" in os.environ:
    command += shlex.split(os.environ["NOTEBOOK_ARGS"])

# Pass any other args we have been passed through
command += sys.argv[1:]

# Execute the command!
print("Executing: " + " ".join(command), flush=True)
os.execvp(command[0], command)
