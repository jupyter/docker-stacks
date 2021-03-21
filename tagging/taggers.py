# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from tagger_interface import TaggerInterface
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


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return GitHelper.commit_hash()[:12]

    @staticmethod
    def tag_name():
        return "git_sha"


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "python-" + _get_program_version(short_image_name, owner, "python").split()[1]

    @staticmethod
    def tag_name():
        return "python_version"


class JupyterNotebookVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "notebook-" + _get_program_version(short_image_name, owner, "jupyter-notebook")

    @staticmethod
    def tag_name():
        return "jupyter_notebook_version"


class JupyterLabVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "lab-" + _get_program_version(short_image_name, owner, "jupyter-lab")

    @staticmethod
    def tag_name():
        return "jupyter_lab_version"


class JupyterHubVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(short_image_name, owner):
        return "hub-" + _get_program_version(short_image_name, owner, "jupyterhub")

    @staticmethod
    def tag_name():
        return "jupyter_lab_version"
