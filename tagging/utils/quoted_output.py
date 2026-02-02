# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import textwrap

from docker.models.containers import Container

from tagging.utils.docker_runner import DockerRunner


def quoted_output(container: Container, cmd: str) -> str:
    cmd_output = DockerRunner.exec_cmd(container, cmd)
    # For example, `mamba info` adds redundant empty lines
    cmd_output = cmd_output.strip("\n")
    # For example, R packages list contains trailing backspaces
    cmd_output = "\n".join(line.rstrip() for line in cmd_output.split("\n"))

    assert cmd_output, f"Command `{cmd}` returned empty output"

    return textwrap.dedent(f"""\
        `{cmd}`:

        ```text
        {{output}}
        ```""").format(output=cmd_output)
