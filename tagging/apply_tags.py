#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

import plumbum

from tagging.common_arguments import common_arguments_parser
from tagging.get_platform import unify_aarch64
from tagging.get_prefix import get_file_prefix_for_platform

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def apply_tags(
    *,
    registry: str,
    owner: str,
    short_image_name: str,
    variant: str,
    platform: str,
    tags_dir: Path,
) -> None:
    """
    Tags <registry>/<owner>/<short_image_name>:latest with the tags reported by all taggers for this image
    """
    LOGGER.info(f"Tagging image: {short_image_name}")

    file_prefix = get_file_prefix_for_platform(platform, variant)
    image = f"{registry}/{owner}/{short_image_name}:latest"
    filename = f"{file_prefix}-{short_image_name}.txt"
    tags = (tags_dir / filename).read_text().splitlines()

    for tag in tags:
        LOGGER.info(f"Applying tag: {tag}")
        docker["tag", image, tag] & plumbum.FG


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = common_arguments_parser()
    arg_parser.add_argument(
        "--platform",
        required=True,
        type=str,
        choices=["x86_64", "aarch64", "arm64"],
        help="Image platform",
    )
    arg_parser.add_argument(
        "--tags-dir",
        required=True,
        type=Path,
        help="Directory with saved tags file",
    )
    args = arg_parser.parse_args()
    args.platform = unify_aarch64(args.platform)

    apply_tags(**vars(args))
