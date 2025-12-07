#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os

import plumbum
from tenacity import (  # type: ignore
    RetryError,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
from tagging.utils.get_platform import ALL_PLATFORMS
from tagging.utils.get_prefix import get_file_prefix_for_platform

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def read_local_tags_from_files(config: Config) -> set[str]:
    LOGGER.info(f"Read tags from file(s) for image: {config.image}")

    merged_local_tags = set()
    for platform in ALL_PLATFORMS:
        LOGGER.info(f"Reading tags for platform: {platform}")

        file_prefix = get_file_prefix_for_platform(
            platform=platform, variant=config.variant
        )
        filename = f"{file_prefix}-{config.image}.txt"
        path = config.tags_dir / filename
        if not path.exists():
            LOGGER.info(f"Tag file: {path} doesn't exist")
            continue

        LOGGER.info(f"Tag file: {path} found")
        for tag in path.read_text().splitlines():
            merged_local_tags.add(tag.replace(platform + "-", ""))

    LOGGER.info(f"Tags read for image: {config.image}")
    return merged_local_tags


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4))
def inspect_manifest(tag: str) -> None:
    LOGGER.info(f"Inspecting manifest for tag: {tag}")
    docker["buildx", "imagetools", "inspect", tag] & plumbum.FG
    LOGGER.info(f"Manifest {tag} exists")


def find_platform_tags(merged_tag: str) -> list[str]:
    platform_tags = []

    for platform in ALL_PLATFORMS:
        platform_tag = merged_tag.replace(":", f":{platform}-")
        LOGGER.warning(f"Trying to inspect: {platform_tag} in the registry")
        try:
            inspect_manifest(platform_tag)
            platform_tags.append(platform_tag)
            LOGGER.info(f"Tag {platform_tag} found successfully")
        except RetryError:
            LOGGER.warning(f"Manifest for tag {platform_tag} doesn't exist")

    return platform_tags


def merge_tags(merged_tag: str, push_to_registry: bool) -> None:
    LOGGER.info(f"Trying to merge tag: {merged_tag}")

    platform_tags = find_platform_tags(merged_tag)
    if not platform_tags:
        assert not push_to_registry, (
            f"No platform tags found for merged tag: {merged_tag}, "
            "and push to registry is enabled. "
            "Cannot create a manifest for a non-existing image."
        )
        LOGGER.info(
            f"Not running merge for tag: {merged_tag} as no platform tags found"
        )
        return

    args = [
        "buildx",
        "imagetools",
        "create",
        *platform_tags,
        "--tag",
        merged_tag,
    ]
    if not push_to_registry:
        args.append("--dry-run")

    LOGGER.info(f"Running command: {' '.join(args)}")
    docker[args] & plumbum.FG
    if push_to_registry:
        LOGGER.info(f"Pushed merged tag: {merged_tag}")
    else:
        LOGGER.info(f"Skipped push for tag: {merged_tag}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(image=True, variant=True, tags_dir=True)
    push_to_registry = os.environ.get("PUSH_TO_REGISTRY", "false").lower() == "true"

    LOGGER.info(f"Merging tags for image: {config.image}")

    merged_local_tags = read_local_tags_from_files(config)
    for tag in merged_local_tags:
        merge_tags(tag, push_to_registry)

    LOGGER.info(f"Successfully merged tags for image: {config.image}")
