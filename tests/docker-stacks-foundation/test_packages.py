# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
test_packages
~~~~~~~~~~~~~~~
This test module tests if the R and Python packages installed can be imported.
It's a basic test aiming to prove that the package is working properly.

The goal is to detect import errors that can be caused by incompatibilities between packages, for example:

- #1012: issue importing `sympy`
- #966: issue importing `pyarrow`

This module checks dynamically, through the `CondaPackageHelper`,
only the requested packages i.e. packages requested by `mamba install` in the `Dockerfile`s.
This means that it does not check dependencies.
This choice is a tradeoff to cover the main requirements while achieving a reasonable test duration.
However, it could be easily changed (or completed) to cover dependencies as well.
Use `package_helper.installed_packages()` instead of `package_helper.requested_packages()`.

Example:

    $ make test/docker-stacks-foundation

    # [...]
    # tests/docker-stacks-foundation/test_packages.py::test_python_packages
    # -------------------------------- live log setup --------------------------------
    # 2024-01-21 17:46:43 [    INFO] Starting container quay.io/jupyter/docker-stacks-foundation ... (package_helper.py:55)
    # 2024-01-21 17:46:43 [    INFO] Running quay.io/jupyter/docker-stacks-foundation with args {'detach': True, 'tty': True, 'command': ['bash', '-c', 'sleep infinity']} ... (conftest.py:99)
    # 2024-01-21 17:46:44 [    INFO] Grabbing the list of manually requested packages ... (package_helper.py:83)
    # -------------------------------- live log call ---------------------------------
    # 2024-01-21 17:46:44 [    INFO] Testing the import of packages ... (test_packages.py:151)
    # 2024-01-21 17:46:44 [    INFO] Trying to import mamba (test_packages.py:153)
    # 2024-01-21 17:46:44 [    INFO] Trying to import jupyter_core (test_packages.py:153)
    PASSED                                                                   [ 17%]
    # ------------------------------ live log teardown -------------------------------
    # [...]

"""

import logging
from collections.abc import Callable, Iterable

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
    "conda-forge::blas=*",
    "grpcio-status",
    "grpcio",
    "hdf5",
    "jupyterhub-singleuser",
    "jupyterlab-git",
    "mamba",
    "notebook>",
    "openssl",
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
def requested_packages(package_helper: CondaPackageHelper) -> dict[str, set[str]]:
    """Return the list of requested packages (i.e. packages explicitly installed excluding dependencies)"""
    return package_helper.requested_packages()


def is_r_package(package: str) -> bool:
    """Check if a package is an R package"""
    return package.startswith("r-")


def get_package_import_name(package: str) -> str:
    """Perform a mapping between the package name and the name used for the import"""
    if is_r_package(package):
        package = package[2:]
    return PACKAGE_MAPPING.get(package, package)


def _check_import_package(
    package_helper: CondaPackageHelper, command: list[str]
) -> None:
    """Generic function executing a command"""
    LOGGER.debug(f"Trying to import a package with [{command}] ...")
    exec_result = package_helper.running_container.exec_run(command)
    assert exec_result.exit_code == 0, exec_result.output.decode("utf-8")


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
    since pytest prevents the use of multiple yields
    """
    failed_imports = []
    LOGGER.info("Testing the import of packages ...")
    for package in packages_to_check:
        LOGGER.info(f"Trying to import {package}")
        try:
            check_function(package_helper, package)
        except AssertionError as err:
            failed_imports.append(package)
            LOGGER.error(f"Failed to import package: {package}, output:\n  {err}")
    if failed_imports:
        pytest.fail(f"following packages are not import-able: {failed_imports}")


@pytest.fixture(scope="function")
def r_packages(requested_packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of R packages"""
    return (
        get_package_import_name(pkg)
        for pkg in requested_packages
        if is_r_package(pkg) and pkg not in EXCLUDED_PACKAGES
    )


def test_r_packages(
    package_helper: CondaPackageHelper, r_packages: Iterable[str]
) -> None:
    """Test the import of specified R packages"""
    _check_import_packages(package_helper, r_packages, check_import_r_package)


@pytest.fixture(scope="function")
def python_packages(requested_packages: dict[str, set[str]]) -> Iterable[str]:
    """Return an iterable of Python packages"""
    return (
        get_package_import_name(pkg)
        for pkg in requested_packages
        if not is_r_package(pkg) and pkg not in EXCLUDED_PACKAGES
    )


def test_python_packages(
    package_helper: CondaPackageHelper,
    python_packages: Iterable[str],
) -> None:
    """Test the import of specified python packages"""
    _check_import_packages(package_helper, python_packages, check_import_python_package)
