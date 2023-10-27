# Maintainer Playbook

## Merging Pull Requests

To build new images and publish them to the Registry, do the following:

1. Make sure GitHub Actions status checks pass for the PR.
2. Merge the PR.
3. Monitor the merge commit GitHub Actions status.

   ```{note}
   GitHub Actions are pretty reliable, so please investigate if some error occurs.
   Building Docker images in PRs is the same as building them in default branch,
   except single-platform images are pushed to Registry and then tags are merged for `x86_64` and `aarch64`.
   ```

4. Avoid merging another PR to the main branch until all pending builds in the main branch are complete.
   This way, you will know which commit might have broken the build
   and also have the correct tags for moving tags (like the `python` version).

## Updating Python version

When a new `Python` version is released, we wait for:

- all the dependencies to be available (as wheels or in `conda-forge`).
- the first `python` patch release for this version.
  This allows us to avoid many bugs, which can happen in a major release.

## Updating the Ubuntu Base Image

`jupyter/docker-stacks-foundation` is based on the LTS Ubuntu docker image.
We wait for the first point release of the new LTS Ubuntu before updating the version.
Other images are directly or indirectly inherited from `docker-stacks-foundation`.
We rebuild our images automatically each week, which means they frequently receive updates.

When there's a security fix in the Ubuntu base image, it's a good idea to manually trigger images rebuild
[from the GitHub actions workflow UI](https://github.com/jupyter/docker-stacks/actions/workflows/docker.yml).
Pushing the `Run Workflow` button will trigger this process.

## Adding a New Core Image to the Registry

```{note}
In general, we do not add new core images and ask contributors to either
create a [recipe](../using/recipes.md) or [community stack](../contributing/stacks.md).
We have a [policy](./new-images-and-packages-policy.md), which we consider when adding new images or new packages to existing images.
```

You can see an example of adding a new image [here](https://github.com/jupyter/docker-stacks/pull/1936/files).

When there's a new stack definition, check before merging the PR:

1. PR includes an update to the stack overview diagram
   [in the documentation](../using/selecting.md#image-relationships).
   The image links to the [blockdiag source](http://interactive.blockdiag.com/) used to create it.
2. PR updates the [Makefile](https://github.com/jupyter/docker-stacks/blob/main/Makefile),
   which is used to build the stacks in order on GitHub Actions.
3. Necessary Tagger(s)/Manifest(s) are added for the new image
   in the [tagging](https://github.com/jupyter/docker-stacks/tree/main/tagging) folder.
4. A new repository is created in the `jupyter` organization in the Registry,
   and it's named after the stack folder in the git repo.

## Adding a New Registry Owner Account

1. Visit <https://quay.io/organization/jupyter/teams/owners>
2. Add the maintainer's username.

## Restarting a failed build

If an automated build in GitHub Actions has got you down, you can restart failed steps on GitHub.
You can also download the artifacts and investigate them for any issues.
