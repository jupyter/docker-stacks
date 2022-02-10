from pathlib import Path

import doit
import doit.tools

# global doit config
DOIT_CONFIG = {"verbosity": 2, "default_tasks": ["build_docker"]}


# dependencies: input to the task execution -> keeps tracks of the state of file dependencies and saves the signature of them every time the tasks are run so if there are no modifications to the files the execution of the task is skipped  (indicated by -- after running doit)
# target: output produces by the task execution

# -----------------------------------------------------------------------------
# Documentation and wiki tasks
# -----------------------------------------------------------------------------


def task_docs():
    """Build Sphinx documentation 📝"""

    yield dict(
        name="docs:build",
        file_dep=[*P.DOCS_MD, *P.DOCS_RST, *P.DOCS_PY],
        actions=[U.do("sphinx-build", "-W", P.DOCS, "docs/_build/html")],
        targets=["_build/"],
        uptodate=[False],
    )


@doit.create_after("docs")
def task_check():
    """Checks for any broken links in the Sphinx documentation 🔗"""
    yield dict(
        name="docs:links",
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
# Docker related
# -----------------------------------------------------------------------------


def task_build_docker():
    """Build Docker images for system's architecture ⛏"""
    for image in P.TEST_IMAGES:
        tag = f"{P.OWNER}/{image}:latest"
        dockerfile = P.ROOT / image / "Dockerfile"

        yield dict(
            name="(system's architecture): " + image,
            actions=[
                U.do(
                    "docker",
                    "buildx",
                    "build",
                    "-t",
                    str(tag),
                    str(P.ROOT / image),
                    "--build-arg",
                    "OWNER=" + P.OWNER,
                )
            ],
            file_dep=[dockerfile],
            targets=[image],
            uptodate=[False],
        )


# -----------------------------------------------------------------------------
# Support classes
# -----------------------------------------------------------------------------


class P:
    """Paths to project files and directories, used to provide consistency across the multiple doit tasks"""

    DODO = Path(__file__)
    ROOT = DODO.parent

    # docs
    DOCS = ROOT / "docs"
    README = ROOT / "README.md"
    DOCS_PY = sorted(DOCS.rglob("*.py"))
    DOCS_RST = sorted(DOCS.rglob("*.rst"))
    DOCS_SRC_MD = sorted(DOCS.rglob("*.md"))
    DOCS_MD = sorted([*DOCS_SRC_MD, README])

    TESTS = ROOT / "tests"
    SCRIPTS = ROOT / "scripts"
    TAGGING = ROOT / "tagging"

    # CI
    CI = ROOT / ".github"

    # Images supporting the following architectures:
    # - linux/amd64
    # - linux/arm64
    MULTI_IMAGES = [
        "base-notebook",
        "minimal-notebook",
        "pyspark-notebook",
        "r-notebook",
        "scipy-notebook",
        "all-spark-notebook",
    ]
    AMD64_IMAGES = ["datascience-notebook", "tensorflow-notebook"]
    ALL_IMAGES = MULTI_IMAGES + AMD64_IMAGES
    TEST_IMAGES = ["base-notebook"]

    OWNER = "jupyter"


class U:
    """Supporting methods (a.k.a utilities)"""

    @staticmethod
    def do(*args, cwd=P.ROOT, **kwargs):
        """wrap a CmdAction for consistency across OS"""
        return doit.tools.CmdAction(list(args), shell=False, cwd=str(Path(cwd)))
