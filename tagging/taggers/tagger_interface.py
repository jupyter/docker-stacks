# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container


class TaggerInterface:
    """Common interface for all taggers"""

    @staticmethod
    def tag_value(container: Container) -> str:
        raise NotImplementedError
