# New Features

Thank you for contributing to the Jupyter Docker Stacks!
We review pull requests for new features (e.g., new packages, new scripts, new flags)
to balance the value of the images to the Jupyter community with the cost of maintaining the images over time.

## Suggesting a New Feature

Please follow the process below to suggest a new feature for inclusion in one of the core stacks:

1. Open a [GitHub feature request issue](https://github.com/jupyter/docker-stacks/issues/new?assignees=&labels=type%3AEnhancement&projects=&template=feature_request.yml)
   describing the feature you'd like to contribute.
2. Discuss with the maintainers whether the addition makes sense
   in [one of the core stacks](../using/selecting.md#core-stacks),
   as a [recipe in the documentation](recipes.md),
   as a [community stack](stacks.md),
   or as something else entirely.

## Selection Criteria

Roughly speaking, we evaluate new features based on the following criteria:

- **Usefulness to Jupyter users**:
  Is the feature generally applicable across domains?
  Does it work with JupyterLab, Jupyter Notebook, JupyterHub, etc.?
- **Fit with the image purpose**:
  Does the feature match the theme of the stack in which it will be added?
  Would it fit better in a new community stack?
- **Complexity of build/runtime configuration**:
  How many lines of code does the feature require in one of the Dockerfiles or startup scripts?
  Does it require new scripts entirely?
  Do users need to adjust how they use the images?
- **Impact on image metrics**:
  How many bytes does the feature and its dependencies add to the image(s)?
  How many minutes do they add to the build time?
- **Ability to support the addition**:
  Can existing maintainers answer user questions and address future build issues?
  Are the contributors interested in helping with long-term maintenance?
  Can we write tests to ensure the feature continues to work over time?

## Submitting a Pull Request

If there's agreement that the feature belongs in one or more of the core stacks:

1. Implement the feature in a local clone of the `jupyter/docker-stacks` project.
2. Please, build the image locally before submitting a pull request.
   It shortens the debugging cycle by taking some load off GitHub Actions,
   which graciously provides free build services for open-source projects like this one.
   If you use `make`, call:

   ```bash
   make build/<somestack>
   ```

3. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)(PR) with your changes.
4. Watch for GitHub to report a build success or failure for your PR on GitHub.
5. Discuss changes with the maintainers and address any build issues.
