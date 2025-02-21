# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.manifests.manifest_interface import ManifestInterface
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.quoted_output import quoted_output


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Python Packages

{DockerRunner.run_simple_command(container, "python --version")}

{quoted_output(container, "conda info")}

{quoted_output(container, "mamba info")}

{quoted_output(container, "mamba list")}"""
