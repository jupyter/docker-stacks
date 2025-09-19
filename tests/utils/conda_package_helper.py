# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# CondaPackageHelper is partially based on the work https://oerpli.github.io/post/2019/06/conda-outdated/.
# See copyright below.
#
# MIT License
# Copyright (c) 2019 Abraham Hinteregger
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import logging
import re
from collections import defaultdict
from functools import cached_property
from itertools import chain

from tabulate import tabulate

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)


class CondaPackageHelper:
    """Conda package helper permitting to get information about packages"""

    def __init__(self, container: TrackedContainer):
        self.container = container
        self.container.run_detached(command=["sleep", "infinity"])

    @cached_property
    def installed_packages(self) -> dict[str, set[str]]:
        """Return the installed packages"""
        LOGGER.info("Grabbing the list of installed packages ...")
        env_export = self.container.exec_cmd("mamba env export --no-build --json")
        return self._parse_package_versions(env_export)

    @cached_property
    def requested_packages(self) -> dict[str, set[str]]:
        """Return the requested package (i.e. `mamba install <package>`)"""
        LOGGER.info("Grabbing the list of manually requested packages ...")
        env_export = self.container.exec_cmd(
            "mamba env export --no-build --json --from-history"
        )
        return self._parse_package_versions(env_export)

    @staticmethod
    def _parse_package_versions(env_export: str) -> dict[str, set[str]]:
        """Extract packages and versions from the lines returned by the list of specifications"""
        dependencies = json.loads(env_export).get("dependencies")
        # Filtering packages installed through pip
        # since we only manage packages installed through mamba here
        # They are represented by a dict with a key 'pip'
        dependencies = filter(lambda x: isinstance(x, str), dependencies)
        packages_dict: dict[str, set[str]] = {}
        for split in map(lambda x: re.split("=?=", x), dependencies):
            # default values
            package = split[0]
            version = set()
            # This normally means we have package=version notation
            if len(split) > 1:
                # checking if it's a proper version by testing if the first char is a digit
                if split[1][0].isdigit():
                    # package + version case
                    version = set(split[1:])
                # The split was incorrect and the package shall not be split
                else:
                    package = f"{split[0]}={split[1]}"
            packages_dict[package] = version
        return packages_dict

    @cached_property
    def available_packages(self) -> dict[str, set[str]]:
        """Return the available packages"""
        LOGGER.info("Grabbing the list of available packages (can take a while) ...")
        return self._extract_available(
            self.container.exec_cmd("conda search --outdated --quiet")
        )

    @staticmethod
    def _extract_available(lines: str) -> defaultdict[str, set[str]]:
        """Extract packages and versions from the lines returned by the list of packages"""
        ddict = defaultdict(set)
        for line in lines.splitlines()[2:]:
            match = re.match(r"^(\S+)\s+(\S+)", line, re.MULTILINE)
            assert match is not None
            pkg, version = match.groups()
            ddict[pkg].add(version)
        return ddict

    def find_updatable_packages(self, requested_only: bool) -> list[dict[str, str]]:
        """Check the updatable packages including or not dependencies"""
        updatable = []
        for pkg, inst_vs in self.installed_packages.items():
            avail_vs = self.available_packages[pkg]
            if not avail_vs or (requested_only and pkg not in self.requested_packages):
                continue
            newest = max(avail_vs, key=CondaPackageHelper.semantic_cmp)
            current = min(inst_vs, key=CondaPackageHelper.semantic_cmp)
            if CondaPackageHelper.semantic_cmp(
                current
            ) < CondaPackageHelper.semantic_cmp(newest):
                updatable.append({"Package": pkg, "Current": current, "Newest": newest})
        return updatable

    @staticmethod
    def semantic_cmp(version_string: str) -> tuple[int, ...]:
        """Manage semantic versioning for comparison"""

        def my_split(string: str) -> list[list[str]]:
            def version_substrs(x: str) -> list[str]:
                return re.findall(r"([A-Za-z]+|\d+)", x)

            return list(chain(map(version_substrs, string.split("."))))

        def str_ord(string: str) -> int:
            num = 0
            for char in string:
                num *= 255
                num += ord(char)
            return num

        def try_int(version_str: str) -> int:
            try:
                return int(version_str)
            except ValueError:
                return str_ord(version_str)

        mss = list(chain(*my_split(version_string)))
        return tuple(map(try_int, mss))

    def get_outdated_summary(
        self, updatable: list[dict[str, str]], requested_only: bool
    ) -> str:
        """Return a summary of outdated packages"""
        packages = (
            self.requested_packages if requested_only else self.installed_packages
        )
        nb_packages = len(packages)
        nb_updatable = len(updatable)
        updatable_ratio = nb_updatable / nb_packages
        return f"{nb_updatable}/{nb_packages} ({updatable_ratio:.0%}) packages could be updated"

    def get_outdated_table(self, updatable: list[dict[str, str]]) -> str:
        """Return a table of outdated packages"""
        return tabulate(updatable, headers="keys")
