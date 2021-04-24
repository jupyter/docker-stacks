#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import datetime
import logging
import os
from docker_runner import DockerRunner
from get_taggers_and_manifests import get_taggers_and_manifests
from git_helper import GitHelper
from taggers import SHATagger


logger = logging.getLogger(__name__)


BUILD_TIMESTAMP = datetime.datetime.utcnow().isoformat()[:-7] + "Z"
MARKDOWN_LINE_BREAK = "<br />"


def append_build_history_line(short_image_name, owner, wiki_path, all_tags, container):
    logger.info("Appending build history line")

    date_column = f"`{BUILD_TIMESTAMP}`"
    image_column = MARKDOWN_LINE_BREAK.join(
        f"`{owner}/{short_image_name}:{tag_value}`" for tag_value in all_tags
    )
    commit_sha_tag = SHATagger.tag_value(container)  # first 12 letters of commit hash
    commit_hash = GitHelper.commit_hash()  # full commit hash
    links_column = MARKDOWN_LINE_BREAK.join([
        f"[Git diff](https://github.com/jupyter/docker-stacks/commit/{commit_hash})",
        f"[Dockerfile](https://github.com/jupyter/docker-stacks/blob/{commit_hash}/{short_image_name}/Dockerfile)"
        f"[Build manifest](./{short_image_name}-{commit_sha_tag})"
    ])
    build_history_line = "|".join([date_column, image_column, links_column]) + "|"

    home_wiki_file = os.path.join(wiki_path, 'Home.md')
    with open(home_wiki_file, "r") as f:
        file = f.read()
    TABLE_BEGINNING = "|-|-|-|\n"
    file = file.replace(TABLE_BEGINNING, TABLE_BEGINNING + build_history_line + "\n")
    with open(home_wiki_file, "w") as f:
        f.write(file)


def create_manifests(short_image_name, owner, wiki_path):
    logger.info(f"Creating manifests for image: {short_image_name}")
    taggers, manifests = get_taggers_and_manifests(short_image_name)

    image = f"{owner}/{short_image_name}:latest"

    with DockerRunner(image) as container:
        all_tags = [tagger.tag_value(container) for tagger in taggers]
        append_build_history_line(short_image_name, owner, wiki_path, all_tags, container)

        manifest_names = [manifest.__name__ for manifest in manifests]
        logger.info(f"Using manifests: {manifest_names}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--short-image-name", required=True, help="Short image name to apply tags for")
    arg_parser.add_argument("--owner", required=True, help="Owner of the image")
    arg_parser.add_argument("--wiki-path", required=True, help="Path to the wiki pages")
    args = arg_parser.parse_args()

    logger.info(f"Current build timestamp: {BUILD_TIMESTAMP}")

    create_manifests(args.short_image_name, args.owner, args.wiki_path)
