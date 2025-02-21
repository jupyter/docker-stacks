# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.taggers.tagger_interface import TaggerInterface
from tagging.utils.docker_runner import DockerRunner


class UbuntuVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        os_release = DockerRunner.run_simple_command(
            container,
            "cat /etc/os-release",
        ).split("\n")
        for line in os_release:
            if line.startswith("VERSION_ID"):
                return "ubuntu-" + line.split("=")[1].strip('"')
        raise RuntimeError(f"did not find ubuntu version in: {os_release}")
