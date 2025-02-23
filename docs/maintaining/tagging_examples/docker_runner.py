# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.utils.docker_runner import DockerRunner

with DockerRunner("ubuntu") as container:
    DockerRunner.run_simple_command(container, cmd="env", print_result=True)
