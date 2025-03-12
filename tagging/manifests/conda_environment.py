# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.manifests.manifest_interface import MarkdownPiece
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.quoted_output import quoted_output


def conda_environment_manifest(container: Container) -> MarkdownPiece:
    return MarkdownPiece(
        title="## Python Packages",
        sections=[
            DockerRunner.exec_cmd(container, "python --version"),
            quoted_output(container, "conda info"),
            quoted_output(container, "mamba info"),
            quoted_output(container, "mamba list"),
        ],
    )
