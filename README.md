[![Discourse badge](https://img.shields.io/discourse/https/discourse.jupyter.org/users.svg?color=%23f37626)](https://discourse.jupyter.org/c/questions "Jupyter Discourse Q&A")
[![Read the Docs badge](https://img.shields.io/readthedocs/jupyter-docker-stacks.svg)](https://jupyter-docker-stacks.readthedocs.io/en/latest/ "Documentation build status")
[![DockerHub badge](https://images.microbadger.com/badges/version/jupyter/base-notebook.svg)](https://microbadger.com/images/jupyter/base-notebook "Recent tag/version of jupyter/base-notebook")
[![Binder badget](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyter/docker-stacks/master?filepath=README.ipynb "Launch a jupyter/base-notebook container on mybinder.org")

# Jupyter Docker Stacks

Jupyter Docker Stacks are a set of ready-to-run [Docker images](https://hub.docker.com/u/jupyter)
containing Jupyter applications and interactive computing tools.

## Maintainer Help Wanted

We value all positive contributions to the Docker stacks project, from
[bug reports](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/issues.html) to
[pull requests](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/packages.html)
to
[translations](https://jupyter-docker-stacks.readthedocs.io/en/latest/contributing/translations.html)
to help answering questions. We'd also like to invite members of the community to help with two
maintainer activities:

- Issue triage: Reading and providing a first response to issues, labeling issues appropriately,
  redirecting cross-project questions to Jupyter Discourse
- Pull request reviews: Reading proposed documentation and code changes, working with the submitter
  to improve the contribution, deciding if the contribution should take another form (e.g., a recipe
  instead of a permanent change to the images)

Anyone in the community can jump in and help with these activities at any time. We will happily
grant additional permissions (e.g., ability to merge PRs) to anyone who shows an on-going interest
in working on the project.

## Jupyter Notebook Deprecation Notice

Following [Jupyter Notebook notice](https://github.com/jupyter/notebook#notice), we encourage users to transition to JupyterLab.
This can be done by passing the environment variable `JUPYTER_ENABLE_LAB=yes` at container startup, 
more information is available in the [documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#docker-options).

At some point, JupyterLab will become the default for all of the Jupyter Docker stack images, however a new environment variable will be introduced to switch back to Jupyter Notebook if needed.

After the change of default, and according to the Jupyter Notebook project status and its compatibility with JupyterLab, these Docker images may remove the classic Jupyter Notebook interface altogether in favor of another *classic-like* UI built atop JupyterLab.

This change is tracked in the issue [#1217](https://github.com/jupyter/docker-stacks/issues/1217), please check its content for more information.

## Quick Start

You can try a
[relatively recent build of the jupyter/base-notebook image on mybinder.org](https://mybinder.org/v2/gh/jupyter/docker-stacks/master?filepath=README.ipynb)
by simply clicking the preceding link. The image used in binder was last updated on 19 Jan 2021.
Otherwise, the two examples below may help you get started if
you [have Docker installed](https://docs.docker.com/install/) know
[which Docker image](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html) you
want to use, and want to launch a single Jupyter Notebook server in a container.

The [User Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) describes additional
uses and features in detail.

**Example 1:** This command pulls the `jupyter/scipy-notebook` image tagged `17aba6048f44` from
Docker Hub if it is not already present on the local host. It then starts a container running a
Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the
terminal. Visiting `http://<hostname>:8888/?token=<token>` in a browser loads the Jupyter Notebook
dashboard page, where `hostname` is the name of the computer running docker and `token` is the
secret token printed in the console. The container remains intact for restart after the notebook
server exits.

    docker run -p 8888:8888 jupyter/scipy-notebook:17aba6048f44

**Example 2:** This command performs the same operations as **Example 1**, but it exposes the server
on host port 10000 instead of port 8888. Visiting `http://<hostname>:10000/?token=<token>` in a
browser loads JupyterLab, where `hostname` is the name of the computer running docker and `token` is
the secret token printed in the console.::

    docker run -p 10000:8888 jupyter/scipy-notebook:17aba6048f44

**Example 3:** This command pulls the `jupyter/datascience-notebook` image tagged `9b06df75e445`
from Docker Hub if it is not already present on the local host. It then starts an _ephemeral_
container running a Jupyter Notebook server and exposes the server on host port 10000. The command
mounts the current working directory on the host as `/home/jovyan/work` in the container. The server
logs appear in the terminal. Visiting `http://<hostname>:10000/?token=<token>` in a browser loads
JupyterLab, where `hostname` is the name of the computer running docker and `token` is the secret
token printed in the console. Docker destroys the container after notebook server exit, but any
files written to `~/work` in the container remain intact on the host.

    docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work jupyter/datascience-notebook:9b06df75e445

## Contributing

Please see the [Contributor Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) for
information about how to contribute package updates, recipes, features, tests, and community
maintained stacks.

## Alternatives

- [jupyter/repo2docker](https://github.com/jupyter/repo2docker) - Turn git repositories into
  Jupyter-enabled Docker Images
- [openshift/source-to-image](https://github.com/openshift/source-to-image) - A tool for
  building/building artifacts from source and injecting into docker images
- [jupyter-on-openshift/jupyter-notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks) -
  OpenShift compatible S2I builder for basic notebook images

## Resources

- [Documentation on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/)
- [Issue Tracker on GitHub](https://github.com/jupyter/docker-stacks)
- [Jupyter Discourse Q&A](https://discourse.jupyter.org/c/questions)
- [Jupyter Website](https://jupyter.org)
- [Images on DockerHub](https://hub.docker.com/u/jupyter)
