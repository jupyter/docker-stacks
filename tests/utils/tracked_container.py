# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from typing import Any

import docker
from docker.models.containers import Container

LOGGER = logging.getLogger(__name__)


class TrackedContainer:
    """Wrapper that collects docker container configuration and delays
    container creation/execution.

    Parameters
    ----------
    docker_client: docker.DockerClient
        Docker client instance
    image_name: str
        Name of the docker image to launch
    """

    def __init__(
        self,
        docker_client: docker.DockerClient,
        image_name: str,
    ):
        self.container: Container | None = None
        self.docker_client: docker.DockerClient = docker_client
        self.image_name: str = image_name

    def run_detached(self, **kwargs: Any) -> None:
        """Runs a docker container using the pre-configured image name
        and a mix of the pre-configured container options and those passed
        to this method.

        Keeps track of the docker.Container instance spawned to kill it
        later.

        Parameters
        ----------
        **kwargs: dict, optional
            Keyword arguments to pass to docker.DockerClient.containers.run
            extending and/or overriding key/value pairs passed to the constructor
        """
        LOGGER.info(
            f"Creating a container for the image: {self.image_name} with args: {kwargs} ..."
        )
        default_kwargs = {"detach": True, "tty": True}
        final_kwargs = default_kwargs | kwargs
        self.container = self.docker_client.containers.run(
            self.image_name, **final_kwargs
        )
        LOGGER.info(f"Container {self.container.name} created")

    def get_logs(self) -> str:
        assert self.container is not None
        logs = self.container.logs().decode()
        assert isinstance(logs, str)
        return logs

    def get_health(self) -> str:
        assert self.container is not None
        self.container.reload()
        return self.container.health  # type: ignore

    def exec_cmd(self, cmd: str, **kwargs: Any) -> str:
        assert self.container is not None
        container = self.container

        LOGGER.info(f"Running cmd: `{cmd}` on container: {container.name}")
        default_kwargs = {"tty": True}
        final_kwargs = default_kwargs | kwargs
        exec_result = container.exec_run(cmd, **final_kwargs)
        output = exec_result.output.decode().rstrip()
        assert isinstance(output, str)
        LOGGER.debug(f"Command output: {output}")
        assert exec_result.exit_code == 0, f"Command: `{cmd}` failed"
        return output

    def run_and_wait(
        self,
        timeout: int,
        no_warnings: bool = True,
        no_errors: bool = True,
        no_failure: bool = True,
        **kwargs: Any,
    ) -> str:
        self.run_detached(**kwargs)
        assert self.container is not None
        rv = self.container.wait(timeout=timeout)
        logs = self.get_logs()
        LOGGER.debug(logs)
        assert no_warnings == (not self.get_warnings(logs))
        assert no_errors == (not self.get_errors(logs))
        assert no_failure == (rv["StatusCode"] == 0)
        self.remove()
        return logs

    @staticmethod
    def get_errors(logs: str) -> list[str]:
        return TrackedContainer._lines_starting_with(logs, "ERROR")

    @staticmethod
    def get_warnings(logs: str) -> list[str]:
        return TrackedContainer._lines_starting_with(logs, "WARNING")

    @staticmethod
    def _lines_starting_with(logs: str, pattern: str) -> list[str]:
        return [line for line in logs.splitlines() if line.startswith(pattern)]

    def remove(self) -> None:
        """Kills and removes the tracked docker container."""
        if self.container is None:
            LOGGER.debug("No container to remove")
        else:
            LOGGER.info(f"Removing container {self.container.name} ...")
            self.container.remove(force=True)
            LOGGER.info(f"Container {self.container.name} removed")
            self.container = None
