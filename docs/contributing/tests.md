# Image Tests

We greatly appreciate pull requests that extend the automated tests that vet the basic functionality of the Docker images.

## How the Tests Work

A [GitHub Action workflow](https://github.com/jupyter/docker-stacks/blob/master/.github/workflows/docker.yml)
runs the following commands against pull requests submitted to the `jupyter/docker-stacks` repository:

1. `make -C main build-all-multi` - which builds all the Docker images
2. `make -C main test-all` - which tests the newly created Docker images
   This `make` command builds and then tests every docker image.

We use `pytest` module to run tests on the image.
`conftest.py` and `pytest.ini` in the `tests` folder define the environment in which tests are run.
More info on `pytest` can be found [here](https://docs.pytest.org/en/latest/contents.html).

The actual image-specific test files are located in folders like `tests/<somestack>-notebook/`.

```{note}
If your test is located in `tests/<somestack>-notebook/`, it will be run against `jupyter/<somestack>-notebook` image and against all the [images inherited from this image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships.
```

Many tests make use of global [pytest fixtures](https://docs.pytest.org/en/latest/reference/fixtures.html)
defined in the [conftest.py](https://github.com/jupyter/docker-stacks/blob/master/tests/conftest.py) file.

## Unit tests

If you want to run a python script in one of our images, you could add a unit test.
You can do this by creating a `tests/<somestack>-notebook/units/` directory, if it doesn't already exist and put your file there.
Files in this folder will be executed in the container when tests are run.
You could see an [example for the TensorFlow package here](https://github.com/jupyter/docker-stacks/blob/HEAD/tests/tensorflow-notebook/units/unit_tensorflow.py).

## Contributing New Tests

Please follow the process below to add new tests:

1. Add your test code to one of the modules in `tests/<somestack>-notebook/` directory or create a new module.
2. Build one or more images you intend to test and run the tests locally.
   If you use `make`, call:

   ```bash
   make build/somestack-notebook
   make test/somestack-notebook
   ```

3. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)
   (PR) with your changes.
4. Watch for GitHub to report a build success or failure for your PR on GitHub.
5. Discuss changes with the maintainers and address any issues running the tests on GitHub.
