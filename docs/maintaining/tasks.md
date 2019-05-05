# Maintainer Playbook

## Merging Pull Requests

To build new images on Docker Cloud and publish them to the Docker Hub registry, do the following:

1. Make sure Travis is green for a PR.
2. Merge the PR.
3. Monitor the Docker Cloud build status for each of the stacks, starting with [jupyter/base-notebook](https://cloud.docker.com/app/jupyter/repository/docker/jupyter/base-notebook/general) and ending with [jupyter/all-spark-notebook](https://cloud.docker.com/app/jupyter/repository/docker/jupyter/all-spark-notebook/general). See the [stack hierarchy diagram](../using/selecting.html#image-relationships) for the current, complete build order.
4. Manually click the retry button next to any build that fails to resume that build and any dependent builds.
5. Try to avoid merging another PR to master until all outstanding builds complete. There's no way at present to propagate the git SHA to build through the Docker Cloud build trigger API. Every build trigger works off of master HEAD.

## Updating the Ubuntu Base Image

When there's a security fix in the Ubuntu base image or after some time passes, it's a good idea to update the pinned SHA in the [jupyter/base-notebook Dockerfile](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile). Submit it as a regular PR and go through the build process. Expect the build to take a while to complete: every image layer will rebuild.

## Adding a New Core Image to Docker Cloud

When there's a new stack definition, do the following before merging the PR with the new stack:

1. Ensure the PR includes an update to the stack overview diagram [in the documentation](https://github.com/jupyter/docker-stacks/blob/master/docs/using/selecting.md#image-relationships). The image links to the [blockdiag source](http://interactive.blockdiag.com/) used to create it.
2. Ensure the PR updates the Makefile which is used to build the stacks in order on Travis CI.
3. Create a new repository in the `jupyter` org on Docker Cloud named after the stack folder in the git repo.
4. Grant the `stacks` team permission to write to the repo.
5. Click *Builds* and then *Configure Automated Builds* for the repository.
6. Select `jupyter/docker-stacks` as the source repository.
7. Choose *Build on Docker Cloud's infrastructure using a Small node* unless you have reason to believe a bigger host is required.
8. Update the *Build Context* in the default build rule to be `/<name-of-the-stack>`.
9. Toggle *Autobuild* to disabled unless the stack is a new root stack (e.g., like `jupyter/base-notebook`).
10. If the new stack depends on the build of another stack in the hierarchy:
    1. Hit *Save* and then click *Configure Automated Builds*.
    2. At the very bottom, add a build trigger named *Stack hierarchy trigger*.
    3. Copy the build trigger URL.
    4. Visit the parent repository *Builds* page and click *Configure Automated Builds*.
    5. Add the URL you copied to the *NEXT_BUILD_TRIGGERS* environment variable comma separated list of URLs, creating that environment variable if it does not already exist.
    6. Hit *Save*.
11. If the new stack should trigger other dependent builds:
    1. Add an environment variable named *NEXT_BUILD_TRIGGERS*.
    2. Copy the build trigger URLs from the dependent builds into the *NEXT_BUILD_TRIGGERS* comma separated list of URLs.
    3. Hit *Save*.
12. Adjust other *NEXT_BUILD_TRIGGERS* values as needed so that the build order matches that in the stack hierarchy diagram.

## Adding a New Maintainer Account

1. Visit https://cloud.docker.com/app/jupyter/team/stacks/users
2. Add the maintainer's Docker Cloud username.
3. Visit https://github.com/orgs/jupyter/teams/docker-image-maintainers/members
4. Add the maintainer's GitHub username.

## Pushing a Build Manually

If automated builds on Docker Cloud have got you down, do the following to push a build manually:

1. Clone this repository.
2. Check out the git SHA you want to build and publish.
3. `docker login` with your Docker Hub/Cloud credentials.
4. Run `make retry/release-all`.

## Enabling a New Doc Language Translation

First enable translation on Transifex:

1. Visit https://www.transifex.com/project-jupyter/jupyter-docker-stacks-1/languages/
2. Click *Edit Languages* in the top right.
3. Select the language from the dropdown.
4. Click *Apply*.

Then setup a subproject on ReadTheDocs for the language:

1. Visit https://readthedocs.org/dashboard/import/manual/
2. Enter *jupyter-docker-stacks-<lang>* for the project name.
3. Enter https://github.com/jupyter/docker-stacks for the URL.
4. Check *Edit advanced project options*.
5. Click *Next*.
6. Select the *Language* from the dropdown on the next screen.
7. Click *Finish*.

Finally link the new language subproject to the top level doc project:

1. Visit https://readthedocs.org/dashboard/jupyter-docker-stacks/translations/
2. Select the subproject you created from the *Project* dropdown.
3. Click *Add*.
