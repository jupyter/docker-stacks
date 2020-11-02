# Lint

In order to enforce some rules **linters** are used in this project.
Linters can be run either during the **development phase** (by the developer) and during **integration phase** (by Travis).
To integrate and enforce this process in the project lifecycle we are using **git hooks** through [pre-commit][pre-commit].

## Pre-commit hook

### Installation

pre-commit is a Python package that needs to be installed.
This can be achieved by using the generic task used to install all Python development dependencies.

```sh
# Install all development dependencies for the project
$ make dev-env
# It can also be installed directly
$ pip install pre-commit
```

Then the git hooks scripts configured for the project in `.pre-commit-config.yaml` need to be installed in the local git repository.

```sh
$ make pre-commit-install
```

### Run

Now pre-commit (and so configured hooks) will run automatically on `git commit` on each changed file.
However it is also possible to trigger it against all files.

```sh
$ make pre-commit-all
```

## Image Lint

To comply with [Docker best practices][dbp], we are using the [Hadolint][hadolint] tool to analyse each `Dockerfile` .

### Installation

There is a specific `make` target to install the linter.
By default `hadolint` will be installed in `${HOME}/hadolint`.

```bash
$ make hadolint-install

# Installing hadolint at /Users/romain/hadolint ...
# Installation done!
# Haskell Dockerfile Linter v1.17.6-0-gc918759
```

### Linting

#### Per Stack

The linter can be run per stack.

```bash
$ make hadolint/scipy-notebook

# Linting Dockerfiles in scipy-notebook...
# scipy-notebook/Dockerfile:4 DL3006 Always tag the version of an image explicitly
# scipy-notebook/Dockerfile:11 DL3008 Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
# scipy-notebook/Dockerfile:18 SC2086 Double quote to prevent globbing and word splitting.
# scipy-notebook/Dockerfile:68 SC2086 Double quote to prevent globbing and word splitting.
# scipy-notebook/Dockerfile:68 DL3003 Use WORKDIR to switch to a directory
# scipy-notebook/Dockerfile:79 SC2086 Double quote to prevent globbing and word splitting.
# make: *** [lint/scipy-notebook] Error 1
```

Optionally you can pass arguments to the hadolint.

```bash
# Use a different export format
$ make hadolint/scipy-notebook ARGS="--format codeclimate"
```

#### All the Stacks

The linter can be run against all the stacks.

```bash
$ make hadolint-all
```

### Ignoring Rules

Sometimes it is necessary to ignore [some rules][rules].
The following rules are ignored by default and sor for all images in the `.hadolint.yaml` file.

- [`DL3006`][DL3006]: We use a specific policy to manage image tags.
  - `base-notebook` `FROM` clause is fixed but based on an argument (`ARG`).
  - Building downstream images from (`FROM`) the latest is done on purpose.
- [`DL3008`][DL3008]: System packages are always updated (`apt-get`) to the latest version.

For other rules, the preferred way to do it is to flag ignored rules in the `Dockerfile`.

> It is also possible to ignore rules by using a special comment directly above the Dockerfile instruction you want to make an exception for. Ignore rule comments look like `# hadolint ignore=DL3001,SC1081`. For example:

```dockerfile

FROM ubuntu

# hadolint ignore=DL3003,SC1035
RUN cd /tmp && echo "hello!"
```

[hadolint]: https://github.com/hadolint/hadolint
[dbp]: https://docs.docker.com/develop/develop-images/dockerfile_best-practices
[rules]: https://github.com/hadolint/hadolint#rules
[DL3006]: https://github.com/hadolint/hadolint/wiki/DL3006
[DL3008]: https://github.com/hadolint/hadolint/wiki/DL3008
[pre-commit]: https://pre-commit.com/