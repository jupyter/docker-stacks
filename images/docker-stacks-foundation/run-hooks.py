#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import json

# The run-hooks.py script looks for *.sh scripts to source
# and executable files to run within a passed directory
import os
import subprocess
import sys
import tempfile
from pathlib import PosixPath
from textwrap import dedent


def source(path: PosixPath):
    """
    Emulate the bash `source` command accurately

    When used in bash, `source` executes the passed file in the current 'context'
    of the script from where it is called. This primarily deals with how
    bash (and thus environment variables) are modified.

    1. Any bash variables (particularly any set via `export`) are passed on to the
       sourced script as their values are at the point source is called
    2. The sourced script can itself use `export` to affect the bash variables of the
       parent script that called it.

    (2) is the primary difference between `source` and just calling a shell script,
    and makes it possible for a set of scripts running in sequence to share data by
    passing bash variables across with `export`.

    Given bash variables are environment variables, we will simply look for all modified
    environment variables in the script we have sourced, and update the calling python
    script's environment variables to match.

    Args:
        path (PosixPath): Valid bash script to source
    """
    # We start a bash process and have it `source` the script we are given. Then, we
    # use python (for convenience) to dump the environment variables from the bash process into
    # json (we could use `env` but then handling multiline variable values becomes a nightmare).
    # The json is written to a temporary file we create. We read this json, and update our python
    # process' environment variable with whatever we get back from bash.
    with tempfile.NamedTemporaryFile() as bash_file, tempfile.NamedTemporaryFile() as py_file, tempfile.NamedTemporaryFile() as env_vars_file:
        py_file.write(
            dedent(
                f"""
                import os
                import json
                with(open("{env_vars_file.name}", "w")) as f:
                    json.dump(dict(os.environ), f)
                """
            ).encode()
        )
        py_file.flush()

        bash_file.write(
            dedent(
                f"""
                #!/bin/bash
                source {path}
                {sys.executable} {py_file.name}
                """
            ).encode()
        )
        bash_file.flush()

        run = subprocess.run(["/bin/bash", bash_file.name])

        if run.returncode != 0:
            print(
                f"{path} has failed with return code {run.returncode}, continuing execution"
            )
            return

        env_vars = json.load(env_vars_file)
        os.environ.update(env_vars)


if len(sys.argv) != 2:
    print("Should pass exactly one directory")
    sys.exit(1)

hooks_directory = PosixPath(sys.argv[1])

if not hooks_directory.exists():
    print(f"Directory {hooks_directory} does not exist")
    sys.exit(1)

if not hooks_directory.is_dir():
    print(f"{hooks_directory} is not a directory")
    sys.exit(1)

print(f"Running hooks in: {hooks_directory} as {os.getuid()} gid: {os.getgid()}")

for f in sorted(hooks_directory.iterdir()):
    if f.suffix == ".sh":
        print(f"Sourcing shell script: {f}")
        source(f)
    elif os.access(f, os.X_OK):
        print(f"Running executable: {f}")
        run = subprocess.run([str(f)])
        if run.returncode != 0:
            print(
                f"{f} has failed with return code {run.returncode}, continuing execution"
            )
    else:
        print(f"Ignoring non-executable: {f}")


print(f"Done running hooks in: {hooks_directory}")
