# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import docker
from docker.models.containers import Container


def get_health(container: Container, client: docker.DockerClient) -> str:
    inspect_results = client.inspect_container(container.name)
    return inspect_results["State"]["Health"]["Status"]  # type: ignore
