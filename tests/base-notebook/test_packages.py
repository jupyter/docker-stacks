# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
test_packages
~~~~~~~~~~~~~~~
This test module tests if R and Python packages installed can be imported.
It's a basic test aiming to prove that the package is working properly.

The goal is to detect import errors that can be caused by incompatibilities between packages, for example:

- #1012: issue importing `sympy`
- #966: isssue importing `pyarrow`

This module checks dynamically, through the `CondaPackageHelper`, only the requested packages i.e. packages requested by `mamba install` in the `Dockerfile`s.
This means that it does not check dependencies. This choice is a tradeoff to cover the main requirements while achieving reasonable test duration.
However it could be easily changed (or completed) to cover also dependencies `package_helper.installed_packages()` instead of `package_helper.requested_packages()`.

Example:

    $ make test/base-notebook

    # [...]
    # test/test_packages.py::test_python_packages
    # tests/base-notebook/test_packages.py::test_python_packages
    # ---------------------------------------------------------------------------------------------- live log setup ----------------------------------------------------------------------------------------------
    # 2022-02-17 16:44:36 [    INFO] Starting container jupyter/base-notebook ... (package_helper.py:55)
    # 2022-02-17 16:44:36 [    INFO] Running jupyter/base-notebook with args {'detach': True, 'tty': True, 'command': ['start.sh', 'bash', '-c', 'sleep infinity']} ... (conftest.py:95)
    # 2022-02-17 16:44:37 [    INFO] Grabing the list of manually requested packages ... (package_helper.py:83)
    # ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
    # 2022-02-17 16:44:38 [    INFO] Testing the import of packages ... (test_packages.py:144)
    # 2022-02-17 16:44:38 [    INFO] Trying to import mamba (test_packages.py:146)
    # [...]

"""

import logging

import pytest  # type: ignore
from conftest import TrackedContainer
from typing import Callable, Iterable

from package_helper import CondaPackageHelper

LOGGER = logging.getLogger(__name__)

# Mapping between package and module name
PACKAGE_MAPPING = {
    # Python
    "matplotlib-base": "matplotlib",
    "beautifulsoup4": "bs4",
    "scikit-learn": "sklearn",
    "scikit-image": "skimage",
    "spylon-kernel": "spylon_kernel",
    "pytables": "tables",
    # R
    "randomforest": "randomForest",
    "rsqlite": "DBI",
    "rcurl": "RCurl",
    "rodbc": "RODBC",
}

# List of packages that cannot be tested in a standard way
EXCLUDED_PACKAGES = [
    "python",
    "hdf5",
    "conda-forge::blas[build=openblas]",
    "protobuf",
    "r-irkernel",
    "unixodbc",
    "bzip2",
    "openssl",
    "ca-certificates",
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
    """Return whether a package is excluded from the list (i.e. a package that cannot be tested with standard imports)"""
    return package in EXCLUDED_PACKAGES


def python_package_predicate(package: str) -> bool:
    """Predicate matching python packages"""
    return not excluded_package_predicate(package) and not r_package_predicate(package)


def r_package_predicate(package: str) -> bool:
    """Predicate matching R packages"""
    return not excluded_package_predicate(package) and package.startswith("r-")


def _check_import_package(
    package_helper: CondaPackageHelper, command: list[str]
) -> int:
    """Generic function executing a command"""
    LOGGER.debug(f"Trying to import a package with [{command}] ...")
    rc = package_helper.running_container.exec_run(command)
    return rc.exit_code  # type: ignore


def check_import_python_package(
    package_helper: CondaPackageHelper, package: str
) -> int:
    """Try to import a Python package from the command line"""
    return _check_import_package(package_helper, ["python", "-c", f"import {package}"])


def check_import_r_package(package_helper: CondaPackageHelper, package: str) -> int:
    """Try to import a R package from the command line"""
    return _check_import_package(
        package_helper, ["R", "--slave", "-e", f"library({package})"]
    )


def _check_import_packages(
    package_helper: CondaPackageHelper,
    filtered_packages: Iterable[str],
    check_function: Callable[[CondaPackageHelper, str], int],
    max_failures: int,
) -> None:
    """Test if packages can be imported

    Note: using a list of packages instead of a fixture for the list of packages since pytest prevents use of multiple yields
    """
    failures = {}
    LOGGER.info("Testing the import of packages ...")
    for package in filtered_packages:
        LOGGER.info(f"Trying to import {package}")
        try:
            assert (
                check_function(package_helper, package) == 0
            ), f"Package [{package}] import failed"
        except AssertionError as err:
            failures[package] = err
    if len(failures) > max_failures:
        raise AssertionError(failures)
    elif len(failures) > 0:
        LOGGER.warning(f"Some import(s) has(have) failed: {failures}")


@pytest.fixture(scope="function")
def r_packages(packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of R packages"""
    # package[2:] is to remove the leading "r-" appended on R packages
    return map(
        lambda package: get_package_import_name(package[2:]),
        filter(r_package_predicate, packages),
    )


def test_r_packages(
    package_helper: CondaPackageHelper, r_packages: Iterable[str], max_failures: int = 0
) -> None:
    """Test the import of specified R packages"""
    _check_import_packages(
        package_helper, r_packages, check_import_r_package, max_failures
    )


@pytest.fixture(scope="function")
def python_packages(packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of Python packages"""
    return map(get_package_import_name, filter(python_package_predicate, packages))


def test_python_packages(
    package_helper: CondaPackageHelper,
    python_packages: Iterable[str],
    max_failures: int = 0,
) -> None:
    """Test the import of specified python packages"""
    _check_import_packages(
        package_helper, python_packages, check_import_python_package, max_failures
    )
