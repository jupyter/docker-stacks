# Changelog

This changelog only contains breaking and/or significant changes manually introduced to this repository (using Pull Requests).
All image manifests can be found in [the wiki](https://github.com/jupyter/docker-stacks/wiki).

## 2026-08-08

Affected: users building images locally.

- **Non-breaking:** Support Apple Container in Makefile ([#2548](https://github.com/jupyter/docker-stacks/pull/2548)).

## 2026-08-07

Affected: all images.

- **Non-breaking:** Set only the setgid bit on directories in `fix-permissions` ([#2539](https://github.com/jupyter/docker-stacks/pull/2539)).
- **Non-breaking:** Sign pushed images with cosign ([#2534](https://github.com/jupyter/docker-stacks/pull/2534)).

## 2026-07-28

Affected: all images.

- **Non-breaking:** Images review fixes: rework Rosetta junk cleanup, automatically resolve `pandas` version from Spark, and more ([#2531](https://github.com/jupyter/docker-stacks/pull/2531)).

## 2026-07-27

Affected: all images.

- **Non-breaking:** Fix multiple small issues: idempotent container restarts, healthcheck for non-HTTP(S) server URLs, checksum verification of downloads, and more ([#2522](https://github.com/jupyter/docker-stacks/pull/2522)).

## 2026-06-02

Affected: all images.

- **Non-breaking:** Add color to log output based on level ([#2459](https://github.com/jupyter/docker-stacks/pull/2459)).

## 2026-06-01

Affected: all images.

- **Non-breaking:** Improve logging in `start.sh` and `run-hooks.sh` ([#2452](https://github.com/jupyter/docker-stacks/pull/2452)).

## 2026-05-31

Affected: all images.

- **Non-breaking:** Pin container images to digest hashes ([#2450](https://github.com/jupyter/docker-stacks/pull/2450)).

## 2026-04-02

Affected: `pyspark-notebook`, `all-spark-notebook`.

- **Breaking:** `pyspark-notebook`: Update to Java 21 and Derby 10.17.1.0 ([#2424](https://github.com/jupyter/docker-stacks/pull/2424)).

## 2025-12-31

Affected: `pytorch-notebook`.

- **Non-breaking:** `pytorch-notebook`: Build pytorch cuda13 image instead of cuda11 ([#2391](https://github.com/jupyter/docker-stacks/pull/2391)).

## 2025-12-02

Affected: `tensorflow-notebook`, `pytorch-notebook`.

- **Non-breaking:** Enable CUDA build for ARM64 ([#2352](https://github.com/jupyter/docker-stacks/pull/2352)).

## 2025-11-29

Affected: all images.

- **Breaking:** Use Docker v29 and `docker buildx imagetools create` ([#2368](https://github.com/jupyter/docker-stacks/pull/2368)).

## 2025-11-24

Affected: all images.

- **Non-breaking:** Add Dev Container support ([#2358](https://github.com/jupyter/docker-stacks/pull/2358)).
- **Non-breaking:** Add recipe on running Jupyter Docker Stacks with Singularity ([#2357](https://github.com/jupyter/docker-stacks/pull/2357)).

## 2025-11-06

Affected: `scipy-notebook`.

- **Breaking:** `scipy-notebook`: Remove facets package installation ([#2347](https://github.com/jupyter/docker-stacks/pull/2347)).

## 2025-09-16

Affected: all images.

- **Non-breaking:** Publish SBOM using anchore/sbom-action ([#2317](https://github.com/jupyter/docker-stacks/pull/2317)).

## 2025-08-15

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: Switch to Python 3.13 ([#2163](https://github.com/jupyter/docker-stacks/pull/2163)).

## 2025-04-13

Affected: `tensorflow-notebook`.

- **Non-breaking:** `tensorflow-notebook`: Install latest tensorflow ([#2263](https://github.com/jupyter/docker-stacks/pull/2263)).

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

- **Non-breaking:** Switch from `ubuntu-22.04-arm` to `ubuntu-24.04-arm` runners ([#2209](https://github.com/jupyter/docker-stacks/pull/2209)).
- **Non-breaking:** Don't create extra free space in runners for cuda images ([#2218](https://github.com/jupyter/docker-stacks/pull/2218)).
- **Non-breaking:** Revert "Pin some packages to fix `r-notebook` and `datascience-notebook` under aarch64" ([#2220](https://github.com/jupyter/docker-stacks/pull/2220)).
- **Non-breaking:** Simplify and improve `test_packages.py` ([#2219](https://github.com/jupyter/docker-stacks/pull/2219)).
- **Non-breaking:** Use Python 3.12 for internal code ([#2222](https://github.com/jupyter/docker-stacks/pull/2222)).

## 2025-02-17

Affected: all images.

- **Non-breaking:** Build contributed recipes in PRs ([#2212](https://github.com/jupyter/docker-stacks/pull/2212), [#2213](https://github.com/jupyter/docker-stacks/pull/2213)).
- **Non-breaking:** Remove information about Docker Hub images from Quay.io READMEs ([#2211](https://github.com/jupyter/docker-stacks/pull/2211)).
- **Non-breaking:** First upload artifacts and then run tests to make sure we can easily debug broken images ([#2214](https://github.com/jupyter/docker-stacks/pull/2214)).
- **Non-breaking:** aarch64 `r-notebook`, `datascience-notebook`: Pin some packages to fix `r-notebook` and `datascience-notebook` under aarch64 ([#2215](https://github.com/jupyter/docker-stacks/pull/2215)).
- **Non-breaking:** Don't use matrix.image-variant, use 2 separate variables ([#2217](https://github.com/jupyter/docker-stacks/pull/2217)).

## 2025-02-11

Affected: all images.

- **Non-breaking:** Start using `ubuntu-22.04-arm` GitHub-hosted `aarch64` runners ([#2202](https://github.com/jupyter/docker-stacks/pull/2202)).

## 2024-12-03

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: Switch to `mamba` v2 ([#2147](https://github.com/jupyter/docker-stacks/pull/2147)).
  More information about changes made: <https://mamba.readthedocs.io/en/latest/developer_zone/changes-2.0.html>.

## 2024-11-08

Affected: all images except `docker-stacks-foundation`.

- **Breaking:** `base-notebook`: Stop installing `nodejs` from `conda-forge` ([#2172](https://github.com/jupyter/docker-stacks/pull/2172)).

  Reason: It isn't a direct dependency on anything in the images anymore, and increased the image size by ~150MB.

## 2024-11-06

Affected: all images except `docker-stacks-foundation`.

- **Non-breaking:** `base-notebook`: Install `jupyterhub-base` and `nodejs` packages instead of `jupyterhub` package ([#2171](https://github.com/jupyter/docker-stacks/pull/2171)).

## 2024-10-23

Affected: all images.

- **Breaking:** `docker-stacks-foundation`: Switch to Python 3.12 ([#2072](https://github.com/jupyter/docker-stacks/pull/2072)).

## 2024-10-22

Affected: `pyspark-notebook`, `all-spark-notebook`.

- **Breaking:** `pyspark-notebook`: Start using Spark 4.0.0 preview versions ([#2159](https://github.com/jupyter/docker-stacks/pull/2159)).
  `sparklyr` doesn't seem to support Spark v4 yet when using Spark locally.

  Reason: Spark v3 is not compatible with Python 3.12, and [the voting group has decided](https://github.com/jupyter/docker-stacks/pull/2072#issuecomment-2414123851) to switch to Spark v4 preview version.

## 2024-10-09

Affected: users building a custom set of images.

- **Breaking:** Rename: `ROOT_CONTAINER`->`ROOT_IMAGE`, `BASE_CONTAINER`->`BASE_IMAGE` ([#2154](https://github.com/jupyter/docker-stacks/issues/2154), [#2155](https://github.com/jupyter/docker-stacks/pull/2155)).
