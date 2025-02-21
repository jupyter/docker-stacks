#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime
import logging
from pathlib import Path

from docker.models.containers import Container

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.hierarchy.get_taggers_and_manifests import (
    get_taggers_and_manifests,
)
from tagging.manifests.header import ManifestHeader
from tagging.manifests.manifest_interface import ManifestInterface
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix
from tagging.utils.git_helper import GitHelper

LOGGER = logging.getLogger(__name__)

# We use a manifest creation timestamp, which happens right after a build
BUILD_TIMESTAMP = datetime.datetime.now(datetime.UTC).isoformat()[:-13] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def write_build_history_line(
    *,
    registry: str,
    owner: str,
    short_image_name: str,
    hist_lines_dir: Path,
    filename: str,
    all_tags: list[str],
    repository: str,
) -> None:
    LOGGER.info("Appending build history line")

    date_column = f"`{BUILD_TIMESTAMP}`"
    image_column = MARKDOWN_LINE_BREAK.join(
        f"`{registry}/{owner}/{short_image_name}:{tag_value}`" for tag_value in all_tags
    )
    commit_hash = GitHelper.commit_hash()
    links_column = MARKDOWN_LINE_BREAK.join(
        [
            f"[Git diff](https://github.com/{repository}/commit/{commit_hash})",
            f"[Dockerfile](https://github.com/{repository}/blob/{commit_hash}/images/{short_image_name}/Dockerfile)",
            f"[Build manifest](./{filename})",
        ]
    )
    build_history_line = f"| {date_column} | {image_column} | {links_column} |"
    hist_lines_dir.mkdir(parents=True, exist_ok=True)
    file = hist_lines_dir / f"{filename}.txt"
    file.write_text(build_history_line)
    LOGGER.info(f"Build history line written to: {file}")


def write_manifest_file(
    *,
    registry: str,
    owner: str,
    short_image_name: str,
    manifests_dir: Path,
    filename: str,
    manifests: list[ManifestInterface],
    container: Container,
    repository: str,
) -> None:
    manifest_names = [manifest.__class__.__name__ for manifest in manifests]
    LOGGER.info(f"Using manifests: {manifest_names}")

    markdown_pieces = [
        ManifestHeader.create_header(
            registry=registry,
            owner=owner,
            short_image_name=short_image_name,
            build_timestamp=BUILD_TIMESTAMP,
            repository=repository,
        )
    ] + [manifest.markdown_piece(container) for manifest in manifests]
    markdown_content = "\n\n".join(markdown_pieces) + "\n"

    manifests_dir.mkdir(parents=True, exist_ok=True)
    file = manifests_dir / f"{filename}.md"
    file.write_text(markdown_content)
    LOGGER.info(f"Manifest file written to: {file}")


def write_manifest(
    *,
    registry: str,
    owner: str,
    short_image_name: str,
    variant: str,
    hist_lines_dir: Path,
    manifests_dir: Path,
    repository: str,
) -> None:
    LOGGER.info(f"Creating manifests for image: {registry}/{owner}/{short_image_name}")
    taggers, manifests = get_taggers_and_manifests(short_image_name)

    image = f"{registry}/{owner}/{short_image_name}:latest"

    file_prefix = get_file_prefix(variant)
    commit_hash_tag = GitHelper.commit_hash_tag()
    filename = f"{file_prefix}-{short_image_name}-{commit_hash_tag}"

    with DockerRunner(image) as container:
        tags_prefix = get_tag_prefix(variant)
        all_tags = [
            tags_prefix + "-" + tagger.tag_value(container) for tagger in taggers
        ]
        write_build_history_line(
            registry=registry,
            owner=owner,
            short_image_name=short_image_name,
            hist_lines_dir=hist_lines_dir,
            filename=filename,
            all_tags=all_tags,
            repository=repository,
        )
        write_manifest_file(
            registry=registry,
            owner=owner,
            short_image_name=short_image_name,
            manifests_dir=manifests_dir,
            filename=filename,
            manifests=manifests,
            container=container,
            repository=repository,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = common_arguments_parser(
        registry=True,
        owner=True,
        short_image_name=True,
        variant=True,
        hist_lines_dir=True,
        manifests_dir=True,
    )
    arg_parser.add_argument(
        "--repository",
        required=True,
        help="Repository name on GitHub",
    )
    args = arg_parser.parse_args()

    LOGGER.info(f"Current build timestamp: {BUILD_TIMESTAMP}")

    write_manifest(**vars(args))
