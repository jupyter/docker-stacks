#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging
from pathlib import Path

from tagging.docker_runner import DockerRunner
from tagging.get_platform import get_platform
from tagging.get_taggers_and_manifests import get_taggers_and_manifests

LOGGER = logging.getLogger(__name__)


def write_tags_file(
    short_image_name: str,
    registry: str,
    owner: str,
    tags_dir: Path,
) -> None:
    """
    Writes tags file for the image <registry>/<owner>/<short_image_name>:latest
    """
    LOGGER.info(f"Tagging image: {short_image_name}")
    taggers, _ = get_taggers_and_manifests(short_image_name)

    image = f"{registry}/{owner}/{short_image_name}:latest"
    tags_prefix = get_platform()
    filename = f"{tags_prefix}-{short_image_name}.txt"

    tags = [f"{registry}/{owner}/{short_image_name}:{tags_prefix}-latest"]
    with DockerRunner(image) as container:
        for tagger in taggers:
            tagger_name = tagger.__class__.__name__
            tag_value = tagger.tag_value(container)
            LOGGER.info(
                f"Calculated tag, tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            tags.append(
                f"{registry}/{owner}/{short_image_name}:{tags_prefix}-{tag_value}"
            )
    tags_dir.mkdir(parents=True, exist_ok=True)
    (tags_dir / filename).write_text("\n".join(tags))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name to write tags for",
    )
    arg_parser.add_argument(
        "--tags-dir",
        required=True,
        type=Path,
        help="Directory to save tags file",
    )
    arg_parser.add_argument(
        "--registry",
        required=True,
        type=str,
        choices=["docker.io", "quay.io"],
        help="Image registry",
    )
    arg_parser.add_argument(
        "--owner",
        required=True,
        help="Owner of the image",
    )
    args = arg_parser.parse_args()

    write_tags_file(args.short_image_name, args.registry, args.owner, args.tags_dir)
