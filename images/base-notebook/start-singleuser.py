#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shlex
import sys

# Entrypoint is start.sh
command = ["jupyterhub-singleuser"]

# set default ip to 0.0.0.0
if "--ip=" not in os.environ.get("NOTEBOOK_ARGS", ""):
    command.append("--ip=0.0.0.0")

# Append any optional NOTEBOOK_ARGS we were passed in.
# This is supposed to be multiple args passed on to the notebook command,
# so we split it correctly with shlex
if "NOTEBOOK_ARGS" in os.environ:
    command += shlex.split(os.environ["NOTEBOOK_ARGS"])

# Pass any other args we have been passed through
command += sys.argv[1:]

# Execute the command!
print("Executing: " + " ".join(command))
os.execvp(command[0], command)
