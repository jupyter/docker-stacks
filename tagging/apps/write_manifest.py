#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime
import logging

from docker.models.containers import Container

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.hierarchy.get_taggers_and_manifests import (
    get_taggers_and_manifests,
)
from tagging.manifests.header import ManifestHeader
from tagging.manifests.manifest_interface import ManifestInterface
from tagging.utils.config import Config
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix
from tagging.utils.git_helper import GitHelper

LOGGER = logging.getLogger(__name__)

# We use a manifest creation timestamp, which happens right after a build
BUILD_TIMESTAMP = datetime.datetime.now(datetime.UTC).isoformat()[:-13] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def write_build_history_line(
    config: Config, filename: str, all_tags: list[str]
) -> None:
    LOGGER.info("Appending build history line")

    date_column = f"`{BUILD_TIMESTAMP}`"
    image_column = MARKDOWN_LINE_BREAK.join(
        f"`{config.full_image()}:{tag_value}`" for tag_value in all_tags
    )
    commit_hash = GitHelper.commit_hash()
    links_column = MARKDOWN_LINE_BREAK.join(
        [
            f"[Git diff](https://github.com/{config.repository}/commit/{commit_hash})",
            f"[Dockerfile](https://github.com/{config.repository}/blob/{commit_hash}/images/{config.image}/Dockerfile)",
            f"[Build manifest](./{filename})",
        ]
    )
    build_history_line = f"| {date_column} | {image_column} | {links_column} |"
    config.hist_lines_dir.mkdir(parents=True, exist_ok=True)
    file = config.hist_lines_dir / f"{filename}.txt"
    file.write_text(build_history_line)
    LOGGER.info(f"Build history line written to: {file}")


def write_manifest_file(
    config: Config,
    filename: str,
    manifests: list[ManifestInterface],
    container: Container,
) -> None:
    manifest_names = [manifest.__class__.__name__ for manifest in manifests]
    LOGGER.info(f"Using manifests: {manifest_names}")

    markdown_pieces = [ManifestHeader.create_header(config, BUILD_TIMESTAMP)] + [
        manifest.markdown_piece(container) for manifest in manifests
    ]
    markdown_content = "\n\n".join(markdown_pieces) + "\n"

    config.manifests_dir.mkdir(parents=True, exist_ok=True)
    file = config.manifests_dir / f"{filename}.md"
    file.write_text(markdown_content)
    LOGGER.info(f"Manifest file written to: {file}")


def write_manifest(config: Config) -> None:
    LOGGER.info(f"Creating manifests for image: {config.image}")
    taggers, manifests = get_taggers_and_manifests(config.image)

    file_prefix = get_file_prefix(config.variant)
    commit_hash_tag = GitHelper.commit_hash_tag()
    filename = f"{file_prefix}-{config.image}-{commit_hash_tag}"

    with DockerRunner(config.full_image()) as container:
        tags_prefix = get_tag_prefix(config.variant)
        all_tags = [
            tags_prefix + "-" + tagger.tag_value(container) for tagger in taggers
        ]
        write_build_history_line(config, filename, all_tags)
        write_manifest_file(config, filename, manifests, container)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    LOGGER.info(f"Current build timestamp: {BUILD_TIMESTAMP}")

    config = common_arguments_parser(
        registry=True,
        owner=True,
        image=True,
        variant=True,
        hist_lines_dir=True,
        manifests_dir=True,
        repository=True,
    )
    write_manifest(config)
