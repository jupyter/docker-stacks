# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
test_packages
~~~~~~~~~~~~~~~
This test module tests if R and Python packages installed can be imported.
It's a basic test aiming to prove that the package is working properly.

The goal is to detect import errors that can be caused by incompatibilities between packages, for example:

- #1012: issue importing `sympy`
- #966: issue importing `pyarrow`

This module checks dynamically, through the `CondaPackageHelper`,
only the requested packages i.e. packages requested by `mamba install` in the `Dockerfile`s.
This means that it does not check dependencies.
This choice is a tradeoff to cover the main requirements while achieving reasonable test duration.
However it could be easily changed (or completed) to cover also dependencies.
Use `package_helper.installed_packages()` instead of `package_helper.requested_packages()`.

Example:

    $ make test/base-notebook

    # [...]
    # tests/base-notebook/test_packages.py::test_python_packages
    # ---------------------------------------------------------------------------------------------- live log setup ----------------------------------------------------------------------------------------------
    # 2023-11-04 23:59:01 [    INFO] Starting container quay.io/jupyter/base-notebook ... (package_helper.py:55)
    # 2023-11-04 23:59:01 [    INFO] Running quay.io/jupyter/base-notebook with args {'detach': True, 'tty': True, 'command': ['start.sh', 'bash', '-c', 'sleep infinity']} ... (conftest.py:99)
    # 2023-11-04 23:59:01 [    INFO] Grabbing the list of manually requested packages ... (package_helper.py:83)
    # ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
    # 2023-11-04 23:59:02 [    INFO] Testing the import of packages ... (test_packages.py:152)
    # 2023-11-04 23:59:02 [    INFO] Trying to import mamba (test_packages.py:154)
    # [...]

"""

import logging
from collections.abc import Iterable
from typing import Callable

import pytest  # type: ignore

from tests.conftest import TrackedContainer
from tests.package_helper import CondaPackageHelper

LOGGER = logging.getLogger(__name__)

# Mapping between package and module name
PACKAGE_MAPPING = {
    # Python
    "beautifulsoup4": "bs4",
    "jupyter-pluto-proxy": "jupyter_pluto_proxy",
    "matplotlib-base": "matplotlib",
    "pytables": "tables",
    "scikit-image": "skimage",
    "scikit-learn": "sklearn",
    # R
    "randomforest": "randomForest",
    "rcurl": "RCurl",
    "rodbc": "RODBC",
    "rsqlite": "DBI",
}

# List of packages that cannot be tested in a standard way
EXCLUDED_PACKAGES = [
    "bzip2",
    "ca-certificates",
    "conda-forge::blas[build=openblas]",
    "grpcio-status",
    "grpcio",
    "hdf5",
    "jupyterlab-git",
    "openssl",
    "pandas[version='>",
    "protobuf",
    "python",
    "r-irkernel",
    "unixodbc",
]


@pytest.fixture(scope="function")
def package_helper(container: TrackedContainer) -> CondaPackageHelper:
    """Return a package helper object that can be used to perform tests on installed packages"""
    return CondaPackageHelper(container)


@pytest.fixture(scope="function")
def packages(package_helper: CondaPackageHelper) -> dict[str, set[str]]:
    """Return the list of requested packages (i.e. packages explicitly installed excluding dependencies)"""
    return package_helper.requested_packages()


def get_package_import_name(package: str) -> str:
    """Perform a mapping between the python package name and the name used for the import"""
    return PACKAGE_MAPPING.get(package, package)


def excluded_package_predicate(package: str) -> bool:
    """Return whether a package is excluded from the list
    (i.e. a package that cannot be tested with standard imports)"""
    return package in EXCLUDED_PACKAGES


def python_package_predicate(package: str) -> bool:
    """Predicate matching python packages"""
    return not excluded_package_predicate(package) and not r_package_predicate(package)


def r_package_predicate(package: str) -> bool:
    """Predicate matching R packages"""
    return not excluded_package_predicate(package) and package.startswith("r-")


def _check_import_package(
    package_helper: CondaPackageHelper, command: list[str]
) -> None:
    """Generic function executing a command"""
    LOGGER.debug(f"Trying to import a package with [{command}] ...")
    exec_result = package_helper.running_container.exec_run(command)
    assert (
        exec_result.exit_code == 0
    ), f"Import package failed, output: {exec_result.output}"


def check_import_python_package(
    package_helper: CondaPackageHelper, package: str
) -> None:
    """Try to import a Python package from the command line"""
    _check_import_package(package_helper, ["python", "-c", f"import {package}"])


def check_import_r_package(package_helper: CondaPackageHelper, package: str) -> None:
    """Try to import an R package from the command line"""
    _check_import_package(package_helper, ["R", "--slave", "-e", f"library({package})"])


def _check_import_packages(
    package_helper: CondaPackageHelper,
    packages_to_check: Iterable[str],
    check_function: Callable[[CondaPackageHelper, str], None],
) -> None:
    """Test if packages can be imported

    Note: using a list of packages instead of a fixture for the list of packages
    since pytest prevents use of multiple yields
    """
    failures = {}
    LOGGER.info("Testing the import of packages ...")
    for package in packages_to_check:
        LOGGER.info(f"Trying to import {package}")
        try:
            check_function(package_helper, package)
        except AssertionError as err:
            failures[package] = err
    if len(failures) > 0:
        raise AssertionError(failures)


@pytest.fixture(scope="function")
def r_packages(packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of R packages"""
    # package[2:] is to remove the leading "r-" appended on R packages
    return map(
        lambda package: get_package_import_name(package[2:]),
        filter(r_package_predicate, packages),
    )


def test_r_packages(
    package_helper: CondaPackageHelper, r_packages: Iterable[str]
) -> None:
    """Test the import of specified R packages"""
    _check_import_packages(package_helper, r_packages, check_import_r_package)


@pytest.fixture(scope="function")
def python_packages(packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of Python packages"""
    return map(get_package_import_name, filter(python_package_predicate, packages))


def test_python_packages(
    package_helper: CondaPackageHelper,
    python_packages: Iterable[str],
) -> None:
    """Test the import of specified python packages"""
    _check_import_packages(package_helper, python_packages, check_import_python_package)
