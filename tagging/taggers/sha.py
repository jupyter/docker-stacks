# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.utils.git_helper import GitHelper


def commit_sha_tagger(container: Container) -> str:
    return GitHelper.commit_hash_tag()
