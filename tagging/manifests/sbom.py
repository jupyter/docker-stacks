# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import textwrap
from dataclasses import dataclass

import plumbum

from tagging.manifests.manifest_interface import MarkdownPiece

docker = plumbum.local["docker"]


@dataclass(frozen=True)
class SbomConfig:
    registry: str
    owner: str
    image: str


def build_sbom(config: SbomConfig) -> MarkdownPiece:
    sbom = docker[
        "sbom", f"{config.registry}/{config.owner}/{config.image}:latest"
    ]().rstrip()

    return MarkdownPiece(
        title="## SBOM",
        sections=[
            textwrap.dedent(
                """\
                ```text
                {sbom}
                ```"""
            ).format(sbom=sbom)
        ],
    )
