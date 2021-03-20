# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagger_interface import TaggerInterface
from git_helper import GitHelper
from plumbum.cmd import docker


def _get_full_name(short_image_name, owner):
    return f"{owner}/{short_image_name}:latest"


def _get_program_version(short_image_name, owner, program):
    return docker[
        "run",
        "--rm",
        "-a", "STDOUT",
        _get_full_name(short_image_name, owner),
        program, "--version"
    ]().strip()


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
