# New Recipes

We welcome contributions of [recipes](../using/recipes.md), short examples of using, configuring, or extending the Docker Stacks for inclusion in the documentation site.
Follow the process below to add a new recipe:

1. Open the `docs/using/recipes.md` source file.
2. Add a second-level Markdown heading naming your recipe at the bottom of the file (e.g., `## Slideshows with JupyterLab and RISE`)
3. Write the body of your recipe under the heading, including whatever command line, links, etc. you need.
4. If you have a Dockerfile, please put it in a `recipe_code` subdirectory.
   This file will be built automatically by [contributed-recipes workflow](https://github.com/jupyter/docker-stacks/blob/main/.github/workflows/contributed-recipes.yml).
5. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request) (PR) with your changes.
   Maintainers will respond and work with you to address any formatting or content issues.
