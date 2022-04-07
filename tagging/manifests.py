# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import plumbum
from docker.models.containers import Container

from .docker_runner import DockerRunner
from .git_helper import GitHelper

docker = plumbum.local["docker"]


def quoted_output(container: Container, cmd: str) -> str:
    return "\n".join(
        [
            "```",
            DockerRunner.run_simple_command(container, cmd, print_result=False),
            "```",
        ]
    )


class ManifestHeader:
    """ManifestHeader doesn't fall under common interface, and we run it separately"""

    @staticmethod
    def create_header(short_image_name: str, owner: str, build_timestamp: str) -> str:
        commit_hash = GitHelper.commit_hash()
        commit_hash_tag = GitHelper.commit_hash_tag()
        commit_message = GitHelper.commit_message()

        image_size = docker[
            "images", f"{owner}/{short_image_name}:latest", "--format", "{{.Size}}"
        ]().rstrip()

        return "\n".join(
            [
                f"# Build manifest for image: {short_image_name}:{commit_hash_tag}",
                "",
                "## Build Info",
                "",
                f"* Build datetime: {build_timestamp}",
                f"* Docker image: {owner}/{short_image_name}:{commit_hash_tag}",
                f"* Docker image size: {image_size}",
                f"* Git commit SHA: [{commit_hash}](https://github.com/jupyter/docker-stacks/commit/{commit_hash})",
                "* Git commit message:",
                "```",
                f"{commit_message}",
                "```",
            ]
        )


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container: Container) -> str:
        raise NotImplementedError


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return "\n".join(
            [
                "## Python Packages",
                "",
                quoted_output(container, "python --version"),
                "",
                quoted_output(container, "mamba info --quiet"),
                "",
                quoted_output(container, "mamba list"),
            ]
        )


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return "\n".join(
            [
                "## Apt Packages",
                "",
                quoted_output(container, "apt list --installed"),
            ]
        )


class RPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return "\n".join(
            [
                "## R Packages",
                "",
                quoted_output(container, "R --version"),
                "",
                quoted_output(
                    container,
                    "R --silent -e 'installed.packages(.Library)[, c(1,3)]'",
                ),
            ]
        )


class JuliaPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return "\n".join(
            [
                "## Julia Packages",
                "",
                quoted_output(
                    container,
                    "julia -E 'using InteractiveUtils; versioninfo()'",
                ),
                "",
                quoted_output(container, "julia -E 'import Pkg; Pkg.status()'"),
            ]
        )


class SparkInfoManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return "\n".join(
            [
                "## Apache Spark",
                "",
                quoted_output(container, "/usr/local/spark/bin/spark-submit --version"),
            ]
        )
