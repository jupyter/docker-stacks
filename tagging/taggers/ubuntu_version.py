# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.utils.docker_runner import DockerRunner


def ubuntu_version_tagger(container: Container) -> str:
    os_release = DockerRunner.exec_cmd(
        container,
        "cat /etc/os-release",
    ).split("\n")
    for line in os_release:
        if line.startswith("VERSION_ID"):
            return "ubuntu-" + line.split("=")[1].strip('"')
    raise RuntimeError(f"did not find ubuntu version in: {os_release}")
