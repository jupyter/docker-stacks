# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from pathlib import Path

from tests.hierarchy.images_hierarchy import IMAGE_PARENT

THIS_DIR = Path(__file__).parent.resolve()
IMAGE_SPECIFIC_TESTS_DIR = THIS_DIR.parent / "by_image"

assert IMAGE_SPECIFIC_TESTS_DIR.exists(), f"{IMAGE_SPECIFIC_TESTS_DIR} does not exist."


def get_test_dirs(image: str | None) -> list[Path]:
    if image is None:
        return []

    test_dirs = get_test_dirs(IMAGE_PARENT[image])
    current_test_dir = IMAGE_SPECIFIC_TESTS_DIR / image
    assert current_test_dir.exists(), f"{current_test_dir} does not exist."
    test_dirs.append(current_test_dir)
    return test_dirs
