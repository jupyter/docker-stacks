#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import plumbum

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
from tagging.utils.get_prefix import get_file_prefix_for_platform

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def apply_tags(config: Config) -> None:
    LOGGER.info(f"Tagging image: {config.image}")

    file_prefix = get_file_prefix_for_platform(
        platform=config.platform, variant=config.variant
    )
    filename = f"{file_prefix}-{config.image}.txt"
    tags = (config.tags_dir / filename).read_text().splitlines()

    for tag in tags:
        LOGGER.info(f"Applying tag: {tag}")
        docker["tag", config.full_image(), tag] & plumbum.FG

    LOGGER.info(f"All tags applied to image: {config.image}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(
        registry=True,
        owner=True,
        image=True,
        variant=True,
        platform=True,
        tags_dir=True,
    )
    apply_tags(config)
