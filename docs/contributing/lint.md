# Lint

To enforce some rules, **linters** are used in this project.
Linters can be run either during the **development phase** (by the developer) or the **integration phase** (by GitHub Actions).
To integrate and enforce this process in the project lifecycle, we are using **git hooks** through [pre-commit](https://pre-commit.com/).

## Using pre-commit hooks

### Pre-commit hook installation

_pre-commit_ is a Python package that needs to be installed.
To achieve this, use the generic task to install all Python development dependencies.

```sh
# Install all development dependencies for the project
pip install --upgrade -r requirements-dev.txt
# It can also be installed directly
pip install pre-commit
```

Then the git hooks scripts configured for the project in `.pre-commit-config.yaml` need to be installed in the local git repository.

```sh
pre-commit install
```

### Run

Now, _pre-commit_ (and so configured hooks) will run automatically on `git commit` on each changed file.
However, you can also run it against all files manually.

```{note}
Hadolint pre-commit uses Docker to run, so `docker` should be running while executing this command.
```

```sh
pre-commit run --all-files --hook-stage manual
```

```{note}
We're running `pre-commit` with `--hook-stage manual`, because `pre-commit` is run on modified files only, which doesn't work well with `mypy --follow-imports error`.
More information can be found in [`.pre-commit-config.yaml` file](https://github.com/jupyter/docker-stacks/blob/main/.pre-commit-config.yaml)
```

## Image Lint

To comply with [Docker best practices](https://docs.docker.com/build/building/best-practices/),
we are using the [Hadolint](https://github.com/hadolint/hadolint) tool to analyze each `Dockerfile`.

### Ignoring Rules

Sometimes it is necessary to ignore [some rules](https://github.com/hadolint/hadolint#rules).
The following rules are ignored by default for all images in the `.hadolint.yaml` file.

- [`DL3006`][dl3006]: We use a specific policy to manage image tags.
  - The `docker-stacks-foundation` `FROM` clause is fixed but based on an argument (`ARG`).
  - Building downstream images from (`FROM`) the latest is done on purpose.
- [`DL3008`][dl3008]: System packages are always updated (`apt-get`) to the latest version.
- [`DL3013`][dl3013]: We always install the latest packages using `pip`

The preferred way to ignore other rules is to flag them in the `Dockerfile`.
You can use a special comment directly above the Dockerfile instruction you want to make an exception for.
Ignore rule comments look like `# hadolint ignore=DL3001,SC1081`.
For example:

```dockerfile
FROM ubuntu

# hadolint ignore=DL3003,SC1035
RUN cd /tmp && echo "hello!"
```

[dl3006]: https://github.com/hadolint/hadolint/wiki/DL3006
[dl3008]: https://github.com/hadolint/hadolint/wiki/DL3008
[dl3013]: https://github.com/hadolint/hadolint/wiki/DL3013
