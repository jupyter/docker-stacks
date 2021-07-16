# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os


def github_set_env(env_name, env_value):
    if not os.environ.get("GITHUB_ACTIONS") or not os.environ.get("GITHUB_ENV"):
        return

    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"{env_name}={env_value}\n")
