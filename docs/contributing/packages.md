# Package Updates

We actively seek pull requests which update packages already included in the project Dockerfiles.
This is a great way for first-time contributors to participate in developing the Jupyter Docker
Stacks.

Please follow the process below to update a package version:

1. Locate the Dockerfile containing the library you wish to update (e.g.,
   [base-notebook/Dockerfile](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile),
   [scipy-notebook/Dockerfile](https://github.com/jupyter/docker-stacks/blob/master/scipy-notebook/Dockerfile))
2. Adjust the version number for the package. We prefer to pin the major and minor version number of
   packages so as to minimize rebuild side-effects when users submit pull requests (PRs). For
   example, you'll find the Jupyter Notebook package, `notebook`, installed using conda with
   `notebook=5.4.*`.
3. Please build the image locally before submitting a pull request. Building the image locally
   shortens the debugging cycle by taking some load off GitHub Actions, which graciously provide
   free build services for open source projects like this one. If you use `make`, call:
   ```bash
   make build/somestack-notebook
   ```
4. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)
   (PR) with your changes.
5. Watch for GitHub to report a build success or failure for your PR on GitHub.
6. Discuss changes with the maintainers and address any build issues. Version conflicts are the most
   common problem. You may need to upgrade additional packages to fix build failures.

## Notes

In order to help identifying packages that can be updated you can use the following helper tool. It
will list all the packages installed in the `Dockerfile` that can be updated -- dependencies are
filtered to focus only on requested packages.

```bash
$ make check-outdated/base-notebook

# INFO     test_outdated:test_outdated.py:80 3/8 (38%) packages could be updated
# INFO     test_outdated:test_outdated.py:82
# Package     Current    Newest
# ----------  ---------  --------
# conda       4.7.12     4.8.2
# jupyterlab  1.2.5      2.0.0
# python      3.7.4      3.8.2
```
