<!---
[![Discourse badge](https://img.shields.io/discourse/https/discourse.jupyter.org/users.svg?color=%23f37626)](https://discourse.jupyter.org/c/questions "Jupyter Discourse Q&A")
[![Read the Docs badge](https://img.shields.io/readthedocs/jupyter-docker-stacks.svg)](https://jupyter-docker-stacks.readthedocs.io/en/latest/ "Documentation build status")
[![DockerHub badge](https://images.microbadger.com/badges/version/jupyter/base-notebook.svg)](https://microbadger.com/images/jupyter/base-notebook "Recent tag/version of jupyter/base-notebook")
[![Binder badget](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyter/docker-stacks/master?filepath=README.ipynb "Launch a jupyter/base-notebook container on mybinder.org")
--->

# Jupyter Multi-Architecture Docker Stacks

The official Jupyter [Docker images](https://hub.docker.com/u/jupyter)
do not support ARM processors.

This fork is an attempt to port a subset of the official stacks to a multi-architecture docker configuration. The main obstacle is the lack of good support for Conda on ARM.

If you do not want to run notebook servers on ARM computers, use the [Official Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/).

## Alternatives

- [Official Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/)
- [jupyter/repo2docker](https://github.com/jupyter/repo2docker) - Turn git repositories into
  Jupyter-enabled Docker Images
- [openshift/source-to-image](https://github.com/openshift/source-to-image) - A tool for
  building/building artifacts from source and injecting into docker images
- [jupyter-on-openshift/jupyter-notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks) -
  OpenShift compatible S2I builder for basic notebook images

## Resources

- [Issue Tracker on GitHub](https://github.com/iot49/docker-stacks)
- [Jupyter Discourse Q&A](https://discourse.jupyter.org/c/questions)
- [Jupyter Website](https://jupyter.org)
- [Images on DockerHub](https://hub.docker.com/u/ttmetro)
