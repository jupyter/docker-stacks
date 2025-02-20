import argparse


def common_arguments_parser(
    registry: bool = True,
    owner: bool = True,
    short_image_name: bool = True,
    variant: bool = True,
) -> argparse.ArgumentParser:
    """Add common CLI arguments to parser"""

    parser = argparse.ArgumentParser()
    if registry:
        parser.add_argument(
            "--registry",
            required=True,
            choices=["docker.io", "quay.io"],
            help="Image registry",
        )
    if owner:
        parser.add_argument(
            "--owner",
            required=True,
            help="Owner of the image",
        )
    if short_image_name:
        parser.add_argument(
            "--short-image-name",
            required=True,
            help="Short image name",
        )
    if variant:
        parser.add_argument(
            "--variant",
            required=True,
            help="Variant tag prefix",
        )

    return parser
