#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.hierarchy.get_taggers_and_manifests import (
    get_taggers_and_manifests,
)
from tagging.utils.config import Config
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix

LOGGER = logging.getLogger(__name__)


def write_tags_file(config: Config) -> None:
    """
    Writes tags file for the image {config.full_image()}
    """
    LOGGER.info(f"Tagging image: {config.image}")
    taggers, _ = get_taggers_and_manifests(config.image)

    file_prefix = get_file_prefix(config.variant)
    filename = f"{file_prefix}-{config.image}.txt"

    tags_prefix = get_tag_prefix(config.variant)
    tags = [f"{config.full_image()}:{tags_prefix}-latest"]
    with DockerRunner(config.full_image()) as container:
        for tagger in taggers:
            tagger_name = tagger.__class__.__name__
            tag_value = tagger.tag_value(container)
            LOGGER.info(
                f"Calculated tag, tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            tags.append(f"{config.full_image()}:{tags_prefix}-{tag_value}")
    config.tags_dir.mkdir(parents=True, exist_ok=True)
    file = config.tags_dir / filename
    file.write_text("\n".join(tags))
    LOGGER.info(f"Tags file written to: {file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(
        registry=True, owner=True, image=True, variant=True, tags_dir=True
    )
    write_tags_file(config)
