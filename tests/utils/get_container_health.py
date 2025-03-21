# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import docker

from tests.utils.tracked_container import TrackedContainer


def get_health(container: TrackedContainer, client: docker.DockerClient) -> str:
    assert container.container is not None
    inspect_results = client.api.inspect_container(container.container.name)
    return inspect_results["State"]["Health"]["Status"]  # type: ignore
