# Changelog

This changelog only contains breaking and/or significant changes manually introduced to this repository (using Pull Requests).
All image manifests can be found in [the wiki](https://github.com/jupyter/docker-stacks/wiki).

## 2024-11-08

Affected: all images except `docker-stacks-foundation`.

- **Breaking:** `base-notebook`: stop installing `nodejs` from `conda-forge` ([#2172](https://github.com/jupyter/docker-stacks/pull/2172)).

  Reason: It isn't a direct dependency on anything in the images any more, and increased the image size with ~150MB.

## 2024-11-06

Affected: all images except `docker-stacks-foundation`.

- **Non-breaking:** `base-notebook`: install `jupyterhub-base` and `nodejs` packages instead of `jupyterhub` package ([#2171](https://github.com/jupyter/docker-stacks/pull/2171)).

## 2024-10-23

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: switch to Python 3.12 ([#2072](https://github.com/jupyter/docker-stacks/pull/2072)).

## 2024-10-22

Affected: `pyspark-notebook` and `all-spark-notebook` images.

- **Breaking:** `pyspark-notebook`: start using Spark 4.0.0 preview versions ([#2159](https://github.com/jupyter/docker-stacks/pull/2159)).
  `sparklyr` doesn't seem to support Spark v4 yet when using Spark locally.

  Reason: Spark v3 is not compatible with Python 3.12, and [the voting group has decided](https://github.com/jupyter/docker-stacks/pull/2072#issuecomment-2414123851) to switch to Spark v4 preview version.

## 2024-10-09

Affected: users building a custom set of images.

- **Breaking:** rename: `ROOT_CONTAINER`->`ROOT_IMAGE`, `BASE_CONTAINER`->`BASE_IMAGE` ([#2154](https://github.com/jupyter/docker-stacks/issues/2154), [#2155](https://github.com/jupyter/docker-stacks/pull/2155)).
