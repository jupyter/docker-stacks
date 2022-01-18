# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import docker
import logging

from conftest import TrackedContainer


LOGGER = logging.getLogger(__name__)


class DockerRunner:
    def __init__(
        self,
        image_name: str,
        docker_client=docker.from_env(),
        command: str = "sleep infinity",
    ):
        self.container = None
        self.image_name = image_name
        self.command = command
        self.docker_client = docker_client

    def __enter__(self):
        LOGGER.info(f"Creating container for image {self.image_name} ...")
        self.container = self.docker_client.containers.run(
            image=self.image_name,
            command=self.command,
            detach=True,
        )
        LOGGER.info(f"Container {self.container.name} created")
        return self.container

    def __exit__(self, exc_type, exc_value, traceback):
        LOGGER.info(f"Removing container {self.container.name} ...")
        if self.container:
            self.container.remove(force=True)
            LOGGER.info(f"Container {self.container.name} removed")

    @staticmethod
    def run_simple_command(
        container: TrackedContainer, cmd: str, print_result: bool = True
    ):
        LOGGER.info(f"Running cmd: '{cmd}' on container: {container}")
        out = container.exec_run(cmd)
        result = out.output.decode("utf-8").rstrip()
        if print_result:
            LOGGER.info(f"Command result: {result}")
        assert out.exit_code == 0, f"Command: {cmd} failed"
        return result
