#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os

import plumbum

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
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


def merge_tags(tag: str, push_to_registry: bool) -> None:
    LOGGER.info(f"Trying to merge tag: {tag}")
    all_platform_tags = []
    for platform in ALL_PLATFORMS:
        platform_tag = tag.replace(":", f":{platform}-")
        LOGGER.info(f"Trying to pull: {platform_tag}")
        try:
            docker["pull", platform_tag] & plumbum.FG
            all_platform_tags.append(platform_tag)
            LOGGER.info("Pull success")
        except plumbum.ProcessExecutionError:
            LOGGER.info("Pull failed, image with this tag and platform doesn't exist")

    LOGGER.info(f"Found images: {all_platform_tags}")
    try:
        docker["manifest", "rm", tag] & plumbum.FG
        LOGGER.info(f"Manifest {tag} already exists, removing it")
    except plumbum.ProcessExecutionError:
        LOGGER.info(f"Manifest {tag} doesn't exist")

    LOGGER.info(f"Creating manifest for tag: {tag}")
    docker["manifest", "create", tag][all_platform_tags] & plumbum.FG
    LOGGER.info(f"Successfully created manifest for tag: {tag}")

    if push_to_registry:
        LOGGER.info(f"Pushing manifest for tag: {tag}")
        docker["manifest", "push", tag] & plumbum.FG
        LOGGER.info(f"Successfully merged and pushed tag: {tag}")
    else:
        LOGGER.info(f"Skipping push for tag: {tag}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(image=True, variant=True, tags_dir=True)
    push_to_registry = os.environ.get("PUSH_TO_REGISTRY", "false").lower() == "true"

    LOGGER.info(f"Merging tags for image: {config.image}")
    all_tags = read_tags_from_files(config)
    for tag in all_tags:
        merge_tags(tag, push_to_registry)
    LOGGER.info(f"Successfully merged tags for image: {config.image}")
