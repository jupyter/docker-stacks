# Package Updates

Generally, we do not pin package versions in our `Dockerfile`s.
Dependency resolution is a difficult thing to do.
All this means that packages might have old versions.
Images are rebuilt weekly, so usually, packages receive updates quite frequently.

```{note}
We pin major.minor version of python, so this will stay the same even after invoking the `mamba update` command.
```

## Outdated packages

To help to identify packages that can be updated, you can use the following helper tool.
It will list all the outdated packages installed in the `Dockerfile` --
dependencies are filtered to focus only on requested packages.

```bash
make check-outdated/base-notebook

# INFO     test_outdated:test_outdated.py:80 3/8 (38%) packages could be updated
# INFO     test_outdated:test_outdated.py:82
# Package     Current    Newest
# ----------  ---------  --------
# conda       4.7.12     4.8.2
# jupyterlab  1.2.5      2.0.0
# python      3.7.4      3.8.2
```
