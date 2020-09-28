# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
test_packages
~~~~~~~~~~~~~~~
This test module tests if R and Python packages installed can be imported.
It's a basic test aiming to prove that the package is working properly.

The goal is to detect import errors that can be caused by incompatibilities between packages for example:

- #1012: issue importing `sympy`
- #966: isssue importing `pyarrow`

This module checks dynmamically, through the `CondaPackageHelper`, only the specified packages i.e. packages requested by `conda install` in the `Dockerfiles`.
This means that it does not check dependencies. This choice is a tradeoff to cover the main requirements while achieving reasonable test duration.
However it could be easily changed (or completed) to cover also dependencies `package_helper.installed_packages()` instead of `package_helper.specified_packages()`.

Example:

    $ make test/datascience-notebook

    # [...]
    # test/test_packages.py::test_python_packages
    # --------------------------------------------------------------------------------------------- live log setup ----------------------------------------------------------------------------------------------
    # 2020-03-08 09:56:04 [    INFO] Starting container jupyter/datascience-notebook ... (helpers.py:51)
    # 2020-03-08 09:56:04 [    INFO] Running jupyter/datascience-notebook with args {'detach': True, 'ports': {'8888/tcp': 8888}, 'tty': True, 'command': ['start.sh', 'bash', '-c', 'sleep infinity']} ... (conftest.py:78)
    # 2020-03-08 09:56:04 [    INFO] Grabing the list of specifications ... (helpers.py:76)
    # ---------------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------------
    # 2020-03-08 09:56:07 [    INFO] Testing the import of packages ... (test_packages.py:125)
    # 2020-03-08 09:56:07 [    INFO] Trying to import conda (test_packages.py:127)
    # 2020-03-08 09:56:07 [    INFO] Trying to import notebook (test_packages.py:127)
    # 2020-03-08 09:56:08 [    INFO] Trying to import jupyterhub (test_packages.py:127)
    # [...]

"""

import logging

import pytest

from helpers import CondaPackageHelper

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
    "tini",
    "python",
    "hdf5",
    "conda-forge::blas[build=openblas]",
    "protobuf",
    "r-irkernel",
    "unixodbc",
]


@pytest.fixture(scope="function")
def package_helper(container):
    """Return a package helper object that can be used to perform tests on installed packages"""
    return CondaPackageHelper(container)


@pytest.fixture(scope="function")
def packages(package_helper):
    """Return the list of specified packages (i.e. packages explicitely installed excluding dependencies)"""
    return package_helper.specified_packages()


def package_map(package):
    """Perform a mapping between the python package name and the name used for the import"""
    _package = package
    if _package in PACKAGE_MAPPING:
        _package = PACKAGE_MAPPING.get(_package)
    return _package


def excluded_package_predicate(package):
    """Return whether a package is excluded from the list (i.e. a package that cannot be tested with standard imports)"""
    return package in EXCLUDED_PACKAGES


def python_package_predicate(package):
    """Predicate matching python packages"""
    return not excluded_package_predicate(package) and not r_package_predicate(package)


def r_package_predicate(package):
    """Predicate matching R packages"""
    return not excluded_package_predicate(package) and package.startswith("r-")


def _check_import_package(package_helper, command):
    """Generic function executing a command"""
    LOGGER.debug(f"Trying to import a package with [{command}] ...")
    rc = package_helper.running_container.exec_run(command)
    return rc.exit_code


def check_import_python_package(package_helper, package):
    """Try to import a Python package from the command line"""
    return _check_import_package(package_helper, ["python", "-c", f"import {package}"])


def check_import_r_package(package_helper, package):
    """Try to import a R package from the command line"""
    return _check_import_package(
        package_helper, ["R", "--slave", "-e", f"library({package})"]
    )


def _import_packages(package_helper, filtered_packages, check_function, max_failures):
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
def r_packages(packages):
    """Return an iterable of R packages"""
    # package[2:] is to remove the leading "r-" appended by conda on R packages
    return map(
        lambda package: package_map(package[2:]), filter(r_package_predicate, packages)
    )


def test_python_packages(package_helper, python_packages, max_failures=0):
    """Test the import of specified python packages"""
    return _import_packages(
        package_helper, python_packages, check_import_python_package, max_failures
    )


@pytest.fixture(scope="function")
def python_packages(packages):
    """Return an iterable of Python packages"""
    return map(package_map, filter(python_package_predicate, packages))


def test_r_packages(package_helper, r_packages, max_failures=0):
    """Test the import of specified R packages"""
    return _import_packages(
        package_helper, r_packages, check_import_r_package, max_failures
    )
