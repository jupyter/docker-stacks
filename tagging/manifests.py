# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from docker_runner import run_simple_command


logger = logging.getLogger(__name__)


def quoted_output(container, cmd: str) -> str:
    return "\n".join([
        "```",
        run_simple_command(container, cmd, print_result=False),
        "```"
    ])


class ManifestInterface:
    """Common interface for all manifests"""
    @staticmethod
    def markdown_piece(container) -> str:
        raise NotImplementedError


class BuildInfoManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return None


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join([
            "## Python Packages",
            "",
            quoted_output(container, "python --version"),
            "",
            quoted_output(container, "conda info"),
            "",
            quoted_output(container, "conda list")
        ])


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container) -> str:
        return "\n".join([
            "## Apt Packages",
            "",
            quoted_output(container, "apt list --installed")
        ])
