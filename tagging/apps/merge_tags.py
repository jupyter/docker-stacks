#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import plumbum

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.utils.config import Config
from tagging.utils.get_platform import ALL_PLATFORMS
from tagging.utils.get_prefix import get_file_prefix_for_platform

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def read_tags_from_files(config: Config) -> set[str]:
    LOGGER.info(f"Read tags from file(s) for image: {config.image}")

    tags: set[str] = set()
    for platform in ALL_PLATFORMS:
        LOGGER.info(f"Reading tags for platform: {platform}")

        file_prefix = get_file_prefix_for_platform(platform, config.variant)
        filename = f"{file_prefix}-{config.image}.txt"
        path = config.tags_dir / filename
        if path.exists():
            LOGGER.info(f"Tag file: {path} found")
            lines = path.read_text().splitlines()
            tags.update(tag.replace(platform + "-", "") for tag in lines)
        else:
            LOGGER.info(f"Tag file: {path} doesn't exist")

    LOGGER.info(f"Tags read for image: {config.image}")
    return tags


def merge_tags(config: Config) -> None:
    LOGGER.info(f"Merging tags for image: {config.image}")

    all_tags = read_tags_from_files(config)
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

        LOGGER.info(f"Successfully merged and pushed tag: {tag}")

    LOGGER.info(f"All tags merged for image: {config.image}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(image=True, variant=True, tags_dir=True)
    merge_tags(config)
