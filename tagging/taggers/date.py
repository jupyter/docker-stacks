# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime

from docker.models.containers import Container

from tagging.taggers.tagger_interface import TaggerInterface


class DateTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
