# Development Setup

This page covers everything you need to run the full CI-equivalent checks locally before opening a pull request.

## Prerequisites

- [Docker](https://docs.docker.com/get-started/get-docker/)
- Python 3.12+
- GNU Make
- Git

## One-time setup

```bash
# Clone the repository (SSH, recommended)
git clone git@github.com:jupyter/docker-stacks.git
# or via HTTPS
git clone https://github.com/jupyter/docker-stacks.git

cd docker-stacks

# Install Python development dependencies
pip install --upgrade -r requirements-dev.txt

# Install pre-commit hooks (runs linters automatically on git commit)
pre-commit install --install-hooks
```

## Pre-PR checklist

Run these steps locally before pushing.

```bash
# 1. Run all linters including mypy
pre-commit run --all-files --hook-stage manual

# 2. Build the image you changed
make build/<image-name>

# 3. Run tests for that image
make test/<image-name>
```

```{note}
If the parent image isn't built locally, Docker pulls it from the registry.
This means changes to a parent image won't be reflected unless you also rebuild it locally.
```

Replace `<image-name>` with the image you modified (e.g., `docker-stacks-foundation`, `base-notebook`, `scipy-notebook`).

```{note}
`make test/<image-name>` runs the tests defined under `tests/by_image/<image-name>/`
against the named image only. CI additionally re-runs that same test set against every
downstream image, so a change in `docker-stacks-foundation` is verified across all images
in CI even though locally you'd only run `make test/docker-stacks-foundation`.
```

## Common examples

```bash
# Working on the foundation image (start scripts, logging, etc.)
pre-commit run --all-files --hook-stage manual
make build/docker-stacks-foundation
make test/docker-stacks-foundation

# Working on the base notebook image
pre-commit run --all-files --hook-stage manual
make build/docker-stacks-foundation
make build/base-notebook
make test/base-notebook

# Build and test every image (slow; mainly useful before opening a PR
# that changes the foundation or base image)
make build-all
make test-all
```
