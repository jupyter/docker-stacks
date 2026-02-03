# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import textwrap
from dataclasses import dataclass

import plumbum

from tagging.manifests.manifest_interface import MarkdownPiece
from tagging.utils.git_helper import GitHelper

docker = plumbum.local["docker"]


@dataclass(frozen=True)
class BuildInfoConfig:
    registry: str
    owner: str
    image: str

    repository: str

    build_timestamp: str

    def full_image(self) -> str:
        return f"{self.registry}/{self.owner}/{self.image}"


def build_info_manifest(config: BuildInfoConfig) -> MarkdownPiece:
    """BuildInfo doesn't fall under common interface, and we run it separately"""
    commit_hash = GitHelper.commit_hash()
    commit_hash_tag = GitHelper.commit_hash_tag()
    commit_message = GitHelper.commit_message()

    # Unfortunately, `docker images` doesn't work when specifying `docker.io` as registry
    fixed_registry = config.registry + "/" if config.registry != "docker.io" else ""

    image_size = docker[
        "images",
        f"{fixed_registry}{config.owner}/{config.image}:latest",
        "--format",
        "{{.Size}}",
    ]().rstrip()

    build_info = textwrap.dedent(f"""\
        - Build timestamp: {config.build_timestamp}
        - Docker image: `{config.full_image()}:{commit_hash_tag}`
        - Docker image size: {image_size}
        - Git commit SHA: [{commit_hash}](https://github.com/{config.repository}/commit/{commit_hash})
        - Git commit message:

        ```text
        {{message}}
        ```""").format(message=commit_message)

    return MarkdownPiece(title="## Build Info", sections=[build_info])
