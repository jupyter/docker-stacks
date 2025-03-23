# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
from pathlib import Path

from tagging.apps.config import Config
from tagging.utils.get_platform import unify_aarch64


def common_arguments_parser(
    *,
    registry: bool = False,
    owner: bool = False,
    image: bool = False,
    variant: bool = False,
    platform: bool = False,
    tags_dir: bool = False,
    hist_lines_dir: bool = False,
    manifests_dir: bool = False,
    repository: bool = False,
) -> Config:
    """Add common CLI arguments to parser"""

    parser = argparse.ArgumentParser()
    if registry:
        parser.add_argument(
            "--registry",
            required=True,
            choices=["docker.io", "quay.io"],
            help="Image registry",
        )
    if owner:
        parser.add_argument(
            "--owner",
            required=True,
            help="Owner of the image",
        )
    if image:
        parser.add_argument(
            "--image",
            required=True,
            help="Short image name",
        )
    if variant:
        parser.add_argument(
            "--variant",
            required=True,
            help="Variant tag prefix",
        )
    if platform:
        parser.add_argument(
            "--platform",
            required=True,
            type=str,
            choices=["x86_64", "aarch64", "arm64"],
            help="Image platform",
        )
    if tags_dir:
        parser.add_argument(
            "--tags-dir",
            required=True,
            type=Path,
            help="Directory for tags file",
        )
    if hist_lines_dir:
        parser.add_argument(
            "--hist-lines-dir",
            required=True,
            type=Path,
            help="Directory for hist_lines file",
        )
    if manifests_dir:
        parser.add_argument(
            "--manifests-dir",
            required=True,
            type=Path,
            help="Directory for manifests file",
        )
    if repository:
        parser.add_argument(
            "--repository",
            required=True,
            help="Repository name on GitHub",
        )
    args = parser.parse_args()
    if platform:
        args.platform = unify_aarch64(args.platform)

    return Config(**vars(args))
