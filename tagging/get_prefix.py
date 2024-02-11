# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.get_platform import get_platform

DEFAULT_VARIANT = "default"


def get_file_prefix_for_platform(platform: str, variant: str) -> str:
    return f"{platform}-{variant}"


def get_tag_prefix_for_platform(platform: str, variant: str) -> str:
    if variant == DEFAULT_VARIANT:
        return platform
    return f"{platform}-{variant}"


def get_file_prefix(variant: str) -> str:
    platform = get_platform()
    return get_file_prefix_for_platform(platform, variant)


def get_tag_prefix(variant: str) -> str:
    platform = get_platform()
    return get_tag_prefix_for_platform(platform, variant)
