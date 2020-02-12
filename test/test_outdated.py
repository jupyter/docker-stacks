"""
Based on the work https://oerpli.github.io/post/2019/06/conda-outdated/.
See copyright below.

MIT License
Copyright (c) 2019 Abraham Hinteregger
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import subprocess
from collections import defaultdict
from itertools import chain
import logging

import pytest

from tabulate import tabulate

LOGGER = logging.getLogger(__name__)


def get_versions(lines):
    """Extract versions from the lines"""
    ddict = defaultdict(set)
    for line in lines.splitlines()[2:]:
        pkg, version = re.match(r"^(\S+)\s+(\S+)", line, re.MULTILINE).groups()
        ddict[pkg].add(version)
    return ddict


def semantic_cmp(version_string):
    """Manage semantic versioning for comparison"""

    def mysplit(string):
        version_substrs = lambda x: re.findall(r"([A-z]+|\d+)", x)
        return list(chain(map(version_substrs, string.split("."))))

    def str_ord(string):
        num = 0
        for char in string:
            num *= 255
            num += ord(char)
        return num

    def try_int(version_str):
        try:
            return int(version_str)
        except ValueError:
            return str_ord(version_str)

    mss = list(chain(*mysplit(version_string)))
    return tuple(map(try_int, mss))


def print_result(installed, result):
    """Print the result of the outdated check"""
    nb_packages = len(installed)
    nb_updatable = len(result)
    updatable_ratio = nb_updatable / nb_packages
    LOGGER.info(
        f"{nb_updatable} packages can be updated over {nb_packages} -> {updatable_ratio:.0%}"
    )
    LOGGER.info(f"\n{tabulate(result, headers='keys')}\n")


@pytest.mark.info
def test_outdated_packages(container):
    """Getting the list of outdated packages"""
    LOGGER.info(f"Checking outdated packages in {container.image_name} ...")
    c = container.run(tty=True, command=["start.sh", "bash", "-c", "sleep infinity"])
    sp_i = c.exec_run(["conda", "list"])
    sp_v = c.exec_run(["conda", "search", "--outdated"])
    installed = get_versions(sp_i.output.decode("utf-8"))
    available = get_versions(sp_v.output.decode("utf-8"))
    result = list()
    for pkg, inst_vs in installed.items():
        avail_vs = sorted(list(available[pkg]), key=semantic_cmp)
        if not avail_vs:
            continue
        current = min(inst_vs, key=semantic_cmp)
        newest = avail_vs[-1]
        if avail_vs and current != newest:
            if semantic_cmp(current) < semantic_cmp(newest):
                result.append({"Package": pkg, "Current": current, "Newest": newest})
    print_result(installed, result)
