# Jupyter Docker Stacks

Jupyter Docker Stacks are a set of ready-to-run Docker images containing Jupyter applications and interactive computing tools.

## Quick Start

The two examples below may help you get started if you [have Docker installed](https://docs.docker.com/install/) know [which Docker image](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html) you want to use, and want to launch a single Jupyter Notebook server in a container.

The [User Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) describes additional uses and features in detail.

**Example 1:** This command pulls the `jupyter/scipy-notebook` image tagged `2c80cf3537ca` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the terminal and include a URL to the notebook server. The container remains intact for restart after notebook server exit.::

    docker run -p 8888:8888 jupyter/scipy-notebook:2c80cf3537ca

**Example 2:** This command pulls the `jupyter/r-notebook` image tagged `e5c5a7d3e52d` from Docker Hub if it is not already present on the local host. It then starts an *ephemeral* container running a Jupyter Notebook server and exposes the server on host port 10000. The command mounts the current working directory on the host as `/home/jovyan/work` in the container. Docker destroys the container after notebook server exit, but any files written to `~/work` in the container remain intact on the host.::

    docker run --rm -p 10000:8888 -v "$PWD":/home/jovyan/work jupyter/r-notebook:e5c5a7d3e52d

## Contributing

Please see the [Contributor Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) for information about how to contribute package updates, recipes features, tests, and community maintained stacks.

## Resources

* [Documentation on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/)
* [Issue Tracker on GitHub](https://github.com/jupyter/docker-stacks)
* [Jupyter Google Group](https://groups.google.com/forum/#!forum/jupyter)
* [Jupyter Website](https://jupyter.org)