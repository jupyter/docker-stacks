# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from git_helper import GitHelper
from docker_runner import DockerRunner


logger = logging.getLogger(__name__)


def _get_program_version(short_image_name, owner, program):
    image = f"{owner}/{short_image_name}:latest"
    cmd = f"{program} --version"
    with DockerRunner(image) as cont:
        logger.info(f"Running cmd: '{cmd}' on image: {image}")
        # exit code doesn't have to be 0, so we won't check it
        return cont.exec_run(cmd).output.decode("utf-8").strip()


class TaggerInterface:
    """HooksInterface for all hooks common interface"""
    @staticmethod
    def tag_value(image):
        raise NotImplementedError


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return GitHelper.commit_hash()[:12]


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "python-" + _get_program_version(short_image_name, owner, "python").split()[1]


class JupyterNotebookVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "notebook-" + _get_program_version(short_image_name, owner, "jupyter-notebook")


class JupyterLabVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "lab-" + _get_program_version(short_image_name, owner, "jupyter-lab")


class JupyterHubVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "hub-" + _get_program_version(short_image_name, owner, "jupyterhub")


class RVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "r-" + _get_program_version(short_image_name, owner, "R")


class TensorflowVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "tensorflow-" + _get_program_version(short_image_name, owner, "tensorflow")


class JuliaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "julia-" + _get_program_version(short_image_name, owner, "julia")


class SparkVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "spark-" + _get_program_version(short_image_name, owner, "spark")


class HadoopVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "hadoop-" + _get_program_version(short_image_name, owner, "hadoop")


class JavaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "java-" + _get_program_version(short_image_name, owner, "java")
