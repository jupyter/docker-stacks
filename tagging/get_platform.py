# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import platform

ALL_PLATFORMS = {"x86_64", "aarch64"}


def unify_aarch64(platform: str) -> str:
    return {
        "aarch64": "aarch64",
        "arm64": "aarch64",  # To support local building on aarch64 Macs
        "x86_64": "x86_64",
    }[platform]


def get_platform() -> str:
    machine = platform.machine()
    return unify_aarch64(machine)
