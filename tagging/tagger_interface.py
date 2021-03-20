# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


class TaggerInterface:
    """HooksInterface for all hooks common interface"""
    @staticmethod
    def tag_value(image):
        raise NotImplementedError

    @staticmethod
    def tag_name():
        raise NotImplementedError
