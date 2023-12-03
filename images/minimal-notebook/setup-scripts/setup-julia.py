#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Requirements:
# - Run as the root user
# - The JULIA_PKGDIR environment variable is set

import os
import platform
import shutil
from pathlib import Path

import plumbum
import requests

curl = plumbum.local["curl"]
ln = plumbum.local["ln"]
chown = plumbum.local["chown"]
fix_permissions = plumbum.local["fix-permissions"]


def unify_aarch64(platform: str) -> str:
    return {
        "aarch64": "aarch64",
        "arm64": "aarch64",  # To support local building on aarch64 Macs
        "x86_64": "x86_64",
    }[platform]


def get_latest_julia_url() -> tuple[str, str]:
    # Get the last stable version of Julia
    # https://github.com/JuliaLang/www.julialang.org/issues/878#issuecomment-749234813

    versions = requests.get(
        "https://julialang-s3.julialang.org/bin/versions.json"
    ).json()
    stable_versions = {k: v for k, v in versions.items() if v["stable"]}
    latest_version_files = stable_versions[max(stable_versions)]["files"]
    triplet = unify_aarch64(platform.machine()) + "-linux-gnu"
    file_info = [vf for vf in latest_version_files if vf["triplet"] == triplet][0]
    return file_info["url"], file_info["version"]


def download_julia(julia_url: str) -> None:
    tmp_file = Path("/tmp/julia.tar.gz")
    curl["--progress-bar", "--location", "--output", tmp_file, julia_url] & plumbum.FG
    shutil.unpack_archive(tmp_file, "/opt/")
    tmp_file.unlink()


def prepare_julia(julia_version: str) -> None:
    # Link Julia installed version to /usr/local/bin, so julia launches it
    (
        ln["-fs", f"/opt/julia-{julia_version}/bin/julia", "/usr/local/bin/julia"]
        & plumbum.FG
    )

    # Tell Julia where conda libraries are
    Path("/etc/julia").mkdir()
    Path("/etc/julia/juliarc.jl").write_text(
        f'push!(Libdl.DL_LOAD_PATH, "{os.environ["CONDA_DIR"]}/lib")\n'
    )

    # Create JULIA_PKGDIR, where user libraries are installed
    JULIA_PKGDIR = Path(os.environ["JULIA_PKGDIR"])
    JULIA_PKGDIR.mkdir()
    chown[os.environ["NB_USER"], JULIA_PKGDIR] & plumbum.FG
    fix_permissions[JULIA_PKGDIR] & plumbum.FG


if __name__ == "__main__":
    julia_url, julia_version = get_latest_julia_url()
    download_julia(julia_url=julia_url)
    prepare_julia(julia_version=julia_version)
