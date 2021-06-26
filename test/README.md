# Docker stacks testing

We test our images using `pytest` module.

`conftest.py` and `pytest.ini` in the root of our repository define the environment in which tests are run.
More info on pytest can be found [here](https://docs.pytest.org/en/latest/contents.html).

There are two kinds of tests we use:

- General tests - these are located in [this](https://github.com/jupyter/docker-stacks/blob/master/test) folder
- Image specific tests - for example, [base-notebook/test](https://github.com/jupyter/docker-stacks/blob/master/base-notebook/test) folder

We also have a way to easily run arbitrary python files in a container.
This is useful for running unit tests of packages we use, so we put these files in `{image}/test/units` folder.
An example of such a test is [unit_pandas.py](https://github.com/jupyter/docker-stacks/blob/master/scipy-notebook/test/units/unit_pandas.py).
