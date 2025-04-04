# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

import pytest  # type: ignore

from tests.shared_checks.nbconvert_check import check_nbconvert
from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)
THIS_DIR = Path(__file__).parent.resolve()


@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.parametrize(
    "test_file,expected_warnings",
    [
        ("local_sparkR", ["WARNING: Using incubator modules: jdk.incubator.vector"]),
        ("local_sparklyr", []),
    ],
)
@pytest.mark.parametrize("output_format", ["pdf", "html", "markdown"])
def test_spark_r_nbconvert(
    container: TrackedContainer,
    test_file: str,
    output_format: str,
    expected_warnings: list[str],
) -> None:
    host_data_file = THIS_DIR / "data" / f"{test_file}.ipynb"
    logs = check_nbconvert(
        container,
        host_data_file,
        output_format,
        execute=True,
        no_warnings=(not expected_warnings),
    )

    warnings = TrackedContainer.get_warnings(logs)
    assert warnings == expected_warnings
