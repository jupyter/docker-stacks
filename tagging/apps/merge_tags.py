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


def read_local_tags_from_files(config: Config) -> tuple[list[str], set[str]]:
    LOGGER.info(f"Read tags from file(s) for image: {config.image}")

    all_local_tags = []
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
            all_local_tags.append(tag)
            merged_local_tags.add(tag.replace(platform + "-", ""))

    LOGGER.info(f"Tags read for image: {config.image}")
    return all_local_tags, merged_local_tags


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4))
def pull_tag(tag: str) -> None:
    LOGGER.info(f"Pulling tag: {tag}")
    docker["pull", tag] & plumbum.FG
    LOGGER.info(f"Tag {tag} pulled successfully")


def pull_missing_tags(merged_tag: str, all_local_tags: list[str]) -> list[str]:
    existing_platform_tags = []

    for platform in ALL_PLATFORMS:
        platform_tag = merged_tag.replace(":", f":{platform}-")
        if platform_tag in all_local_tags:
            LOGGER.info(
                f"Tag {platform_tag} already exists locally, not pulling it from registry"
            )
            existing_platform_tags.append(platform_tag)
            continue

        LOGGER.warning(f"Trying to pull: {platform_tag} from registry")
        try:
            pull_tag(platform_tag)
            existing_platform_tags.append(platform_tag)
            LOGGER.info(f"Tag {platform_tag} pulled successfully")
        except RetryError:
            LOGGER.warning(f"Pull failed, tag {platform_tag} doesn't exist")

    return existing_platform_tags


def merge_tags(
    merged_tag: str, all_local_tags: list[str], push_to_registry: bool
) -> None:
    LOGGER.info(f"Trying to merge tag: {merged_tag}")

    existing_platform_tags = pull_missing_tags(merged_tag, all_local_tags)
    args = [
        "buildx",
        "imagetools",
        "create",
        *existing_platform_tags,
        "--tag",
        merged_tag,
    ]
    if not push_to_registry:
        args.append("--dry-run")

    LOGGER.info(f"Running command: {' '.join(args)}")
    docker[args] & plumbum.FG
    if push_to_registry:
        LOGGER.info(f"Pushed merged tag: {merged_tag} to registry")
    else:
        LOGGER.info(f"Skipping push for tag: {merged_tag}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(image=True, variant=True, tags_dir=True)
    push_to_registry = os.environ.get("PUSH_TO_REGISTRY", "false").lower() == "true"

    LOGGER.info(f"Merging tags for image: {config.image}")

    all_local_tags, merged_local_tags = read_local_tags_from_files(config)
    for tag in merged_local_tags:
        merge_tags(tag, all_local_tags, push_to_registry)

    LOGGER.info(f"Successfully merged tags for image: {config.image}")
