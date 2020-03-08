# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging

import pytest

from helpers import CondaPackageHelper

LOGGER = logging.getLogger(__name__)

# Mapping between package and module name
PYTHON_PACKAGE_MAPPING = {
    "matplotlib-base": "matplotlib",
    "beautifulsoup4": "bs4",
    "scikit-learn": "sklearn",
    "scikit-image": "skimage",
}

R_PACKAGE_MAPPING = {"randomforest": "randomForest", "rsqlite": "DBI", "rcurl": "RCurl"}

# List of packages that cannot be tested in a standard way
EXCLUDED_PACKAGES = [
    "tini",
    "python",
    "hdf5",
    "conda-forge::blas[build",
    "protobuf",
    "r-irkernel",
]


@pytest.fixture(scope="function")
def package_helper(container):
    """Return a package helper object that can be used to perform tests on installed packages"""
    return CondaPackageHelper(container)


@pytest.fixture(scope="function")
def packages(package_helper):
    return package_helper.specified_packages()


def excluded_package_predicate(package):
    """Return whether a package is excluded from the list (i.e. a package that cannot be tested with standard imports)"""
    return package in EXCLUDED_PACKAGES


def python_package_predicate(package):
    # return x not in block_list and x in accept_list and is_good(x)
    return not excluded_package_predicate(package) and not r_package_predicate(package)


def python_package_map(package):
    """Perform a mapping between the python package name and the name used for the import"""
    _package = package
    if _package in PYTHON_PACKAGE_MAPPING:
        _package = PYTHON_PACKAGE_MAPPING.get(_package)
    return _package


def r_package_predicate(package):
    return not excluded_package_predicate(package) and package.startswith("r-")


# TODO: Refactoring
def r_package_map(package):
    """Perform a mapping between the R package name and the name used for the import"""
    # Removing the leading "r-"
    _package = package[2:]
    if _package in R_PACKAGE_MAPPING:
        _package = R_PACKAGE_MAPPING.get(_package)
    return _package


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


def _import_packages(package_helper, filtered_packages, check_function):
    """Test if packages can be imported
    
    Note: using a list of packages instead of a fixture for the list of packages since pytest prevent to use multiple yields
    """
    failures = {}
    LOGGER.info(f"Testing the import of packages ...")
    for package in filtered_packages:
        LOGGER.info(f"Trying to import {package}")
        try:
            assert (
                check_function(package_helper, package) == 0
            ), f"Package [{package}] import failed"
        except AssertionError as err:
            failures[package] = err
    if failures:
        raise AssertionError(failures)


@pytest.fixture(scope="function")
def r_packages(packages):
    return map(r_package_map, filter(r_package_predicate, packages))


def test_python_packages(package_helper, python_packages):
    """Test the import of specified python packages"""
    return _import_packages(
        package_helper, python_packages, check_import_python_package
    )


@pytest.fixture(scope="function")
def python_packages(packages):
    return map(python_package_map, filter(python_package_predicate, packages))


def test_r_packages(package_helper, r_packages):
    """Test the import of specified R packages"""
    return _import_packages(package_helper, r_packages, check_import_r_package)
