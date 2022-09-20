# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import platform

ALL_TAGS_PREFIXES = {"x86_64", "aarch64"}


def get_tags_prefix() -> str:
    return platform.machine()
