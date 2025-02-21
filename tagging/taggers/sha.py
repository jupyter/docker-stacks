# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.taggers.tagger_interface import TaggerInterface
from tagging.utils.git_helper import GitHelper


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return GitHelper.commit_hash_tag()
