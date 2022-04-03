# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from types import TracebackType
from typing import Optional

import docker
from docker.models.containers import Container

LOGGER = logging.getLogger(__name__)


class DockerRunner:
    def __init__(
        self,
        image_name: str,
        docker_client: docker.DockerClient = docker.from_env(),
        command: str = "sleep infinity",
    ):
        self.container: Optional[Container] = None
        self.image_name: str = image_name
        self.command: str = command
        self.docker_client: docker.DockerClient = docker_client

    def __enter__(self) -> Container:
        LOGGER.info(f"Creating container for image {self.image_name} ...")
        self.container = self.docker_client.containers.run(
            image=self.image_name,
            command=self.command,
            detach=True,
        )
        LOGGER.info(f"Container {self.container.name} created")
        return self.container

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        assert self.container is not None
        LOGGER.info(f"Removing container {self.container.name} ...")
        if self.container:
            self.container.remove(force=True)
            LOGGER.info(f"Container {self.container.name} removed")

    @staticmethod
    def run_simple_command(
        container: Container, cmd: str, print_result: bool = True
    ) -> str:
        LOGGER.info(f"Running cmd: '{cmd}' on container: {container}")
        out = container.exec_run(cmd)
        result = out.output.decode("utf-8").rstrip()
        assert isinstance(result, str)
        if print_result:
            LOGGER.info(f"Command result: {result}")
        assert out.exit_code == 0, f"Command: {cmd} failed"
        return result
