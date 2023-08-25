# Lint

To enforce some rules, **linters** are used in this project.
Linters can be run either during the **development phase** (by the developer) or the **integration phase** (by GitHub Actions).
To integrate and enforce this process in the project lifecycle, we are using **git hooks** through [pre-commit][pre-commit].

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
However, it is also possible to trigger it against all files.

```{note}
Hadolint pre-commit uses Docker to run, so `docker` should be running while running this command.
```

```sh
pre-commit run --all-files --hook-stage manual
```

```{note}
We're running `pre-commit` with `--hook-stage manual`, because works with changed files, which doesn't work well for mypy.
More information can be found in [`.pre-commit-config.yaml` file](https://github.com/jupyter/docker-stacks/blob/main/.pre-commit-config.yaml)
```

## Image Lint

To comply with [Docker best practices][dbp], we are using the [Hadolint][hadolint] tool to analyse each `Dockerfile`.

### Ignoring Rules

Sometimes it is necessary to ignore [some rules][rules].
The following rules are ignored by default for all images in the `.hadolint.yaml` file.

- [`DL3006`][dl3006]: We use a specific policy to manage image tags.
  - `base-notebook` `FROM` clause is fixed but based on an argument (`ARG`).
  - Building downstream images from (`FROM`) the latest is done on purpose.
- [`DL3008`][dl3008]: System packages are always updated (`apt-get`) to the latest version.
- [`DL3013`][dl3013]: We always install latest packages using `pip`

The preferred way to do it for other rules is to flag ignored ones in the `Dockerfile`.

> It is also possible to ignore rules by using a special comment directly above the Dockerfile instruction you want to make an exception for.
> Ignore rule comments look like `# hadolint ignore=DL3001,SC1081`.
> For example:

```dockerfile
FROM ubuntu

# hadolint ignore=DL3003,SC1035
RUN cd /tmp && echo "hello!"
```

[hadolint]: https://github.com/hadolint/hadolint
[dbp]: https://docs.docker.com/develop/develop-images/dockerfile_best-practices
[rules]: https://github.com/hadolint/hadolint#rules
[dl3006]: https://github.com/hadolint/hadolint/wiki/DL3006
[dl3008]: https://github.com/hadolint/hadolint/wiki/DL3008
[dl3013]: https://github.com/hadolint/hadolint/wiki/DL3013
[pre-commit]: https://pre-commit.com/
