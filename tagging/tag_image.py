#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
from plumbum.cmd import docker
from .docker_runner import DockerRunner
from .get_taggers_and_manifests import get_taggers_and_manifests


logger = logging.getLogger(__name__)


def tag_image(short_image_name: str, owner: str) -> None:
    logger.info(f"Tagging image: {short_image_name}")
    taggers, _ = get_taggers_and_manifests(short_image_name)

    image = f"{owner}/{short_image_name}:latest"

    with DockerRunner(image) as container:
        for tagger in taggers:
            tagger_name = tagger.__name__
            tag_value = tagger.tag_value(container)
            logger.info(
                f"Applying tag tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            docker["tag", image, f"{owner}/{short_image_name}:{tag_value}"]()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name to apply tags for",
    )
    arg_parser.add_argument("--owner", required=True, help="Owner of the image")
    args = arg_parser.parse_args()

    tag_image(args.short_image_name, args.owner)
