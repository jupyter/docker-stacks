# Package Updates

We welcome all contributions that update packages already included in the project Dockerfiles. Please follow the process below to update a package version:

1. Locate the Dockerfile containing the library you wish to update (e.g., [base-notebook/Dockerfile](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile), [scipy-notebook/Dockerfile](https://github.com/jupyter/docker-stacks/blob/master/scipy-notebook/Dockerfile))
2. Adjust the version number for the package.
    * We prefer to pin the major and minor version number of packages so as to minimize rebuild side-effects when users submit pull requests (PRs). For example, you'll find the Jupyter Notebook package, `notebook`, installed using conda with  `notebook=5.4.*`.
3. Try to build the image locally (`make image/somestack-notebook`) before submitting a pull request.
    * Building the image locally gives you a shorter debugging cycle than waiting for [Travis CI](http://travis-ci.org/) to build your changes.
    * Building locally also takes some load off of Travis CI which graciously provides free build services for open source projects like this one.
4. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)  (PR) with your changes.
5. Watch for Travis to report a build success or failure for your PR on GitHub.
6. Discuss changes with the maintainers and address any build issues.
    * Version conflicts are the most common problem. You may need to upgrade additional packages to fix build failures.
