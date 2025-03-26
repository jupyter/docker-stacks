# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging

import pytest  # type: ignore

from tests.utils.conda_package_helper import CondaPackageHelper
from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("requested_only", [True, False])
@pytest.mark.info
def test_outdated_packages(container: TrackedContainer, requested_only: bool) -> None:
    """Getting the list of updatable packages"""
    LOGGER.info(f"Checking outdated packages in {container.image_name} ...")
    pkg_helper = CondaPackageHelper(container)
    updatable = pkg_helper.find_updatable_packages(requested_only)
    LOGGER.info(pkg_helper.get_outdated_summary(updatable, requested_only))
    LOGGER.info(
        f"Outdated packages table:\n{pkg_helper.get_outdated_table(updatable)}\n"
    )
