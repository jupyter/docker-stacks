#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging

import plumbum

from .docker_runner import DockerRunner
from .get_taggers_and_manifests import get_taggers_and_manifests
from .github_set_env import github_set_env

docker = plumbum.local["docker"]

LOGGER = logging.getLogger(__name__)


def tag_image(short_image_name: str, owner: str) -> None:
    """
    Tags <owner>/<short_image_name>:latest with the tags reported by all taggers
    for the given image.

    Tags are in a GitHub Actions environment also saved to environment variables
    in a format making it easy to append them.
    """
    LOGGER.info(f"Tagging image: {short_image_name}")
    taggers, _ = get_taggers_and_manifests(short_image_name)

    image = f"{owner}/{short_image_name}:latest"

    with DockerRunner(image) as container:
        tags = []
        for tagger in taggers:
            tagger_name = tagger.__class__.__name__
            tag_value = tagger.tag_value(container)
            tags.append(tag_value)
            LOGGER.info(
                f"Applying tag, tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            docker["tag", image, f"{owner}/{short_image_name}:{tag_value}"]()

        if tags:
            env_name = f'{short_image_name.replace("-", "_")}_EXTRA_TAG_ARGS'
            docker_build_tag_args = " ".join(
                [f"-t {owner}/{short_image_name}:{tag}" for tag in tags]
            )
            github_set_env(env_name, docker_build_tag_args)


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
