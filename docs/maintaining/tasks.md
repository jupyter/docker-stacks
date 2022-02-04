# Maintainer Playbook

## Merging Pull Requests

To build new images and publish them to the Docker Hub registry, do the following:

1. Make sure GitHub Actions status checks pass for the PR.
2. Merge the PR.
3. Monitor the merge commit GitHub Actions status.
   **Note**: we think, GitHub Actions are quite reliable, so please, investigate, if some error occurs.
   The process of building docker images in PRs is exactly the same after merging to master, except there is an additional `push` step.
4. Try to avoid merging another PR to master until all pending builds complete.
   This way you will know which commit might have broken the build and also have correct tags for moving tags (like `python` version).

## Updating the Ubuntu Base Image

`minimal-notebook` is based on the Latest LTS Ubuntu docker image.
Other images are directly or indirectly inherited from `minimal-notebook`.
We rebuild our images automatically each week, which means they receive the updates quite frequently.

When there's a security fix in the Ubuntu base image, it's a good idea to manually trigger images rebuild [from the GitHub actions workflow UI](https://github.com/jupyter/docker-stacks/actions/workflows/docker.yml).
Pushing `Run Workflow` button will trigger this process.

## Adding a New Core Image to Docker Hub

```{note}
In general, we do not add new core images and ask contributors to either create a [recipe](../using/recipes.md) or [community stack](../contributing/stacks.md).
```

When there's a new stack definition, do the following before merging the PR with the new stack:

1. Ensure the PR includes an update to the stack overview diagram
   [in the documentation](https://github.com/jupyter/docker-stacks/blob/master/docs/using/selecting.md#image-relationships).
   The image links to the [blockdiag source](http://interactive.blockdiag.com/) used to create it.
2. Ensure the PR updates the [Makefile](https://github.com/jupyter/docker-stacks/blob/master/Makefile) which is used to build the stacks in order on GitHub Actions.
3. Ensure necessary tags / manifests are added for the new image in the [tagging](https://github.com/jupyter/docker-stacks/blob/master/tagging) folder.
4. Create a new repository in the `jupyter` org on Docker Hub named after the stack folder in the
   git repo.
5. Grant the `stacks` team permission to write to the repo.

## Adding a New Maintainer Account

1. Visit <https://hub.docker.com/app/jupyter/team/stacks/users>
2. Add the maintainer's Docker Hub username.
3. Visit <https://github.com/orgs/jupyter/teams/docker-image-maintainers/members>
4. Add the maintainer's GitHub username.

## Pushing a Build Manually

If automated build in Github Actions has got you down, do the following to push a build manually:

1. Clone this repository.
2. Check out the git SHA you want to build and publish.
3. `docker login` with your Docker Hub credentials.
4. Run `make push-all`.
