# Image Tests

We greatly appreciate pull requests that extend the automated tests that vet the basic functionality
of the Docker images.

## How the Tests Work

GitHub Action executes `make build-test-all` against pull requests submitted to the `jupyter/docker-stacks` repository.
This `make` command builds every docker image.
After building each image, the `make` command executes `pytest` to run both image-specific tests like those in
[base-notebook/test/](https://github.com/jupyter/docker-stacks/tree/master/base-notebook/test) and
common tests defined in [test/](https://github.com/jupyter/docker-stacks/tree/master/test).
Both kinds of tests make use of global [pytest fixtures](https://docs.pytest.org/en/latest/reference/fixtures.html)
defined in the [conftest.py](https://github.com/jupyter/docker-stacks/blob/master/conftest.py) file at the root of the projects.

## Unit tests

If you want to run a python script in one of our images, you could add a unit test.
You can do this by creating a `<somestack>-notebook/test/units/` directory, if it doesn't already exist and put your file there.
These file will run automatically when tests are run.
You could see an example for tensorflow package [here](https://github.com/jupyter/docker-stacks/blob/HEAD/tensorflow-notebook/test/units/unit_tensorflow.py).

## Contributing New Tests

Please follow the process below to add new tests:

1. If the test should run against every image built, add your test code to one of the modules in
   [test/](https://github.com/jupyter/docker-stacks/tree/master/test) or create a new module.
2. If your test should run against a single image, add your test code to one of the modules in
   `some-notebook/test/` or create a new module.
3. Build one or more images you intend to test and run the tests locally.
   If you use `make`, call:

   ```bash
   make build/somestack-notebook
   make test/somestack-notebook
   ```

4. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)
   (PR) with your changes.
5. Watch for GitHub to report a build success or failure for your PR on GitHub.
6. Discuss changes with the maintainers and address any issues running the tests on GitHub.
