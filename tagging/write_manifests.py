#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import datetime
import logging
from pathlib import Path

from docker.models.containers import Container

from tagging.docker_runner import DockerRunner
from tagging.get_taggers_and_manifests import get_taggers_and_manifests
from tagging.git_helper import GitHelper
from tagging.manifests import ManifestHeader, ManifestInterface
from tagging.tags_prefix import get_tags_prefix

LOGGER = logging.getLogger(__name__)


BUILD_TIMESTAMP = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def write_build_history_line(
    short_image_name: str,
    owner: str,
    manifest_filename: str,
    all_tags: list[str],
) -> None:
    LOGGER.info("Appending build history line")

    date_column = f"`{BUILD_TIMESTAMP}`"
    image_column = MARKDOWN_LINE_BREAK.join(
        f"`{owner}/{short_image_name}:{tag_value}`" for tag_value in all_tags
    )
    commit_hash = GitHelper.commit_hash()
    links_column = MARKDOWN_LINE_BREAK.join(
        [
            f"[Git diff](https://github.com/jupyter/docker-stacks/commit/{commit_hash})",
            f"[Dockerfile](https://github.com/jupyter/docker-stacks/blob/{commit_hash}/{short_image_name}/Dockerfile)",
            f"[Build manifest](./{manifest_filename.removesuffix('.md')})",
        ]
    )
    build_history_line = "|".join([date_column, image_column, links_column]) + "|"
    build_history_filename = manifest_filename.replace(".md", ".txt")
    Path(f"/tmp/build_history_lines/{build_history_filename}").write_text(
        build_history_line
    )


def write_manifest_file(
    short_image_name: str,
    owner: str,
    manifest_filename: str,
    manifests: list[ManifestInterface],
    container: Container,
) -> None:
    manifest_names = [manifest.__class__.__name__ for manifest in manifests]
    LOGGER.info(f"Using manifests: {manifest_names}")

    markdown_pieces = [
        ManifestHeader.create_header(short_image_name, owner, BUILD_TIMESTAMP)
    ] + [manifest.markdown_piece(container) for manifest in manifests]
    markdown_content = "\n\n".join(markdown_pieces) + "\n"

    Path(f"/tmp/manifests/{manifest_filename}").write_text(markdown_content)


def write_manifests(short_image_name: str, owner: str) -> None:
    LOGGER.info(f"Creating manifests for image: {short_image_name}")
    taggers, manifests = get_taggers_and_manifests(short_image_name)

    image = f"{owner}/{short_image_name}:latest"

    tags_prefix = get_tags_prefix()
    commit_hash_tag = GitHelper.commit_hash_tag()
    filename = f"{tags_prefix}{short_image_name}-{commit_hash_tag}.md"
    manifest_filename = f"{filename}.md"

    with DockerRunner(image) as container:
        all_tags = [tags_prefix + tagger.tag_value(container) for tagger in taggers]
        write_build_history_line(short_image_name, owner, manifest_filename, all_tags)
        write_manifest_file(
            short_image_name, owner, manifest_filename, manifests, container
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name to create manifests for",
    )
    arg_parser.add_argument("--owner", default="jupyter", help="Owner of the image")
    args = arg_parser.parse_args()

    LOGGER.info(f"Current build timestamp: {BUILD_TIMESTAMP}")

    write_manifests(args.short_image_name, args.owner)
