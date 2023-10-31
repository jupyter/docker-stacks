#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import argparse
import logging

import plumbum

from tests.images_hierarchy import get_test_dirs

python3 = plumbum.local["python3"]

LOGGER = logging.getLogger(__name__)


def test_image(short_image_name: str, registry: str, owner: str) -> None:
    LOGGER.info(f"Testing image: {short_image_name}")
    test_dirs = get_test_dirs(short_image_name)
    LOGGER.info(f"Test dirs to be run: {test_dirs}")
    with plumbum.local.env(TEST_IMAGE=f"{registry}/{owner}/{short_image_name}"):
        (
            python3[
                "-m",
                "pytest",
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
    arg_parser.add_argument(
        "--registry",
        required=True,
        type=str,
        choices=["docker.io", "quay.io"],
        help="Image registry",
    )
    arg_parser.add_argument(
        "--owner",
        required=True,
        help="Owner of the image",
    )

    args = arg_parser.parse_args()

    test_image(args.short_image_name, args.registry, args.owner)
