# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

from tests.conftest import TrackedContainer
from tests.images_hierarchy import get_test_dirs

LOGGER = logging.getLogger(__name__)


def test_units(container: TrackedContainer) -> None:
    """Various units tests
    Add a py file in the `tests/<somestack>/units` dir, and it will be automatically tested
    """
    short_image_name = container.image_name[container.image_name.rfind("/") + 1 :]
    LOGGER.info(f"Running unit tests for: {short_image_name}")

    test_dirs = get_test_dirs(short_image_name)

    for test_dir in test_dirs:
        host_data_dir = test_dir / "units"
        LOGGER.info(f"Searching for units tests in {host_data_dir}")
        cont_data_dir = "/home/jovyan/data"

        if not host_data_dir.exists():
            LOGGER.info(f"Not found unit tests for image: {container.image_name}")
            continue

        for test_file in host_data_dir.iterdir():
            test_file_name = test_file.name
            LOGGER.info(f"Running unit test: {test_file_name}")

            container.run_and_wait(
                timeout=30,
                volumes={str(host_data_dir): {"bind": cont_data_dir, "mode": "ro"}},
                tty=True,
                command=["start.sh", "python", f"{cont_data_dir}/{test_file_name}"],
            )
