# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.hierarchy.images_hierarchy import ALL_IMAGES
from tagging.manifests.manifest_interface import ManifestInterface


def get_manifests(image: str | None) -> list[ManifestInterface]:
    if image is None:
        return []
    image_description = ALL_IMAGES[image]
    parent_manifests = get_manifests(image_description.parent_image)
    return parent_manifests + image_description.manifests
