# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from docker.models.containers import Container

from tagging.utils.docker_runner import DockerRunner


def _get_program_version(container: Container, program: str) -> str:
    return DockerRunner.exec_cmd(container, cmd=f"{program} --version")


def _get_pip_package_version(container: Container, package: str) -> str:
    PIP_VERSION_PREFIX = "Version: "

    package_info = DockerRunner.exec_cmd(
        container,
        cmd=f"pip show {package}",
    )
    version_line = package_info.split("\n")[1]
    assert version_line.startswith(PIP_VERSION_PREFIX)
    return version_line[len(PIP_VERSION_PREFIX) :]


def python_tagger(container: Container) -> str:
    return "python-" + _get_program_version(container, "python").split()[1]


def python_major_minor_tagger(container: Container) -> str:
    full_version = python_tagger(container)
    return full_version[: full_version.rfind(".")]


def mamba_tagger(container: Container) -> str:
    return "mamba-" + _get_program_version(container, "mamba")


def conda_tagger(container: Container) -> str:
    return "conda-" + _get_program_version(container, "conda").split()[1]


def jupyter_notebook_tagger(container: Container) -> str:
    return "notebook-" + _get_program_version(container, "jupyter-notebook")


def jupyter_lab_tagger(container: Container) -> str:
    return "lab-" + _get_program_version(container, "jupyter-lab")


def jupyter_hub_tagger(container: Container) -> str:
    return "hub-" + _get_program_version(container, "jupyterhub")


def r_tagger(container: Container) -> str:
    return "r-" + _get_program_version(container, "R").split()[2]


def julia_tagger(container: Container) -> str:
    return "julia-" + _get_program_version(container, "julia").split()[2]


def tensorflow_tagger(container: Container) -> str:
    try:
        return "tensorflow-" + _get_pip_package_version(container, "tensorflow")
    except AssertionError:
        return "tensorflow-" + _get_pip_package_version(container, "tensorflow-cpu")


def pytorch_tagger(container: Container) -> str:
    return "pytorch-" + _get_pip_package_version(container, "torch").split("+")[0]


def spark_tagger(container: Container) -> str:
    SPARK_VERSION_LINE_PREFIX = r"   /___/ .__/\_,_/_/ /_/\_\   version"

    spark_version = _get_program_version(container, "spark-submit")
    version_line = next(
        filter(
            lambda line: line.startswith(SPARK_VERSION_LINE_PREFIX),
            spark_version.split("\n"),
        )
    )
    return "spark-" + version_line.split(" ")[-1]


def java_tagger(container: Container) -> str:
    return "java-" + _get_program_version(container, "java").split()[1]
