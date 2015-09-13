# docker-stacks

[![Join the chat at https://gitter.im/jupyter/jupyter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jupyter/jupyter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Opinionated stacks of ready-to-run Jupyter applications in Docker.

## Quick Start

If you're familiar with Docker, have it configured, and know exactly what you'd like to run, this one-liner should work in most cases:

```
docker run -d -P jupyter/<your desired stack>
```

## Getting Started

If this is your first time using Docker or any of the Jupyter projects, do the following to get started.

1. [Install Docker](https://docs.docker.com/installation/) on your host of choice.
2. Click the link for the Docker Hub repo or GitHub source for your desired stack.
3. Follow the README for that stack.

## Available Stacks

Branches / tags reflect the version of the primary process in each container (e.g., notebook server). Currently, GitHub master / Docker latest for Jupyter Notebook containers are equivalent to 4.0.x / 4.0

| Docker Hub repo | GitHub source | Git Branch &rarr; Docker Tag |
| --------------- | ------------- | ---------------------------- |
| [jupyter/minimal-notebook](https://hub.docker.com/r/jupyter/minimal-notebook/) | [minimal-notebook](./minimal-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 <br /> 3.2.x &rarr; 3.2 |
| [jupyter/scipy-notebook](https://hub.docker.com/r/jupyter/scipy-notebook/) | [scipy-notebook](./scipy-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 <br /> 3.2.x &rarr; 3.2 |
| [jupyter/r-notebook](https://hub.docker.com/r/jupyter/r-notebook/) | [r-notebook](./r-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 <br /> 3.2.x &rarr; 3.2 |
| [jupyter/datascience-notebook](https://hub.docker.com/r/jupyter/datascience-notebook/) | [datascience-notebook](./datascience-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 |
| [jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook/) | [all-spark-notebook](./all-spark-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 <br /> 3.2.x &rarr; 3.2 |
| [jupyter/pyspark-notebook](https://hub.docker.com/r/jupyter/pyspark-notebook/) | [pyspark-notebook](./pyspark-notebook) | master &rarr; latest <br /> 4.0.x &rarr; 4.0 <br /> 3.2.x &rarr; 3.2 |

## Maintainer Workflows

N.B. These are point in time instructions, subject to change as we find the best way to publish builds, manage branches, tag versions, etc.

### Triggering a Docker Hub build

At the moment, we have disabled the webhook to notify Docker Hub of commits in this GitHub repo and all links between parent and child docker repositories. (See issue #15.) Follow these steps to manually trigger builds.

After merging changes to `minimal-notebook` on any branch:

1. Visit https://hub.docker.com/r/jupyter/minimal-notebook/builds/.
2. Click *Trigger a Build*.
3. Monitor for transient build errors on Docker Hub.
4. Visit Docker Hub build page for each dependent stack.
5. Click *Trigger a Build* on each.
5. Monitor all dependent stack builds for errors on Docker Hub.

After merging changes to any other stack on any branch:

1. Visit the Docker Hub build page for the modified stack.
2. Click *Trigger a Build*.
3. Monitor for transient build errors on Docker Hub.

N.B. There's no way to rebuild a specific tag. If there are errors rebuilding a Docker Hub tag associated with a branch unaffected by the GitHub merge, it's OK. The last built image will retain the tag and should be functionally equivalent.

### Backporting fixes from master to a version branch (e.g., 4.0.x)

If the fix is a single commit, git cherry pick it. If it's multiple commits, use rebase. For example, if we have commits on master that we want to put in the `4.0.x` branch:

```
# make sure we're up to date locally
git co 4.0.x
git pull origin 4.0.x
git co master
git pull origin master

# create a backport branch off *master* and interactively
# rebase on the version branch
git co -b 4.0.x-backport
git rebase -i 4.0.x

# during the rebase ...
# delete any commits that ONLY belong in master
# retain any commits that you need to backport

# push backport branch to origin version branch
git push origin 4.0.x-backport:4.0.x

# cleanup
git branch -D 4.0.x-backport
```

### Upgrading to a new major/minor version of a Jupyter project

Our git branch and docker tagging scheme captures the major and minor version of the primary Jupyter project within the stack (e.g., Jupyter Notebook 4.0.x). When a new major or minor release of that project becomes available:

1. Update the relevant Dockerfiles, README, etc. to install the new version.
2. Push a new git branch in the form `<major>.<minor>.x` containing those changes.
3. Add a new branch-to-tag build under `Build Settings` in the affected `jupyter/*` Docker Hub repositories.
4. Promote the relevant git commits to master.
5. Manually trigger Docker Hub builds on all affected repositories.
