# Jupyter Docker Stacks

[![GitHub actions badge](https://github.com/jupyter/docker-stacks/actions/workflows/docker.yml/badge.svg)](https://github.com/jupyter/docker-stacks/actions/workflows/docker.yml "Docker images build status")
[![Read the Docs badge](https://img.shields.io/readthedocs/jupyter-docker-stacks.svg)](https://jupyter-docker-stacks.readthedocs.io/en/latest/ "Documentation build status")
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jupyter/docker-stacks/main.svg)](https://results.pre-commit.ci/latest/github/jupyter/docker-stacks/main "pre-commit.ci build status")
[![Discourse badge](https://img.shields.io/discourse/users.svg?color=%23f37626&server=https%3A%2F%2Fdiscourse.jupyter.org)](https://discourse.jupyter.org/ "Jupyter Discourse Forum")
[![Binder badge](https://static.mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyter/docker-stacks/main?urlpath=lab/tree/README.ipynb "Launch a jupyter/base-notebook container on mybinder.org")

Jupyter Docker Stacks are a set of ready-to-run [Docker images](https://hub.docker.com/u/jupyter) containing Jupyter applications and interactive computing tools.
You can use a stack image to do any of the following (and more):

- Start a personal Jupyter Server with JupyterLab frontend (default)
- Run JupyterLab for a team using JupyterHub
- Start a personal Jupyter Notebook server in a local Docker container
- Write your own project Dockerfile

## Quick Start

You can try a [relatively recent build of the jupyter/base-notebook image on mybinder.org](https://mybinder.org/v2/gh/jupyter/docker-stacks/main?urlpath=lab/tree/README.ipynb)
by simply clicking the preceding link.
Otherwise, the examples below may help you get started if you [have Docker installed](https://docs.docker.com/get-docker/),
know [which Docker image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html) you want to use
and want to launch a single Jupyter Server in a container.

The [User Guide on ReadTheDocs](https://jupyter-docker-stacks.readthedocs.io/en/latest/) describes additional uses and features in detail.

**Example 1:**

This command pulls the `jupyter/scipy-notebook` image tagged `9e63909e0317` from Docker Hub if it is not already present on the local host.
It then starts a container running a Jupyter Server and exposes the container's internal port `8888` to port `10000` of the host machine:

```bash
docker run -p 10000:8888 jupyter/scipy-notebook:9e63909e0317
```

You can modify the port on which the container's port is exposed by [changing the value of the `-p` option](https://docs.docker.com/engine/reference/run/#expose-incoming-ports) to `-p 8888:8888`.

Visiting `http://<hostname>:10000/?token=<token>` in a browser loads JupyterLab,
where:

- `hostname` is the name of the computer running Docker
- `token` is the secret token printed in the console.

The container remains intact for restart after the Jupyter Server exits.

**Example 2:**

This command pulls the `jupyter/datascience-notebook` image tagged `9e63909e0317` from Docker Hub if it is not already present on the local host.
It then starts an _ephemeral_ container running a Jupyter Server and exposes the server on host port 10000.

```bash
docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook:9e63909e0317
```

The use of the `-v` flag in the command mounts the current working directory on the host (`${PWD}` in the example command) as `/home/jovyan/work` in the container.
The server logs appear in the terminal.

Visiting `http://<hostname>:10000/?token=<token>` in a browser loads JupyterLab.

Due to the usage of [the flag `--rm`](https://docs.docker.com/engine/reference/run/#clean-up---rm) Docker automatically cleans up the container and removes the file
system when the container exits, but any changes made to the `~/work` directory and its files in the container will remain intact on the host.
[The `-it` flag](https://docs.docker.com/engine/reference/commandline/run/#assign-name-and-allocate-pseudo-tty---name--it) allocates pseudo-TTY.

## Contributing

Please see the [Contributor Guide on ReadTheDocs](https://jupyter-docker-stacks.readthedocs.io/en/latest/) for
information about how to contribute package updates, recipes, features, tests, and community
maintained stacks.

## Maintainer Help Wanted

We value all positive contributions to the Docker stacks project,
from [bug reports](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/issues.html)
to [pull requests](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/packages.html)
to help with answering questions.
We'd also like to invite members of the community to help with two maintainer activities:

- **Issue triaging**: Reading and providing a first response to issues, labeling issues appropriately,
  redirecting cross-project questions to Jupyter Discourse
- **Pull request reviews**: Reading proposed documentation and code changes, working with the submitter
  to improve the contribution, deciding if the contribution should take another form (e.g., a recipe
  instead of a permanent change to the images)

Anyone in the community can jump in and help with these activities at any time.
We will happily grant additional permissions (e.g., ability to merge PRs) to anyone who shows an ongoing interest in working on the project.

## Jupyter Notebook Deprecation Notice

Following [Jupyter Notebook notice](https://github.com/jupyter/notebook#notice), JupyterLab is now the default for all the Jupyter Docker stack images.
It is still possible to switch back to Jupyter Notebook (or to launch a different startup command).
You can achieve this by passing the environment variable `DOCKER_STACKS_JUPYTER_CMD=notebook` (or any other valid `jupyter` subcommand) at container startup,
more information is available in the [documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#alternative-commands).

According to the Jupyter Notebook project status and its compatibility with JupyterLab,
these Docker images may remove the classic Jupyter Notebook interface altogether in favor of another _classic-like_ UI built atop JupyterLab.

This change is tracked in the issue [#1217](https://github.com/jupyter/docker-stacks/issues/1217); please check its content for more information.

## Alternatives

- [jupyter/repo2docker](https://github.com/jupyterhub/repo2docker) - Turn git repositories into
  Jupyter-enabled Docker Images
- [openshift/source-to-image](https://github.com/openshift/source-to-image) - A tool for
  building/building artifacts from source and injecting into docker images
- [jupyter-on-openshift/jupyter-notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks) -
  OpenShift compatible S2I builder for basic notebook images

## Resources

- [Documentation on ReadTheDocs](https://jupyter-docker-stacks.readthedocs.io/en/latest/)
- [Issue Tracker on GitHub](https://github.com/jupyter/docker-stacks)
- [Jupyter Discourse Forum](https://discourse.jupyter.org/)
- [Jupyter Website](https://jupyter.org)
- [Images on DockerHub](https://hub.docker.com/u/jupyter)

## CPU Architectures

- We publish containers for both `x86_64` and `aarch64` platforms, except for `tensorflow-notebook`, which only supports `x86_64` for now
- Single-platform images have either `aarch64` or `x86_64` tag prefixes, for example `jupyter/base-notebook:aarch64-python-3.10.5`
- Starting from `2022-09-21`, we create multi-platform images

## Using old images

This project only builds one set of images at a time.
On `2022-10-09`, we rebuilt images with old `Ubuntu` and `python` versions for users who still need them:

| Ubuntu | Python | Tag                                     |
| ------ | ------ | --------------------------------------- |
| 20.04  | 3.7    | `1aac87eb7fa5`                          |
| 20.04  | 3.8    | `a374cab4fcb6`                          |
| 20.04  | 3.9    | `5ae537728c69`                          |
| 20.04  | 3.10   | `f3079808ca8c`                          |
| 22.04  | 3.7    | `b86753318aa1`                          |
| 22.04  | 3.8    | `7285848c0a11`                          |
| 22.04  | 3.9    | `ed2908bbb62e`                          |
| 22.04  | 3.10   | `latest` (this image is rebuilt weekly) |
