#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
from pathlib import Path

import plumbum

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def apply_tags(
    short_image_name: str,
    owner: str,
    tags_dir: Path,
    platform: str,
) -> None:
    """
    Tags <owner>/<short_image_name>:latest with the tags
    reported by all taggers for the given image.
    """
    LOGGER.info(f"Tagging image: {short_image_name}")

    image = f"{owner}/{short_image_name}:latest"
    filename = f"{platform}-{short_image_name}.txt"
    tags = (tags_dir / filename).read_text().splitlines()

    for tag in tags:
        LOGGER.info(f"Applying tag: {tag}")
        docker["tag", image, tag] & plumbum.FG

    LOGGER.info("Removing latest tag from the image")
    docker["image", "rmi", image] & plumbum.FG


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name to apply tags for",
    )
    arg_parser.add_argument(
        "--tags-dir",
        required=True,
        type=Path,
        help="Directory with saved tags file",
    )
    arg_parser.add_argument(
        "--platform",
        required=True,
        type=str,
        choices=["x86_64", "aarch64"],
        help="Image platform",
    )
    arg_parser.add_argument(
        "--owner",
        required=True,
        help="Owner of the image",
    )
    args = arg_parser.parse_args()

    apply_tags(args.short_image_name, args.owner, args.tags_dir, args.platform)
