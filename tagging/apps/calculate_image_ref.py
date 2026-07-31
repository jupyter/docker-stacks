#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import os

from tenacity import RetryError

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
from tagging.apps.merge_tags import read_local_tags_from_files
from tagging.utils.get_manifest_digest import ManifestNotFoundError, get_manifest_digest
from tagging.utils.get_prefix import get_file_prefix_for_platform

LOGGER = logging.getLogger(__name__)


def get_tag_to_sign(config: Config) -> str:
    """All tags of an image point to the same digest, so any tag can be signed.
    If the platform is not specified, choose one of the merged tags."""
    if config.platform:
        file_prefix = get_file_prefix_for_platform(
            platform=config.platform, variant=config.variant
        )
        filename = f"{file_prefix}-{config.image}.txt"
        return (config.tags_dir / filename).read_text().splitlines()[0]
    return next(iter(read_local_tags_from_files(config)))


def calculate_image_ref(config: Config, push_to_registry: bool) -> str | None:
    tag = get_tag_to_sign(config)
    try:
        digest = get_manifest_digest(tag)
    except (ManifestNotFoundError, RetryError):
        # The tag might not exist in the registry yet if the image is new
        if push_to_registry:
            raise
        LOGGER.warning(f"Failed to calculate digest for tag: {tag}")
        return None
    image = tag.rpartition(":")[0]
    return f"{image}@{digest}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(
        image=True, variant=True, platform_optional=True, tags_dir=True
    )
    push_to_registry = os.environ.get("PUSH_TO_REGISTRY", "false").lower() == "true"

    image_ref = calculate_image_ref(config, push_to_registry)
    if image_ref is not None:
        print(image_ref)
