# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from collections.abc import Callable

from docker.models.containers import Container

TaggerInterface = Callable[[Container], str]
