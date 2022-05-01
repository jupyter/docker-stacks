# Lint

In order to enforce some rules **linters** are used in this project.
Linters can be run either during the **development phase** (by the developer) and during **integration phase** (by GitHub Actions).
To integrate and enforce this process in the project lifecycle we are using **git hooks** through [pre-commit][pre-commit].

## Using pre-commit hooks

### Pre-commit hook installation

pre-commit is a Python package that needs to be installed.
This can be achieved by using the generic task used to install all Python development dependencies.

```sh
# Install all development dependencies for the project
pip install requirements-dev.txt
# It can also be installed directly
pip install pre-commit
```

Then the git hooks scripts configured for the project in `.pre-commit-config.yaml` need to be installed in the local git repository.

```sh
make pre-commit-install
```

### Run

Now pre-commit (and so configured hooks) will run automatically on `git commit` on each changed file.
However, it is also possible to trigger it against all files.

```{note}
Hadolint pre-commit uses docker to run, so docker should be running while running this command.
```

```sh
make pre-commit-all
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

For other rules, the preferred way to do it is to flag ignored rules in the `Dockerfile`.

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
[pre-commit]: https://pre-commit.com/
