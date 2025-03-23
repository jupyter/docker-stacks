#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.apps.config import Config
from tagging.hierarchy.get_taggers import get_taggers
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix

LOGGER = logging.getLogger(__name__)


def get_tags(config: Config) -> list[str]:
    LOGGER.info(f"Calculating tags for image: {config.image}")

    taggers = get_taggers(config.image)
    tags_prefix = get_tag_prefix(config.variant)
    tags = [f"{config.full_image()}:{tags_prefix}-latest"]
    with DockerRunner(config.full_image()) as container:
        for tagger in taggers:
            tagger_name = tagger.__name__
            tag_value = tagger(container)
            LOGGER.info(
                f"Calculated tag, tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            tags.append(f"{config.full_image()}:{tags_prefix}-{tag_value}")

    LOGGER.info(f"Tags calculated for image: {config.image}")
    return tags


def write_tags_file(config: Config) -> None:
    LOGGER.info(f"Writing tags for image: {config.image}")

    file_prefix = get_file_prefix(config.variant)
    filename = f"{file_prefix}-{config.image}.txt"
    path = config.tags_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    tags = get_tags(config)
    path.write_text("\n".join(tags))

    LOGGER.info(f"Tags wrtitten to: {path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = common_arguments_parser(
        registry=True, owner=True, image=True, variant=True, tags_dir=True
    )
    write_tags_file(config)
