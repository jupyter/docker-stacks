# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
from pathlib import Path


def common_arguments_parser(
    *,
    registry: bool = False,
    owner: bool = False,
    short_image_name: bool = False,
    variant: bool = False,
    tags_dir: bool = False,
    hist_lines_dir: bool = False,
    manifests_dir: bool = False,
) -> argparse.ArgumentParser:
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
    if short_image_name:
        parser.add_argument(
            "--short-image-name",
            required=True,
            help="Short image name",
        )
    if variant:
        parser.add_argument(
            "--variant",
            required=True,
            help="Variant tag prefix",
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

    return parser
