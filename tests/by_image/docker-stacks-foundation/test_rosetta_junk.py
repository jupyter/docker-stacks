# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import io
import tarfile

import docker
from docker.errors import NotFound


def test_no_rosetta_junk(docker_client: docker.DockerClient, image_name: str) -> None:
    """Rosetta junk must not be baked into the image.

    The image is inspected without being run:
    macOS Rosetta virtualization creates ~/.cache/rosetta as soon as
    any process runs in a container,
    so checking inside a running container would fail on macOS hosts
    even for clean images.
    """
    container = docker_client.containers.create(image_name)
    try:
        try:
            bits, _stat = container.get_archive("/home/jovyan/.cache")
        except NotFound:
            return
        archive = b"".join(bits)
    finally:
        container.remove(force=True)

    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        junk = [name for name in tar.getnames() if "rosetta" in name]
    assert not junk, f"Rosetta junk found in the image: {junk}"
