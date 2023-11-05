# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import plumbum
from docker.models.containers import Container

from tagging.docker_runner import DockerRunner
from tagging.git_helper import GitHelper

docker = plumbum.local["docker"]


def quoted_output(container: Container, cmd: str) -> str:
    cmd_output = DockerRunner.run_simple_command(container, cmd, print_result=False)
    # For example, `mamba info --quiet` adds redundant empty lines
    cmd_output = cmd_output.strip("\n")
    # For example, R packages list contains trailing backspaces
    cmd_output = "\n".join(line.rstrip() for line in cmd_output.split("\n"))
    return f"""\
`{cmd}`:

```text
{cmd_output}
```"""


class ManifestHeader:
    """ManifestHeader doesn't fall under common interface, and we run it separately"""

    @staticmethod
    def create_header(
        short_image_name: str, registry: str, owner: str, build_timestamp: str
    ) -> str:
        commit_hash = GitHelper.commit_hash()
        commit_hash_tag = GitHelper.commit_hash_tag()
        commit_message = GitHelper.commit_message()

        # Unfortunately, `docker images` doesn't work when specifying `docker.io` as registry
        fixed_registry = registry + "/" if registry != "docker.io" else ""

        image_size = docker[
            "images",
            f"{fixed_registry}{owner}/{short_image_name}:latest",
            "--format",
            "{{.Size}}",
        ]().rstrip()

        return f"""\
# Build manifest for image: {short_image_name}:{commit_hash_tag}

## Build Info

- Build datetime: {build_timestamp}
- Docker image: `{registry}/{owner}/{short_image_name}:{commit_hash_tag}`
- Docker image size: {image_size}
- Git commit SHA: [{commit_hash}](https://github.com/jupyter/docker-stacks/commit/{commit_hash})
- Git commit message:

```text
{commit_message}
```"""


class ManifestInterface:
    """Common interface for all manifests"""

    @staticmethod
    def markdown_piece(container: Container) -> str:
        raise NotImplementedError


class CondaEnvironmentManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Python Packages

{DockerRunner.run_simple_command(container, "python --version")}

{quoted_output(container, "mamba info --quiet")}

{quoted_output(container, "mamba list")}"""


class AptPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Apt Packages

{quoted_output(container, "apt list --installed")}"""


class RPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## R Packages

{quoted_output(container, "R --version")}

{quoted_output(container, "R --silent -e 'installed.packages(.Library)[, c(1,3)]'")}"""


class JuliaPackagesManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Julia Packages

{quoted_output(container, "julia -E 'using InteractiveUtils; versioninfo()'")}

{quoted_output(container, "julia -E 'import Pkg; Pkg.status()'")}"""


class SparkInfoManifest(ManifestInterface):
    @staticmethod
    def markdown_piece(container: Container) -> str:
        return f"""\
## Apache Spark

{quoted_output(container, "/usr/local/spark/bin/spark-submit --version")}"""
