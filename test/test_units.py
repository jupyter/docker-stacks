# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
from pathlib import Path

from conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


def test_units(container: TrackedContainer) -> None:
    """Various units tests
    Add a py file in the {image}/test/units dir and it will be automatically tested
    """
    short_image_name = container.image_name[container.image_name.rfind("/") + 1 :]
    host_data_dir = THIS_DIR / f"../{short_image_name}/test/units"
    LOGGER.info(f"Searching for units tests in {host_data_dir}")
    cont_data_dir = "/home/jovyan/data"

    if not host_data_dir.exists():
        LOGGER.info(f"Not found unit tests for image: {container.image_name}")
        return

    for test_file in host_data_dir.iterdir():
        test_file_name = test_file.name
        LOGGER.info(f"Running unit test: {test_file_name}")

        container.run_and_wait(
            timeout=30,
            volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
            tty=True,
            command=["start.sh", "python", f"{cont_data_dir}/{test_file_name}"],
        )
