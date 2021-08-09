# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from datetime import datetime
import logging
from .git_helper import GitHelper
from .docker_runner import DockerRunner


logger = logging.getLogger(__name__)


def _get_program_version(container, program: str) -> str:
    return DockerRunner.run_simple_command(container, cmd=f"{program} --version")


def _get_env_variable(container, variable: str) -> str:
    env = DockerRunner.run_simple_command(
        container,
        cmd="env",
        print_result=False,
    ).split()
    for env_entry in env:
        if env_entry.startswith(variable):
            return env_entry[len(variable) + 1 :]
    raise KeyError(variable)


def _get_pip_package_version(container, package: str) -> str:
    VERSION_PREFIX = "Version: "
    package_info = DockerRunner.run_simple_command(
        container,
        cmd=f"pip show {package}",
        print_result=False,
    )
    version_line = package_info.split("\n")[1]
    assert version_line.startswith(VERSION_PREFIX)
    return version_line[len(VERSION_PREFIX) :]


class TaggerInterface:
    """Common interface for all taggers"""

    @staticmethod
    def tag_value(container) -> str:
        raise NotImplementedError


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return GitHelper.commit_hash_tag()


class DateTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return datetime.utcnow().strftime("%Y-%m-%d")


class UbuntuVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        os_release = DockerRunner.run_simple_command(
            container,
            "cat /etc/os-release",
        ).split("\n")
        for line in os_release:
            if line.startswith("VERSION_ID"):
                return "ubuntu-" + line.split("=")[1].strip('"')


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "python-" + _get_program_version(container, "python").split()[1]


class JupyterNotebookVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "notebook-" + _get_program_version(container, "jupyter-notebook")


class JupyterLabVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "lab-" + _get_program_version(container, "jupyter-lab")


class JupyterHubVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "hub-" + _get_program_version(container, "jupyterhub")


class RVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "r-" + _get_program_version(container, "R").split()[2]


class TensorflowVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "tensorflow-" + _get_pip_package_version(container, "tensorflow")


class JuliaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "julia-" + _get_program_version(container, "julia").split()[2]


class SparkVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "spark-" + _get_env_variable(container, "APACHE_SPARK_VERSION")


class HadoopVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "hadoop-" + _get_env_variable(container, "HADOOP_VERSION")


class JavaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return "java-" + _get_program_version(container, "java").split()[1]
