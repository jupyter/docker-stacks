# Image Lint

We are using the [Hadolint][LK1] tool to analyse each `Dockerfile` to comply with [Docker best practices][LK2].

## Install

There is a specific make target to install the linter.
By default `hadolint` will be installed in `${HOME}/hadolint`.

```bash
$ make lint-install

# Installing hadolint at /Users/romain/hadolint ...
# Installation done!
# Haskell Dockerfile Linter v1.17.6-0-gc918759
```

## Lint

The linter can be run per stack `make lint/<stack>`

```bash
$ make lint/scipy-notebook  

# Linting Dockerfiles in scipy-notebook...
# scipy-notebook/Dockerfile:4 DL3006 Always tag the version of an image explicitly
# scipy-notebook/Dockerfile:11 DL3008 Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
# scipy-notebook/Dockerfile:18 SC2086 Double quote to prevent globbing and word splitting.
# scipy-notebook/Dockerfile:68 SC2086 Double quote to prevent globbing and word splitting.
# scipy-notebook/Dockerfile:68 DL3003 Use WORKDIR to switch to a directory
# scipy-notebook/Dockerfile:79 SC2086 Double quote to prevent globbing and word splitting.
# make: *** [lint/scipy-notebook] Error 1
```

Optionally you can pass arguments to the linter.

```bash
# Use a different export format
$ make lint/scipy-notebook ARGS="--format codeclimate"  
```

To lint all the stacks.

```bash
$ make lint-all
```

## Ignore Rules

Sometimes it's necessary to ignore [some rules][LK3]. The preferred way is to do it in the `Dockerfile`.

> It is also possible to ignore rules by using a special comment directly above the Dockerfile instruction you want to make an exception for. Ignore rule comments look like `# hadolint ignore=DL3001,SC1081.` For example:

```dockerfile
# hadolint ignore=DL3006
FROM ubuntu

# hadolint ignore=DL3003,SC1035
RUN cd /tmp && echo "hello!"
```

[LK1]: https://github.com/hadolint/hadolint
[LK2]: https://docs.docker.com/develop/develop-images/dockerfile_best-practices
[LK3]: https://github.com/hadolint/hadolint#rules
