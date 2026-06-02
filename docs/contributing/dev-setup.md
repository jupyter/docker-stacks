# Development Setup

This page covers everything you need to run the full CI-equivalent checks locally before opening a pull request.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- Python 3.12+
- [GNU Make](https://www.gnu.org/software/make/)
- Git

## One-time setup

```bash
# Clone the repository (HTTPS)
git clone https://github.com/jupyter/docker-stacks.git
# or via SSH
git clone git@github.com:jupyter/docker-stacks.git

cd docker-stacks

# Install Python development dependencies
pip install --upgrade -r requirements-dev.txt

# Install pre-commit hooks (runs linters automatically on git commit)
pre-commit install --install-hooks
```

## Pre-PR checklist

Run these steps locally before pushing. They mirror what CI does.

```bash
# 1. Run all linters including mypy
pre-commit run --all-files --hook-stage manual

# 2. Build the image you changed
make build/<image-name>

# 3. Run tests for that image
make test/<image-name>
```

Replace `<image-name>` with the image you modified (e.g., `docker-stacks-foundation`, `base-notebook`, `scipy-notebook`).

```{note}
Tests run against all images that inherit from the one you specify.
If you modified `docker-stacks-foundation`, you only need to build and test that image,
but your changes will also be tested against downstream images in CI.
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
```
