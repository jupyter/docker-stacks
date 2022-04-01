#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging

import plumbum
from images_hierarchy import get_test_dirs

pytest = plumbum.local["pytest"]

LOGGER = logging.getLogger(__name__)


def test_image(short_image_name: str, owner: str) -> None:
    LOGGER.info(f"Testing image: {short_image_name}")
    test_dirs = get_test_dirs(short_image_name)
    LOGGER.info(f"Test dirs to be run: {test_dirs}")
    with plumbum.local.env(TEST_IMAGE=f"{owner}/{short_image_name}"):
        (
            pytest[
                "--numprocesses",
                "auto",
                "-m",
                "not info",
                test_dirs,
            ]
            & plumbum.FG
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--short-image-name",
        required=True,
        help="Short image name to run test on",
    )
    arg_parser.add_argument("--owner", required=True, help="Owner of the image")

    args = arg_parser.parse_args()

    test_image(args.short_image_name, args.owner)
