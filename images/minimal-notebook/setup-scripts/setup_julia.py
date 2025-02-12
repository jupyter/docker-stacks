#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Requirements:
# - Run as the root user
# - The JULIA_PKGDIR environment variable is set

import logging
import os
import platform
import shutil
import subprocess
from pathlib import Path

import requests

LOGGER = logging.getLogger(__name__)


def unify_aarch64(platform: str) -> str:
    """
    Renames arm64->aarch64 to support local builds on aarch64 Macs
    """
    return {"arm64": "aarch64"}.get(platform, platform)


def get_latest_julia_url() -> tuple[str, str]:
    """
    Get the last stable version of Julia
    Based on: https://github.com/JuliaLang/www.julialang.org/issues/878#issuecomment-749234813
    """
    LOGGER.info("Downloading Julia versions information")
    versions = requests.get(
        "https://julialang-s3.julialang.org/bin/versions.json"
    ).json()
    stable_versions = {k: v for k, v in versions.items() if v["stable"]}
    # Compare versions semantically
    latest_stable_version = max(
        stable_versions, key=lambda ver: [int(sub_ver) for sub_ver in ver.split(".")]
    )
    latest_version_files = stable_versions[latest_stable_version]["files"]
    triplet = unify_aarch64(platform.machine()) + "-linux-gnu"
    file_info = [vf for vf in latest_version_files if vf["triplet"] == triplet][0]
    LOGGER.info(f"Latest version: {file_info['version']} url: {file_info['url']}")
    return file_info["url"], file_info["version"]


def download_julia(julia_url: str) -> None:
    """
    Downloads and unpacks julia
    The resulting julia directory is "/opt/julia-VERSION/"
    """
    LOGGER.info("Downloading and unpacking Julia")
    tmp_file = Path("/tmp/julia.tar.gz")
    subprocess.check_call(
        ["curl", "--progress-bar", "--location", "--output", tmp_file, julia_url]
    )
    shutil.unpack_archive(tmp_file, "/opt/")
    tmp_file.unlink()


def configure_julia(julia_version: str) -> None:
    """
    Creates /usr/local/bin/julia symlink
    Make Julia aware of conda libraries
    Creates a directory for Julia user libraries
    """
    LOGGER.info("Configuring Julia")
    # Link Julia installed version to /usr/local/bin, so julia launches it
    subprocess.check_call(
        ["ln", "-fs", f"/opt/julia-{julia_version}/bin/julia", "/usr/local/bin/julia"]
    )

    # Tell Julia where conda libraries are
    Path("/etc/julia").mkdir()
    Path("/etc/julia/juliarc.jl").write_text(
        f'push!(Libdl.DL_LOAD_PATH, "{os.environ["CONDA_DIR"]}/lib")\n'
    )

    # Create JULIA_PKGDIR, where user libraries are installed
    JULIA_PKGDIR = Path(os.environ["JULIA_PKGDIR"])
    JULIA_PKGDIR.mkdir()
    subprocess.check_call(["chown", os.environ["NB_USER"], JULIA_PKGDIR])
    subprocess.check_call(["fix-permissions", JULIA_PKGDIR])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    julia_url, julia_version = get_latest_julia_url()
    download_julia(julia_url=julia_url)
    configure_julia(julia_version=julia_version)
