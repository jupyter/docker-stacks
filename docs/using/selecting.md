# Selecting an Image

- [Core Stacks](#core-stacks)
- [Image Relationships](#image-relationships)
- [Community Stacks](#community-stacks)

Using one of the Jupyter Docker Stacks requires two choices:

1. Which Docker image you wish to use
2. How you wish to start Docker containers from that image

This section provides details about the first.

## Core Stacks

The Jupyter team maintains a set of Docker image definitions in the <https://github.com/jupyter/docker-stacks> GitHub repository.
The following sections describe these images, including their contents, relationships, and versioning strategy.

### jupyter/base-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/base-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/base-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/base-notebook/tags/)

`jupyter/base-notebook` is a small image supporting the [options common across all core stacks](common.md).
It is the basis for all other stacks and contains:

- Minimally-functional Jupyter Notebook server (e.g., no LaTeX support for saving notebooks as PDFs)
- [Miniforge](https://github.com/conda-forge/miniforge) Python 3.x in `/opt/conda` with two package managers
  - [conda](https://github.com/conda/conda): "cross-platform, language-agnostic binary package manager".
  - [mamba](https://github.com/mamba-org/mamba): "reimplementation of the conda package manager in C++". We use this package manager by default when installing packages.
- `notebook`, `jupyterhub` and `jupyterlab` packages
- No preinstalled scientific computing packages
- Unprivileged user `jovyan` (`uid=1000`, configurable, [see options in the common features section](./common.md) of this documentation) in group `users` (`gid=100`)
  with ownership over the `/home/jovyan` and `/opt/conda` paths
- `tini` as the container entrypoint and a `start-notebook.sh` script as the default command
- A `start-singleuser.sh` script useful for launching containers in JupyterHub
- A `start.sh` script useful for running alternative commands in the container (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
- Options for a self-signed HTTPS certificate and passwordless sudo

### jupyter/minimal-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/minimal-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/minimal-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/minimal-notebook/tags/)

`jupyter/minimal-notebook` adds command-line tools useful when working in Jupyter applications.

It contains:

- Everything in `jupyter/base-notebook`
- [TeX Live](https://www.tug.org/texlive/) for notebook document conversion
- [git](https://git-scm.com/),
  [vi](https://www.vim.org) (actually `vim-tiny`),
  [nano](https://www.nano-editor.org/) (actually `nano-tiny`), `tzdata`, and `unzip`

### jupyter/r-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/r-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/r-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/r-notebook/tags/)

`jupyter/r-notebook` includes popular packages from the R ecosystem listed below:

- Everything in `jupyter/minimal-notebook` and its ancestor images
- The [R](https://www.r-project.org/) interpreter and base environment
- [IRKernel](https://irkernel.github.io/) to support R code in Jupyter notebooks
- [tidyverse](https://www.tidyverse.org/)
  packages from [conda-forge](https://conda-forge.org/feedstock-outputs/index.html)
- [caret](https://topepo.github.io/caret/index.html),
  [crayon](https://cran.r-project.org/web/packages/crayon/index.html),
  [devtools](https://cran.r-project.org/web/packages/devtools/index.html),
  [forecast](https://cran.r-project.org/web/packages/forecast/index.html),
  [hexbin](https://cran.r-project.org/web/packages/hexbin/index.html),
  [htmltools](https://cran.r-project.org/web/packages/htmltools/index.html),
  [htmlwidgets](https://www.htmlwidgets.org),
  [nycflights13](https://cran.r-project.org/web/packages/nycflights13/index.html),
  [randomforest](https://cran.r-project.org/web/packages/randomForest/index.html),
  [rcurl](https://cran.r-project.org/web/packages/RCurl/index.html),
  [rmarkdown](https://rmarkdown.rstudio.com),
  [rodbc](https://cran.r-project.org/web/packages/RODBC/index.html),
  [rsqlite](https://cran.r-project.org/web/packages/RSQLite/index.html),
  [shiny](https://shiny.rstudio.com/),
  [tidymodels](https://www.tidymodels.org/),
  [unixodbc](http://www.unixodbc.org)
  packages from [conda-forge](https://conda-forge.org/feedstock-outputs/index.html)

### jupyter/scipy-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/scipy-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/scipy-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/scipy-notebook/tags/)

`jupyter/scipy-notebook` includes popular packages from the scientific Python ecosystem.

- Everything in `jupyter/minimal-notebook` and its ancestor images
- [altair](https://altair-viz.github.io),
  [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/),
  [bokeh](https://docs.bokeh.org/en/latest/),
  [bottleneck](https://bottleneck.readthedocs.io/en/latest/),
  [cloudpickle](https://github.com/cloudpipe/cloudpickle),
  [conda-forge::blas=\*=openblas](https://www.openblas.net),
  [cython](https://cython.org),
  [dask](https://www.dask.org/),
  [dill](https://pypi.org/project/dill/),
  [h5py](https://www.h5py.org),
  [matplotlib-base](https://matplotlib.org/),
  [numba](https://numba.pydata.org/),
  [numexpr](https://github.com/pydata/numexpr),
  [openpyxl](https://openpyxl.readthedocs.io/en/stable/),
  [pandas](https://pandas.pydata.org/),
  [patsy](https://patsy.readthedocs.io/en/latest/),
  [protobuf](https://developers.google.com/protocol-buffers/docs/pythontutorial),
  [pytables](https://www.pytables.org/),
  [scikit-image](https://scikit-image.org),
  [scikit-learn](https://scikit-learn.org/stable/),
  [scipy](https://scipy.org/),
  [seaborn](https://seaborn.pydata.org/),
  [sqlalchemy](https://www.sqlalchemy.org/),
  [statsmodel](https://www.statsmodels.org/stable/index.html),
  [sympy](https://www.sympy.org/en/index.html),
  [widgetsnbextension](https://ipywidgets.readthedocs.io/en/latest/user_install.html#installing-in-classic-jupyter-notebook),
  [xlrd](https://www.python-excel.org)
  packages
- [ipympl](https://github.com/matplotlib/ipympl) and
  [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/)
  for interactive visualizations and plots in Python notebooks
- [Facets](https://github.com/PAIR-code/facets)
  for visualizing machine learning datasets

### jupyter/tensorflow-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/tensorflow-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/tensorflow-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/tensorflow-notebook/tags/)

`jupyter/tensorflow-notebook` includes popular Python deep learning libraries.

- Everything in `jupyter/scipy-notebook` and its ancestor images
- [tensorflow](https://www.tensorflow.org/) machine learning library

### jupyter/datascience-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/datascience-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/datascience-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)

`jupyter/datascience-notebook` includes libraries for data analysis from the Julia, Python, and R
communities.

- Everything in the `jupyter/scipy-notebook` and `jupyter/r-notebook` images, and their ancestor
  images
- [rpy2](https://rpy2.github.io/doc/latest/html/index.html) package
- The [Julia](https://julialang.org/) compiler and base environment
- [IJulia](https://github.com/JuliaLang/IJulia.jl) to support Julia code in Jupyter notebooks
- [HDF5](https://github.com/JuliaIO/HDF5.jl),
  [Gadfly](https://gadflyjl.org/stable/),
  [RDatasets](https://github.com/JuliaStats/RDatasets.jl)
  packages

### jupyter/pyspark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/pyspark-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/pyspark-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/pyspark-notebook/tags/)

`jupyter/pyspark-notebook` includes Python support for Apache Spark.

- Everything in `jupyter/scipy-notebook` and its ancestor images
- [Apache Spark](https://spark.apache.org/) with Hadoop binaries
- [pyarrow](https://arrow.apache.org/docs/python/) library

### jupyter/all-spark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/all-spark-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/all-spark-notebook/Dockerfile) |
[Docker Hub image tags](https://hub.docker.com/r/jupyter/all-spark-notebook/tags/)

`jupyter/all-spark-notebook` includes Python and R support for Apache Spark.

- Everything in `jupyter/pyspark-notebook` and its ancestor images
- [IRKernel](https://irkernel.github.io/) to support R code in Jupyter notebooks
- [rcurl](https://cran.r-project.org/web/packages/RCurl/index.html),
  [sparklyr](https://spark.rstudio.com),
  [ggplot2](https://ggplot2.tidyverse.org)
  packages

### Image Relationships

The following diagram depicts the build dependency tree of the core images. (i.e., the `FROM` statements in their Dockerfiles).
Any given image inherits the complete content of all ancestor images pointing to it.

[![Image inheritance
diagram](../images/inherit.svg)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFzrEKwjAQxvG9T3FkskM3KUrRJ3DTUShJe9XQ9C4kKbWK7266CCmCW_jnd_Apw03fanmDVwbQYidHE-qOKXj9RDjAvsrihxjVSGG80uZ0OcOkwx0sawrg0KD0mAsojqDiqyAOqJj7Kp4lYRGDJj1Ik6B1W5xvtJ0TlZbFiIDk2XWGp2-PA5nMDI9dWZfbXPy-bGWQsSI1-HeJ-7PCzt5K1ydq3RYnjSnW8v0BwS-D-w)

### Builds

Every Monday and whenever a pull request is merged, images are rebuilt and pushed to [the public container registry](https://hub.docker.com/u/jupyter).

### Versioning via image tags

Whenever a docker image is pushed to the container registry, it is tagged with:

- a `latest` tag
- a 12-character git commit SHA like `9e63909e0317`
- a date formatted like `2022-08-04`
- OS version like `ubuntu-22.04`
- a set of software version tags like `python-3.10.5` and `lab-3.4.4`

```{warning}
- Tags before `2022-07-05` were sometimes incorrect. Please, do not rely on them.
- Single-platform images have either `aarch64` or `x86_64` tag prefixes, for example `jupyter/base-notebook:aarch64-python-3.10.5`
```

For stability and reproducibility, you should either reference a date formatted
tag from a date before the current date (in UTC time) or a git commit SHA older
than the latest git commit SHA in the default branch of the
[jupyter/docker-stacks GitHub repository](https://github.com/jupyter/docker-stacks/).

## Community Stacks

The core stacks are but a tiny sample of what's possible when combining Jupyter with other technologies.
We encourage members of the Jupyter community to create their own stacks based on the core images and link them below.
See the [contributing guide](../contributing/stacks.md) for information about how to create your own Jupyter Docker Stack.

| Flavor         | Binder                  | Description                                                                                               |
| -------------- | ----------------------- | --------------------------------------------------------------------------------------------------------- |
| [csharp]       | [![bb]][csharp_b]       | More than 200 Jupyter Notebooks with example **C#** code                                                  |
| [education]    | [![bb]][education_b]    | **`nbgrader`** and `RISE` on top of the `datascience-notebook` image                                      |
| [ihaskell]     | [![bb]][ihaskell_b]     | Based on [**IHaskell**][ihaskell_project]. Includes popular packages and example notebooks                |
| [java]         | [![bb]][java_b]         | [**IJava**][ijava] kernel on top of the `minimal-notebook` image                                          |
| [sage]         | [![bb]][sage_b]         | [**sagemath**][sagemath] kernel on top of the `minimal-notebook` image                                    |
| [cgspatial]    | [![bb]][cgspatial_b]    | Major **geospatial** Python & R libraries on top of the `datascience-notebook` image                      |
| [kotlin]       | [![bb]][kotlin_b]       | [**Kotlin** kernel for Jupyter/IPython][kotlin_kernel] on top of the `base-notebook` image                |
| [transformers] | [![bb]][transformers_b] | [**Transformers**][transformers_lib] and NLP libraries such as `Tensorflow`, `Keras`, `Jax` and `PyTorch` |
| [scraper]      | [![bb]][scraper_b]      | **Scraper** tools (`selenium`, `chromedriver`, `beatifulsoup4`, `requests`) on `minimal-notebook` image   |

[bb]: https://static.mybinder.org/badge_logo.svg
[csharp]: https://github.com/tlinnet/csharp-notebook
[csharp_b]: https://mybinder.org/v2/gh/tlinnet/csharp-notebook/master
[education]: https://github.com/umsi-mads/education-notebook
[education_b]: https://mybinder.org/v2/gh/umsi-mads/education-notebook/master
[ihaskell]: https://github.com/IHaskell/ihaskell-notebook
[ihaskell_b]: https://mybinder.org/v2/gh/jamesdbrock/learn-you-a-haskell-notebook/master?urlpath=lab/tree/ihaskell_examples/ihaskell/IHaskell.ipynb
[ihaskell_project]: https://github.com/IHaskell/IHaskell
[java]: https://github.com/jbindinga/java-notebook
[java_b]: https://mybinder.org/v2/gh/jbindinga/java-notebook/master
[ijava]: https://github.com/SpencerPark/IJava
[sage]: https://github.com/sharpTrick/sage-notebook
[sage_b]: https://mybinder.org/v2/gh/sharpTrick/sage-notebook/master
[sagemath]: https://www.sagemath.org
[cgspatial]: https://github.com/SCiO-systems/cgspatial-notebook
[cgspatial_b]: https://mybinder.org/v2/gh/SCiO-systems/cgspatial-notebook/master
[kotlin]: https://github.com/knonm/kotlin-notebook
[kotlin_b]: https://mybinder.org/v2/gh/knonm/kotlin-notebook/main
[kotlin_kernel]: https://github.com/Kotlin/kotlin-jupyter
[transformers]: https://github.com/ToluClassics/transformers_notebook
[transformers_b]: https://mybinder.org/v2/gh/ToluClassics/transformers_notebook/main
[transformers_lib]: https://huggingface.co/docs/transformers/index
[scraper]: https://github.com/rgriffogoes/scraper-notebook
[scraper_b]: https://mybinder.org/v2/gh/rgriffogoes/scraper-notebook/main

### GPU enabled notebooks

| Flavor             | Description                                                                                                                                                                                                                                                                                                                                              |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GPU-Jupyter][gpu] | Power of your NVIDIA GPU and GPU calculations using Tensorflow and Pytorch in collaborative notebooks. This is done by generating a Dockerfile that consists of the **nvidia/cuda** base image, the well-maintained **docker-stacks** that is integrated as submodule and GPU-able libraries like **Tensorflow**, **Keras** and **PyTorch** on top of it |
| [PRP-GPU][prp_gpu] | PRP (Pacific Research Platform) maintained [registry][prp_reg] for jupyter stack based on NVIDIA CUDA-enabled image. Added the PRP image with Pytorch and some other python packages and GUI Desktop notebook based on <https://github.com/jupyterhub/jupyter-remote-desktop-proxy>.                                                                     |

[gpu]: https://github.com/iot-salzburg/gpu-jupyter
[prp_gpu]: https://gitlab.nrp-nautilus.io/prp/jupyter-stack/-/tree/prp
[prp_reg]: https://gitlab.nrp-nautilus.io/prp/jupyter-stack/container_registry
