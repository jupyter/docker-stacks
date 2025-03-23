#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shlex
import sys

# If we are in a JupyterHub, we pass on to `start-singleuser.py` instead so it does the right thing
if "JUPYTERHUB_API_TOKEN" in os.environ:
    print(
        "WARNING: using start-singleuser.py instead of start-notebook.py to start a server associated with JupyterHub.",
        flush=True,
    )
    command = ["/usr/local/bin/start-singleuser.py"] + sys.argv[1:]
    os.execvp(command[0], command)


# Entrypoint is start.sh
command = []

# If we want to survive restarts, launch the command using `run-one-constantly`
if os.environ.get("RESTARTABLE") == "yes":
    command.append("run-one-constantly")

# We always launch a jupyter subcommand from this script
command.append("jupyter")

# Launch the configured subcommand.
# Note that this should be a single string, so we don't split it.
# We default to `lab`.
jupyter_command = os.environ.get("DOCKER_STACKS_JUPYTER_CMD", "lab")
command.append(jupyter_command)

# Append any optional NOTEBOOK_ARGS we were passed in.
# This is supposed to be multiple args passed on to the notebook command,
# so we split it correctly with shlex
if "NOTEBOOK_ARGS" in os.environ:
    command += shlex.split(os.environ["NOTEBOOK_ARGS"])

# Pass through any other args we were passed on the command line
command += sys.argv[1:]

# Execute the command!
print("Executing: " + " ".join(command), flush=True)
os.execvp(command[0], command)
