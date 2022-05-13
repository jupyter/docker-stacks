# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import platform


def get_tags_prefix() -> str:
    machine = platform.machine()
    return "" if machine == "x86_64" else f"{machine}-"
