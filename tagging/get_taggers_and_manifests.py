# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from .images_hierarchy import ALL_IMAGES
from .manifests import ManifestInterface
from .taggers import TaggerInterface


def get_taggers_and_manifests(
    short_image_name: str,
) -> tuple[list[TaggerInterface], list[ManifestInterface]]:
    taggers: list[TaggerInterface] = []
    manifests: list[ManifestInterface] = []
    while short_image_name is not None:
        image_description = ALL_IMAGES[short_image_name]

        taggers = image_description.taggers + taggers
        manifests = image_description.manifests + manifests

        short_image_name = image_description.parent_image
    return taggers, manifests
