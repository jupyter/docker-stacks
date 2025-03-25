# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from types import TracebackType

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
        self.container: Container | None = None
        self.image_name: str = image_name
        self.command: str = command
        self.docker_client: docker.DockerClient = docker_client

    def __enter__(self) -> Container:
        LOGGER.info(f"Creating a container for the image: {self.image_name} ...")
        default_kwargs = {"detach": True, "tty": True}
        self.container = self.docker_client.containers.run(
            image=self.image_name, command=self.command, **default_kwargs
        )
        LOGGER.info(f"Container {self.container.name} created")
        return self.container

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        assert self.container is not None
        LOGGER.info(f"Removing container {self.container.name} ...")
        self.container.remove(force=True)
        LOGGER.info(f"Container {self.container.name} removed")

    @staticmethod
    def exec_cmd(container: Container, cmd: str) -> str:
        LOGGER.info(f"Running cmd: `{cmd}` on container: {container.name}")
        exec_result = container.exec_run(cmd)
        output = exec_result.output.decode().rstrip()
        assert isinstance(output, str)
        if exec_result.exit_code != 0:
            LOGGER.error(f"Command output:\n{output}")
            raise AssertionError(f"Command: `{cmd}` failed")
        else:
            LOGGER.debug(f"Command output:\n{output}")
        return output
