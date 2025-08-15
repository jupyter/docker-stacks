# Changelog

This changelog only contains breaking and/or significant changes manually introduced to this repository (using Pull Requests).
All image manifests can be found in [the wiki](https://github.com/jupyter/docker-stacks/wiki).

## 2025-08-15

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: switch to Python 3.13 ([#2163](https://github.com/jupyter/docker-stacks/pull/2163)).

## 2025-04-13

Affected: `tensorflow-notebook`.

- **Non-breaking:** `tesnorflow-notebook`: Install latest tensorflow ([#2263](https://github.com/jupyter/docker-stacks/pull/2263)).

## 2025-04-12

Affected: all images.

- **Non-breaking:** `docker-stacks-foundation`: Pin libxml2 to avoid ABI breakage ([#2283](https://github.com/jupyter/docker-stacks/pull/2283)).

## 2025-04-11

Affected: all images.

- **Non-breaking:** Make docker tag-push depend on contributed recipes in CI ([#2282](https://github.com/jupyter/docker-stacks/pull/2282)).

## 2025-04-01

Affected: all images.

- **Non-breaking:** Apply and merge tags in the same place ([#2274](https://github.com/jupyter/docker-stacks/pull/2274)).

## 2025-03-23

Affected: `tensorflow-notebook`.

- **Non-breaking:** `tensorflow-notebook`: Use mamba to install jupyter-server-proxy ([#2262](https://github.com/jupyter/docker-stacks/pull/2262)).

## 2025-03-22

Affected: all images.

- **Non-breaking:** Use tty for running docker commands by default ([#2260](https://github.com/jupyter/docker-stacks/pull/2260)).
- **Non-breaking:** Improve logs around running docker ([#2261](https://github.com/jupyter/docker-stacks/pull/2261)).

## 2025-03-21

Affected: all images.

- **Non-breaking:** Refactor TrackedContainer run_detached/exec_cmd functions ([#2256](https://github.com/jupyter/docker-stacks/pull/2256)).
- **Non-breaking:** Do not allocate TTY in tests if not needed ([#2257](https://github.com/jupyter/docker-stacks/pull/2257)).
- **Non-breaking:** `base-notebook`: Flush output in Python before running execvp ([#2258](https://github.com/jupyter/docker-stacks/pull/2258)).

## 2025-03-20

Affected: all images except `docker-stacks-foundation`.

- **Non-breaking:** `base-notebook`: Refactor healthcheck tests to use one function ([#2254](https://github.com/jupyter/docker-stacks/pull/2254)).
- **Non-breaking:** `base-notebook`: Test server listening on IPv4/IPv6 ([#2255](https://github.com/jupyter/docker-stacks/pull/2255)).

## 2025-03-12

Affected: all images.

- **Non-breaking:** Add `conda` and `mamba` version taggers ([#2251](https://github.com/jupyter/docker-stacks/pull/2251)).
- **Non-breaking:** Make taggers and manifests functions ([#2252](https://github.com/jupyter/docker-stacks/pull/2252)).

## 2025-02-21

Affected: all images.

- **Non-breaking:** Better tagging directory structure ([#2228](https://github.com/jupyter/docker-stacks/pull/2228)).
- **Non-breaking:** Better testing directory structure ([#2231](https://github.com/jupyter/docker-stacks/pull/2231)).

## 2025-02-18

Affected: all images.

- **Non-breaking:** switch from `ubuntu-22.04-arm` to `ubuntu-24.04-arm` runners ([#2209](https://github.com/jupyter/docker-stacks/pull/2209)).
- **Non-breaking:** don't create extra free space in runners for cuda images ([#2218](https://github.com/jupyter/docker-stacks/pull/2218)).
- **Non-breaking:** revert "Pin some packages to fix `r-notebook` and `datascience-notebook` under aarch64" ([#2220](https://github.com/jupyter/docker-stacks/pull/2220)).
- **Non-breaking:** Simplify and improve `test_packages.py` ([#2219](https://github.com/jupyter/docker-stacks/pull/2219)).
- **Non-breaking:** Use Python 3.12 for internal code ([#2222](https://github.com/jupyter/docker-stacks/pull/2222)).

## 2025-02-17

Affected: all images.

- **Non-breaking:** build contributed recipes in PRs ([#2212](https://github.com/jupyter/docker-stacks/pull/2212), [#2213](https://github.com/jupyter/docker-stacks/pull/2213)).
- **Non-breaking:** remove information about Docker Hub images from Quay.io READMEs ([#2211](https://github.com/jupyter/docker-stacks/pull/2211)).
- **Non-breaking:** first upload artifacts and then run tests to make sure we can easily debug broken images ([#2214](https://github.com/jupyter/docker-stacks/pull/2214)).
- **Non-Breaking:** aarch64 `r-notebook`, `datascience-notebook`: pin some packages to fix `r-notebook` and `datascience-notebook` under aarch64 ([#2215](https://github.com/jupyter/docker-stacks/pull/2215)).
- **Non-breaking:** don't use matrix.image-variant, use 2 separate variables ([#2217](https://github.com/jupyter/docker-stacks/pull/2217)).

## 2025-02-11

Affected: all images.

- **Non-breaking:** start using `ubuntu-22.04-arm` GitHub-hosted `aarch64` runners ([#2202](https://github.com/jupyter/docker-stacks/pull/2202)).

## 2024-12-03

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: switch to `mamba` v2 ([#2147](https://github.com/jupyter/docker-stacks/pull/2147)).
  More information about changes made: <https://mamba.readthedocs.io/en/latest/developer_zone/changes-2.0.html>.

## 2024-11-08

Affected: all images except `docker-stacks-foundation`.

- **Breaking:** `base-notebook`: stop installing `nodejs` from `conda-forge` ([#2172](https://github.com/jupyter/docker-stacks/pull/2172)).

  Reason: It isn't a direct dependency on anything in the images anymore, and increased the image size by ~150MB.

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
