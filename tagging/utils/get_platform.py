# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import platform

# Tuple (and not set) to guarantee a deterministic iteration order
ALL_PLATFORMS = ("aarch64", "x86_64")


def unify_aarch64(platform: str) -> str:
    """
    Renames arm64->aarch64 to support local builds on aarch64 Macs
    """
    return {"arm64": "aarch64"}.get(platform, platform)


def get_platform() -> str:
    machine = platform.machine()
    return unify_aarch64(machine)
