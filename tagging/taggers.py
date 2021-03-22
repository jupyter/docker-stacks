# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from git_helper import GitHelper
from docker_runner import run_simple_command


logger = logging.getLogger(__name__)


def _get_program_version(container, program):
    return run_simple_command(container, f"{program} --version")


def _get_env_variable(container, variable):
    env = run_simple_command(container, "env").split()
    for env_entry in env:
        if env_entry.startswith(variable):
            return env_entry[len(variable) + 1:]
    raise KeyError(variable)


class TaggerInterface:
    """HooksInterface for all hooks common interface"""
    @staticmethod
    def tag_value(container):
        raise NotImplementedError


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return GitHelper.commit_hash()[:12]


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "python-" + _get_program_version(container, "python").split()[1]


class JupyterNotebookVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "notebook-" + _get_program_version(container, "jupyter-notebook")


class JupyterLabVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "lab-" + _get_program_version(container, "jupyter-lab")


class JupyterHubVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "hub-" + _get_program_version(container, "jupyterhub")


class RVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "r-" + _get_program_version(container, "R")


class TensorflowVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "tensorflow-" + _get_program_version(container, "tensorflow")


class JuliaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "julia-" + _get_program_version(container, "julia")


class SparkVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "spark-" + _get_env_variable(container, "APACHE_SPARK_VERSION")


class HadoopVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "hadoop-" + _get_env_variable(container, "HADOOP_VERSION")


class JavaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container):
        return "java-" + _get_program_version(container, "java").split()[1]
