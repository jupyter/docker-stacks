#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime
import logging

from docker.models.containers import Container

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.hierarchy.get_manifests import get_manifests
from tagging.hierarchy.get_taggers import get_taggers
from tagging.manifests.build_info import BuildInfo
from tagging.utils.config import Config
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix
from tagging.utils.git_helper import GitHelper

LOGGER = logging.getLogger(__name__)

# We use a manifest creation timestamp, which happens right after a build
BUILD_TIMESTAMP = datetime.datetime.now(datetime.UTC).isoformat()[:-13] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def get_build_history_line(config: Config, filename: str, container: Container) -> str:
    LOGGER.info(f"Calculating build history line for image: {config.image}")

    taggers = get_taggers(config.image)
    tags_prefix = get_tag_prefix(config.variant)
    all_tags = [tags_prefix + "-" + tagger.tag_value(container) for tagger in taggers]

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

    LOGGER.info(f"Build history line calculated for image: {config.image}")
    return build_history_line


def write_build_history_line(
    config: Config, filename: str, container: Container
) -> None:
    LOGGER.info(f"Writing tags for image: {config.image}")

    path = config.hist_lines_dir / f"{filename}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    build_history_line = get_build_history_line(config, filename, container)
    path.write_text(build_history_line)

    LOGGER.info(f"Build history line written to: {path}")


def get_manifest(config: Config, commit_hash_tag: str, container: Container) -> str:
    LOGGER.info(f"Calculating manifest file for image: {config.image}")

    manifests = get_manifests(config.image)
    manifest_names = [manifest.__class__.__name__ for manifest in manifests]
    LOGGER.info(f"Using manifests: {manifest_names}")

    markdown_pieces = [
        f"# Build manifest for image: {config.image}:{commit_hash_tag}",
        BuildInfo.markdown_piece(config, BUILD_TIMESTAMP).get_str(),
        *(manifest.markdown_piece(container).get_str() for manifest in manifests),
    ]
    markdown_content = "\n\n".join(markdown_pieces) + "\n"

    LOGGER.info(f"Manifest file calculated for image: {config.image}")
    return markdown_content


def write_manifest(
    config: Config, filename: str, commit_hash_tag: str, container: Container
) -> None:
    LOGGER.info(f"Writing manifest file for image: {config.image}")

    path = config.manifests_dir / f"{filename}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = get_manifest(config, commit_hash_tag, container)
    path.write_text(manifest)

    LOGGER.info(f"Manifest file wrtitten to: {path}")


def write_all(config: Config) -> None:
    LOGGER.info(f"Writing all files for image: {config.image}")

    file_prefix = get_file_prefix(config.variant)
    commit_hash_tag = GitHelper.commit_hash_tag()
    filename = f"{file_prefix}-{config.image}-{commit_hash_tag}"

    with DockerRunner(config.full_image()) as container:
        write_build_history_line(config, filename, container)
        write_manifest(config, filename, commit_hash_tag, container)

    LOGGER.info(f"All files written for image: {config.image}")


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
    write_all(config)
