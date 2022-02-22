# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import subprocess
from pathlib import Path

import doit
import doit.tools

# global doit config
DOIT_CONFIG = {"verbosity": 2, "default_tasks": ["build_docs"]}


# dependencies: input to the task execution -> keeps tracks of the state of file dependencies and saves the signature of them every time the tasks are run so if there are no modifications to the files the execution of the task is skipped  (indicated by -- after running doit)
# target: output produces by the task execution

# -----------------------------------------------------------------------------
# Documentation and wiki tasks
# -----------------------------------------------------------------------------


def task_build_docs():
    """Build Sphinx documentation 📝
    setting uptodate to False will force the task to run every time
    """

    return dict(
        file_dep=[*P.DOCS_MD, *P.DOCS_RST, *P.DOCS_PY],
        actions=[U.do("sphinx-build", "-W", P.DOCS, "docs/_build/html")],
        targets=[P.DOCS_TARGET],
        uptodate=[False],
    )


# https://pydoit.org/task-creation.html#delayed-task-creation
@doit.create_after(executed="build_docs")
def task_docs_check_links():
    """Checks for any broken links in the Sphinx documentation 🔗
    only created after the docs are built"""
    return dict(
        file_dep=[*P.DOCS.rglob("_build/*.html")],
        actions=[
            U.do(
                "sphinx-build",
                "-W",
                "--keep-going",
                "--color",
                "-b",
                "linkcheck",
                P.DOCS,
                "docs/_build",
            )
        ],
    )


# -----------------------------------------------------------------------------
# Docker related tasks
# -----------------------------------------------------------------------------


def task_docker_build():
    """Build Docker images using the system's architecture"""
    for image in P.ALL_IMAGES:

        image_tags, image_dir, dockerfile, tar_file = U.image_meta(image)

        yield dict(
            name=f"build:{image}",
            doc="Build the latest image for a stack using the system's acrchitecture ⛏",
            actions=[
                U.do(
                    "echo",
                    f"::group::Build {P.OWNER}/{image}- using system's architecture",
                ),
                U.do(
                    "docker",
                    "buildx",
                    "build",
                    *["-t" + tag for tag in image_tags],
                    "-f",
                    dockerfile,
                    "--build-arg",
                    "OWNER=" + P.OWNER,
                    str(image_dir),
                    "--load",
                ),
            ],
            file_dep=[dockerfile],
            uptodate=[False],
        )

        yield dict(
            name=f"build_summary:{image}",
            doc="Brief summary of the image built - defaulting to using the latest tag",
            actions=[
                ["echo", "\n \n ⚡️ Build complete, image size:"],
                U.do("docker", "images", image_tags[0], "--format", "{{.Size}}"),
                U.do("echo", "::endgroup::"),
            ],
        )


def task_docker_save_images():
    """Save the built Docker images - these will be stored as CI artifacts"""
    if U.IS_CI:
        ci_img_tar = P.CI_IMG / f"docker_images_{U.GIT_COMMIT_SHA}.tar"

        return dict(
            targets=[ci_img_tar],
            actions=[
                U.do("echo", f"Saving images to: {P.CI_IMG}"),
                U.do("mkdir", "-p", P.CI_IMG),
                U.do(
                    "docker",
                    "save",
                    "$(docker images -q)",
                    "-o",
                    str(ci_img_tar),
                ),
            ],
        )


def task_docker_test():
    """Test Docker images - need to be run after `docker_build`"""
    for image in P.ALL_IMAGES:

        image_tags, image_dir, dockerfile, tar_file = U.image_meta(image)

        if U.IS_CI:
            yield dict(
                name=f"load:{image}",
                doc="Load and inspect the image - this ensures it is available for docker commands",
                actions=[
                    (U.do("docker", "load", "--input", tar_file)),
                    (U.inspect_image, [image_tags[0]]),
                ],
            )

        yield dict(
            name=f"test:{image}",
            doc="Run tests for images",
            uptodate=[False],
            actions=[
                (U.set_env, [f"{P.OWNER}/{image}"]),
                (U.do(*U.PYTEST_ARGS)),
            ],
        )


def task_docker_create_manifest():
    """Build the manifest file and tags for the Docker images 🏷 - can be run in parallel to the build stage"""
    for image in P.ALL_IMAGES:

        yield dict(
            name=f"tags:{image}",
            doc="Create tags for the images",
            actions=[
                U.do(
                    *U.PYM,
                    "tagging.tag_image",
                    "--short-image-name",
                    image,
                    "--owner",
                    P.OWNER,
                ),
            ],
        )

        yield dict(
            name=f"manifest:{image}",
            doc="Create the manifest file for the images",
            targets=[P.WIKI_MANIFEST / f"{image}-{U.GIT_COMMIT_HASH_TAG}.md"],
            actions=[
                U.do(
                    *U.PYM,
                    "tagging.create_manifests",
                    "--short-image-name",
                    image,
                    "--owner",
                    P.OWNER,
                    "--wiki-path",
                    P.WIKI,
                )
            ],
        )


