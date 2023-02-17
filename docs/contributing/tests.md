# Image Tests

We greatly appreciate pull requests that extend the automated tests that vet the basic functionality of the Docker images.

## How the Tests Work

A [GitHub Action workflow](https://github.com/jupyter/docker-stacks/blob/main/.github/workflows/docker.yml)
runs tests against pull requests submitted to the `jupyter/docker-stacks` repository.

We use the `pytest` module to run tests on the image.
`conftest.py` and `pytest.ini` in the `tests` folder define the environment in which tests are run.
More info on `pytest` can be found [here](https://docs.pytest.org/en/latest/contents.html).

The actual image-specific test files are located in folders like `tests/<somestack>/` (e.g., `tests/docker-stacks-foundation/`, `tests/minimal-notebook/`, etc.).

```{note}
If your test is located in `tests/<somestack>/`, it will be run against `jupyter/<somestack>` image and against all the [images inherited from this image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships.
```

Many tests make use of global [pytest fixtures](https://docs.pytest.org/en/latest/reference/fixtures.html)
defined in the [conftest.py](https://github.com/jupyter/docker-stacks/blob/main/tests/conftest.py) file.

## Unit tests

You can add a unit test if you want to run a python script in one of our images.
You should create a `tests/<somestack>/units/` directory, if it doesn't already exist and put your file there.
Files in this folder will be executed in the container when tests are run.
You can see an [example for the TensorFlow package here](https://github.com/jupyter/docker-stacks/blob/HEAD/tests/tensorflow-notebook/units/unit_tensorflow.py).

## Contributing New Tests

Please follow the process below to add new tests:

1. Add your test code to one of the modules in `tests/<somestack>/` directory or create a new module.
2. Build one or more images you intend to test and run the tests locally.
   If you use `make`, call:

   ```bash
   make build/<somestack>
   make test/<somestack>
   ```

3. [Submit a pull request](https://github.com/PointCloudLibrary/pcl/wiki/A-step-by-step-guide-on-preparing-and-submitting-a-pull-request)
   (PR) with your changes.
4. Watch for GitHub to report a build success or failure for your PR on GitHub.
5. Discuss changes with the maintainers and address any issues running the tests on GitHub.
