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
    **kwargs: dict, optional
        Default keyword arguments to pass to docker.DockerClient.containers.run
    """

    def __init__(
        self,
        docker_client: docker.DockerClient,
        image_name: str,
        **kwargs: Any,
    ):
        self.running: Container | None = None
        self.docker_client: docker.DockerClient = docker_client
        self.image_name: str = image_name
        self.kwargs: Any = kwargs

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
        all_kwargs = self.kwargs | kwargs
        LOGGER.info(f"Running {self.image_name} with args {all_kwargs} ...")
        self.running = self.docker_client.containers.run(
            self.image_name,
            **all_kwargs,
        )

    def get_logs(self) -> str:
        assert self.running is not None
        logs = self.running.logs().decode()
        assert isinstance(logs, str)
        return logs

    def exec_cmd(self, cmd: str, print_output: bool = True, **kwargs: Any) -> str:
        assert self.running is not None
        container = self.running
        LOGGER.info(f"Running cmd: `{cmd}` on container: {container.name}")
        exec_result = container.exec_run(cmd, **kwargs)
        output = exec_result.output.decode().rstrip()
        assert isinstance(output, str)
        if print_output:
            LOGGER.info(f"Command output: {output}")
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
        assert self.running is not None
        rv = self.running.wait(timeout=timeout)
        logs = self.get_logs()
        LOGGER.debug(logs)
        assert no_warnings == (not self.get_warnings(logs))
        assert no_errors == (not self.get_errors(logs))
        assert no_failure == (rv["StatusCode"] == 0)
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
        if self.running is None:
            LOGGER.info("No container to remove")
        else:
            LOGGER.info(f"Removing container {self.running.name} ...")
            self.running.remove(force=True)
            LOGGER.info(f"Container {self.running.name} removed")
