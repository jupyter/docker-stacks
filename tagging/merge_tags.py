#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
from pathlib import Path

import plumbum

from tagging.get_platform import ALL_PLATFORMS

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def merge_tags(
    short_image_name: str,
    tags_dir: Path,
) -> None:
    """
    Merge tags for x86_64 and aarch64 images when possible.
    """
    LOGGER.info(f"Merging tags for image: {short_image_name}")

    all_tags: set[str] = set()

    for platform in ALL_PLATFORMS:
        filename = f"{platform}-{short_image_name}.txt"
        tags = (tags_dir / filename).read_text().splitlines()
        all_tags.update(tag.replace(platform + "-", "") for tag in tags)

    LOGGER.info(f"Got tags: {all_tags}")

    for tag in all_tags:
        LOGGER.info(f"Trying to merge tag: {tag}")
        existing_images = []
        for platform in ALL_PLATFORMS:
            image_with_platform = tag.replace(":", f":{platform}-")
            LOGGER.info(f"Trying to pull: {image_with_platform}")
            try:
                docker["pull", image_with_platform] & plumbum.FG
                existing_images.append(image_with_platform)
                LOGGER.info("Pull success")
            except plumbum.ProcessExecutionError:
                LOGGER.info(
                    "Pull failed, image with this tag and platform doesn't exist"
                )

        LOGGER.info(f"Found images: {existing_images}")
        docker["manifest", "create", tag][existing_images] & plumbum.FG
        docker["manifest", "push", tag] & plumbum.FG


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
    args = arg_parser.parse_args()

    merge_tags(args.short_image_name, args.tags_dir)
