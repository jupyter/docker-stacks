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
from itertools import chain
from typing import Any, Optional

from docker.models.containers import Container
from tabulate import tabulate

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


class CondaPackageHelper:
    """Conda package helper permitting to get information about packages"""

    def __init__(self, container: TrackedContainer):
        self.running_container: Container = CondaPackageHelper.start_container(
            container
        )
        self.requested: Optional[dict[str, set[str]]] = None
        self.installed: Optional[dict[str, set[str]]] = None
        self.available: Optional[dict[str, set[str]]] = None
        self.comparison: list[dict[str, str]] = []

    @staticmethod
    def start_container(container: TrackedContainer) -> Container:
        """Start the TrackedContainer and return an instance of a running container"""
        LOGGER.info(f"Starting container {container.image_name} ...")
        return container.run_detached(
            tty=True,
            command=["start.sh", "bash", "-c", "sleep infinity"],
        )

    @staticmethod
    def _conda_export_command(from_history: bool) -> list[str]:
        """Return the mamba export command with or without history"""
        cmd = ["mamba", "env", "export", "-n", "base", "--json", "--no-builds"]
        if from_history:
            cmd.append("--from-history")
        return cmd

    def installed_packages(self) -> dict[str, set[str]]:
        """Return the installed packages"""
        if self.installed is None:
            LOGGER.info("Grabbing the list of installed packages ...")
            self.installed = CondaPackageHelper._packages_from_json(
                self._execute_command(
                    CondaPackageHelper._conda_export_command(from_history=False)
                )
            )
        return self.installed

    def requested_packages(self) -> dict[str, set[str]]:
        """Return the requested package (i.e. `mamba install <package>`)"""
        if self.requested is None:
            LOGGER.info("Grabbing the list of manually requested packages ...")
            self.requested = CondaPackageHelper._packages_from_json(
                self._execute_command(
                    CondaPackageHelper._conda_export_command(from_history=True)
                )
            )
        return self.requested

    def _execute_command(self, command: list[str]) -> str:
        """Execute a command on a running container"""
        rc = self.running_container.exec_run(command)
        return rc.output.decode("utf-8")  # type: ignore

    @staticmethod
    def _packages_from_json(env_export: str) -> dict[str, set[str]]:
        """Extract packages and versions from the lines returned by the list of specifications"""
        # dependencies = filter(lambda x:  isinstance(x, str), json.loads(env_export).get("dependencies"))
        dependencies = json.loads(env_export).get("dependencies")
        # Filtering packages installed through pip in this case it's a dict {'pip': ['toree==0.3.0']}
        # Since we only manage packages installed through mamba here
        dependencies = filter(lambda x: isinstance(x, str), dependencies)
        packages_dict: dict[str, set[str]] = dict()
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

    def available_packages(self) -> dict[str, set[str]]:
        """Return the available packages"""
        if self.available is None:
            LOGGER.info(
                "Grabbing the list of available packages (can take a while) ..."
            )
            # Keeping command line output since `mamba search --outdated --json` is way too long ...
            self.available = CondaPackageHelper._extract_available(
                self._execute_command(["mamba", "search", "--outdated", "--quiet"])
            )
        return self.available

    @staticmethod
    def _extract_available(lines: str) -> dict[str, set[str]]:
        """Extract packages and versions from the lines returned by the list of packages"""
        ddict = defaultdict(set)
        for line in lines.splitlines()[2:]:
            match = re.match(r"^(\S+)\s+(\S+)", line, re.MULTILINE)
            assert match is not None
            pkg, version = match.groups()
            ddict[pkg].add(version)
        return ddict

    def check_updatable_packages(
        self, requested_only: bool = True
    ) -> list[dict[str, str]]:
        """Check the updatable packages including or not dependencies"""
        requested = self.requested_packages()
        installed = self.installed_packages()
        available = self.available_packages()
        self.comparison = []
        for pkg, inst_vs in installed.items():
            if not requested_only or pkg in requested:
                avail_vs = sorted(
                    list(available[pkg]), key=CondaPackageHelper.semantic_cmp
                )
                if not avail_vs:
                    continue
                current = min(inst_vs, key=CondaPackageHelper.semantic_cmp)
                newest = avail_vs[-1]
                if (
                    avail_vs
                    and current != newest
                    and CondaPackageHelper.semantic_cmp(current)
                    < CondaPackageHelper.semantic_cmp(newest)
                ):
                    self.comparison.append(
                        {"Package": pkg, "Current": current, "Newest": newest}
                    )
        return self.comparison

    @staticmethod
    def semantic_cmp(version_string: str) -> Any:
        """Manage semantic versioning for comparison"""

        def my_split(string: str) -> list[Any]:
            def version_substrs(x: str) -> list[str]:
                return re.findall(r"([A-z]+|\d+)", x)

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

    def get_outdated_summary(self, requested_only: bool = True) -> str:
        """Return a summary of outdated packages"""
        packages = self.requested if requested_only else self.installed
        assert packages is not None
        nb_packages = len(packages)
        nb_updatable = len(self.comparison)
        updatable_ratio = nb_updatable / nb_packages
        return f"{nb_updatable}/{nb_packages} ({updatable_ratio:.0%}) packages could be updated"

    def get_outdated_table(self) -> str:
        """Return a table of outdated packages"""
        return tabulate(self.comparison, headers="keys")
