# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime

from docker.models.containers import Container


def date_tagger(container: Container) -> str:
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
