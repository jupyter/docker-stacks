from pathlib import Path

import doit
import doit.tools

# global doit config
DOIT_CONFIG = {"verbosity": 2}


def task_docs():
    """Build Sphinx documentation"""

    yield dict(
        name="Build Sphinx documentation",
        file_dep=[*P.DOCS_MD, *P.DOCS_RST, *P.DOCS_PY],
        # actions=["sphinx-build -W docs/ docs/_build/html"],
        actions=[f"sphinx-build -W {P.DOCS} docs/_build/html"],
        targets=["_build/"],
        uptodate=[False],
    )


@doit.create_after("docs")
def task_check():
    """Perform checks of built doc artifacts"""
    yield dict(
        name="docs:links",
        doc="Check for broken (internal) links",
        file_dep=[*P.DOCS.rglob("*.html")],
        actions=["sphinx-build -W --keep-going --color -b linkcheck docs/ docs/_build"],
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

    # images
    ALL_SPARK_NB = ROOT / "all-spark-notebook"
    BASE_NB = ROOT / "base-notebook"
    DATASCIENCE_NB = ROOT / "datascience-notebook"
    MINIMAL_NB = ROOT / "minimal-notebook"
    PYSPARK_NB = ROOT / "pyspark-notebook"
    R_NB = ROOT / "r-notebook"
    SCIPY_NB = ROOT / "scipy-notebook"
    TENSORFLOW_NB = ROOT / "tensorflow-notebook"
