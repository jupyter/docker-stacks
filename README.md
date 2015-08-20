# docker-stacks

[![Join the chat at https://gitter.im/jupyter/docker-stacks](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jupyter/docker-stacks?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Opinionated stacks of ready-to-run Jupyter applications in Docker.

## Quick Start

If you already have Docker configured and know exactly what you'd like to run, this one-liner should work in most cases:

```
docker run -d -P jupyter/<your desired stack>
```

## Getting Started

If this is your first time using Docker or any of the Jupyter projects, do the following to get started.

1. [Install Docker](https://docs.docker.com/installation/) on your host of choice.
2. Click the folder for your desired stack on GitHub.
3. Follow the README in that stack.

## Available Stacks

| Docker Hub repo | GitHub source |
| --------------- | ------------- |
| [jupyter/minimal-notebook](https://hub.docker.com/r/jupyter/minimal-notebook/) | [minimal-notebook](./minimal-notebook) |
| [jupyter/scipy-notebook](https://hub.docker.com/r/jupyter/scipy-notebook/) | [scipy-notebook](./scipy-notebook) |
| [jupyter/r-notebook](https://hub.docker.com/r/jupyter/r-notebook/) | [r-notebook](./r-notebook) |
| [jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook/) | [all-spark-notebook](./all-spark-notebook)
| [jupyter/pyspark-notebook](https://hub.docker.com/r/jupyter/pyspark-notebook/) | [pyspark-notebook](./pyspark-notebook) |