def task_docker_push_image():
    """Push all tags for a Jupyter image - only should be done after they have been tested"""
    # TODO: need to add a flag to identify the registry to which we are pushing as need to preped gchr.io accordingly
    for image in P.ALL_IMAGES:

        yield dict(
            name=f"push:{image}",
            doc="Push the image to the specified registry",
            actions=[
                U.do(
                    "echo",
                    f"::group::Push {P.OWNER}/{image}- system's architecture",
                ),
                U.do("docker", "push", "--all-tags", f"{P.OWNER}/{image}"),
                U.do("echo", "::endgroup::"),
            ],
        )


# -----------------------------------------------------------------------------
# Support classes and methods
# -----------------------------------------------------------------------------


class P:
    """Paths to project files and directories, used to provide consistency across the multiple doit tasks"""

    DODO = Path(__file__)
    ROOT = DODO.parent

    # docs
    DOCS = ROOT / "docs"
    DOCS_TARGET = ROOT / "docs/_build/html"
    README = ROOT / "README.md"
    DOCS_PY = sorted(DOCS.rglob("*.py"))
    DOCS_RST = sorted(DOCS.rglob("*.rst"))
    DOCS_SRC_MD = sorted(DOCS.rglob("*.md"))
    DOCS_MD = sorted([*DOCS_SRC_MD, README])

    # wiki
    WIKI = ROOT.parent / "wiki"
    WIKI_MANIFEST = WIKI / "manifests"

    # tests
    TESTS = ROOT / "tests"

    # CI
    CI = ROOT / ".github"
    CI_IMG = CI / "built_docker_images"

    # Docker-related
    # Images supporting the following architectures:
    # - linux/amd64
    # - linux/arm64
    MULTI_IMAGES = [
        "base-notebook",
        "minimal-notebook",
        "scipy-notebook",
        "r-notebook",
        "pyspark-notebook",
        "all-spark-notebook",
    ]

    # TODO: uncomment after initial tests
    # ALL_IMAGES = [
    #     "base-notebook",
    #     "minimal-notebook",
    #     "scipy-notebook",
    #     "r-notebook",
    #     "tensorflow-notebook",
    #     "datascience-notebook",
    #     "pyspark-notebook",
    #     "all-spark-notebook",
    # ]
    ALL_IMAGES = [
        "base-notebook",
        "minimal-notebook",
    ]

    AMD64_IMAGES = ["datascience-notebook", "tensorflow-notebook"]

    OWNER = "jupyter"


class U:
    """Supporting methods and variables"""

    @staticmethod
    def do(*args, cwd=P.ROOT, **kwargs):
        """wrap a CmdAction for consistency across OS"""
        return doit.tools.CmdAction(list(args), shell=False, cwd=str(Path(cwd)))

    # CI specific
    IS_CI = bool(os.environ.get("CI", 0))

    # args
    PYTEST_ARGS = ["pytest", "-m", "not info", "test"]
    PYM = ["python", "-m"]
    PIP = [*PYM, "pip"]

    # git specific - used for tagging
    SOURCE_DATE_EPOCH = (
        subprocess.check_output(["git", "log", "-1", "--format=%ct"])
        .decode("utf-8")
        .strip()
    )

    GIT_COMMIT_SHA = (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("utf-8")
        .strip()
    )

    GIT_COMMIT_HASH_TAG = (
        subprocess.check_output(["git", "rev-parse", "HEAD"])
        .decode("utf-8")
        .strip()[:12]
    )

    # utility methods
    @staticmethod
    def image_meta(image):
        """Get the image tags and other supporting meta for building, testing and tagging"""
        tags = [
            f"{P.OWNER}/{image}:latest",
            f"{P.OWNER}/{image}:{U.GIT_COMMIT_SHA}_{U.SOURCE_DATE_EPOCH}",
        ]
        image_dir = P.ROOT / image
        dockerfile = str(image_dir / "Dockerfile")
        tar_file = str(P.CI_IMG / image / f"{image}-{U.GIT_COMMIT_SHA}.tar")

        return tags, image_dir, dockerfile, tar_file

    @staticmethod
    def set_env(image):
        """We need this env variable later on for the tests"""
        os.environ["TEST_IMAGE"] = image
        print(os.environ.get("TEST_IMAGE"))

    @staticmethod
    def inspect_image(image):
        """Since we are sharing artifacts across jobs we need to make sure that these are loaded properly. The easies way to check this is to run `docker inspect` on the image"""
        try:
            subprocess.check_call(
                ["docker", "image", "inspect", image], stdout=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            print(f"Image not found: {image}")
