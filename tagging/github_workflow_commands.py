"""
GitHub Workflow Commands (gwc) for GitHub Actions can help us pass information
from a Workflow's Job's various build steps to others via "output" and improve
the presented logs when viewed via the GitHub web based UI.

Reference: https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions

Workflow commands relies on emitting messages:

    print("::{command name} parameter1={data},parameter2={data}::{command value}")

The functions defined in this file will only emit such messages if found to be
in a GitHub CI environment.
"""

import json
import os


def _gwc(command_name, command_value="", **params):
    if not os.environ.get("GITHUB_ACTIONS"):
        return

    # Assume non-string values are meant to be dumped as JSON
    if not isinstance(command_value, str):
        command_value = json.dumps(command_value)
        print(f"dumped json: {command_value}")

    if params:
        comma_sep_params = ",".join([f"{k}={v}" for k, v in params.items()])
        print(f"::{command_name} {comma_sep_params}::{command_value}")
    else:
        print(f"::{command_name}::{command_value}")


def _gwc_set_env(env_name, env_value):
    if not os.environ.get("GITHUB_ACTIONS") or not os.environ.get("GITHUB_ENV"):
        return

    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"{env_name}={env_value}\n")
