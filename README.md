# docker-stacks

[![Join the chat at https://gitter.im/jupyter/jupyter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jupyter/jupyter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Opinionated stacks of ready-to-run Jupyter applications in Docker.

## Quick Start

If you're familiar with Docker, have it configured, and know exactly what you'd like to run, this one-liner should work in most cases:

```
docker run -d -P jupyter/<your desired stack>
```

## Getting Started

If this is your first time using Docker or any of the Jupyter projects, do the following to get started.

1. [Install Docker](https://docs.docker.com/installation/) on your host of choice.
2. Open the README in one of the folders in this git repository.
3. Follow the README for that stack.

## Stacks, Tags, Versioning, and Progress

Starting with [git commit SHA 9bd33dcc8688](https://github.com/jupyter/docker-stacks/tree/9bd33dcc8688):

* Every folder here on GitHub has an equivalent `jupyter/<stack name>` on Docker Hub. 
* The `latest` tag in each Docker Hub repository tracks the `master` branch `HEAD` reference on GitHub. 
* Any 12-character image tag on Docker Hub refers to a git commit SHA here on GitHub. 
* Stack contents (e.g., new library versions) will be updated upon request via PRs against this project.
* Users looking to remain on older builds should refer to specific git SHA tagged images in their work, not `latest`.
* Users who want to know the contents of a specific tagged image on Docker Hub can take its tag and use it as a git SHA to inspect the state of this repo at the time of that image build.
* For legacy reasons, there are two additional tags named `3.2` and `4.0` on Docker Hub which point to images prior to our versioning scheme switch.

## Maintainer Workflow

For PRs that impact the definition of one or more stacks:

1. Pull a PR branch locally.
2. Try building the affected stack(s).
3. If everything builds OK locally, merge it.
4. `ssh -i ~/.ssh/your-github-key build@docker-stacks.cloudet.xyz`
5. Run these commands on that VM.

```
cd docker-stacks
# make sure we're always on clean master from github
git fetch origin
git reset --hard origin/master
# if this fails, just run it again and again (idempotent)
make release-all
```

When there's a security fix in the Debian base image, do the following in place of the last command:

```
docker pull debian:jessie
make release-all DARGS=--no-cache
```

This will take time as the entire set of stacks will rebuild.
