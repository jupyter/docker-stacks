#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import datetime
import logging
from pathlib import Path

from docker.models.containers import Container

from tagging.docker_runner import DockerRunner
from tagging.get_platform import get_platform
from tagging.get_taggers_and_manifests import get_taggers_and_manifests
from tagging.git_helper import GitHelper
from tagging.manifests import ManifestHeader, ManifestInterface

LOGGER = logging.getLogger(__name__)

# We use a manifest creation timestamp, which happens right after a build
BUILD_TIMESTAMP = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def write_build_history_line(
    short_image_name: str,
    registry: str,
    owner: str,
    hist_lines_dir: Path,
    filename: str,
    all_tags: list[str],
) -> None:
    LOGGER.info("Appending build history line")

    date_column = f"`{BUILD_TIMESTAMP}`"
    image_column = MARKDOWN_LINE_BREAK.join(
        f"`{registry}/{owner}/{short_image_name}:{tag_value}`" for tag_value in all_tags
    )
    commit_hash = GitHelper.commit_hash()
    links_column = MARKDOWN_LINE_BREAK.join(
        [
            f"[Git diff](https://github.com/jupyter/docker-stacks/commit/{commit_hash})",
            f"[Dockerfile](https://github.com/jupyter/docker-stacks/blob/{commit_hash}/images/{short_image_name}/Dockerfile)",
            f"[Build manifest](./{filename})",
        ]
    )
    build_history_line = f"| {date_column} | {image_column} | {links_column} |"
    hist_lines_dir.mkdir(parents=True, exist_ok=True)
    (hist_lines_dir / f"{filename}.txt").write_text(build_history_line)


def write_manifest_file(
    short_image_name: str,
    registry: str,
    owner: str,
    manifests_dir: Path,
    filename: str,
    manifests: list[ManifestInterface],
    container: Container,
) -> None:
    manifest_names = [manifest.__class__.__name__ for manifest in manifests]
    LOGGER.info(f"Using manifests: {manifest_names}")

    markdown_pieces = [
        ManifestHeader.create_header(short_image_name, registry, owner, BUILD_TIMESTAMP)
    ] + [manifest.markdown_piece(container) for manifest in manifests]
    markdown_content = "\n\n".join(markdown_pieces) + "\n"

    manifests_dir.mkdir(parents=True, exist_ok=True)
    (manifests_dir / f"{filename}.md").write_text(markdown_content)


def write_manifest(
    short_image_name: str,
    registry: str,
    owner: str,
    hist_lines_dir: Path,
    manifests_dir: Path,
) -> None:
    LOGGER.info(f"Creating manifests for image: {short_image_name}")
    taggers, manifests = get_taggers_and_manifests(short_image_name)

    image = f"{registry}/{owner}/{short_image_name}:latest"

    file_prefix = get_platform()
    commit_hash_tag = GitHelper.commit_hash_tag()
    filename = f"{file_prefix}-{short_image_name}-{commit_hash_tag}"

    with DockerRunner(image) as container:
        tags_prefix = get_platform()
        all_tags = [
            tags_prefix + "-" + tagger.tag_value(container) for tagger in taggers
        ]
        write_build_history_line(
            short_image_name, registry, owner, hist_lines_dir, filename, all_tags
        )
        write_manifest_file(
            short_image_name,
            registry,
            owner,
            manifests_dir,
            filename,
            manifests,
            container,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name",
    )
    arg_parser.add_argument(
        "--hist-lines-dir",
        required=True,
        type=Path,
        help="Directory to save history line",
    )
    arg_parser.add_argument(
        "--manifests-dir",
        required=True,
        type=Path,
        help="Directory to save manifest file",
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

    LOGGER.info(f"Current build timestamp: {BUILD_TIMESTAMP}")

    write_manifest(
        args.short_image_name,
        args.registry,
        args.owner,
        args.hist_lines_dir,
        args.manifests_dir,
    )
