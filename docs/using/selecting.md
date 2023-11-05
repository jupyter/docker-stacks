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

### jupyter/docker-stacks-foundation

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/docker-stacks-foundation) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/docker-stacks-foundation/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/docker-stacks-foundation?tab=tags)

`jupyter/docker-stacks-foundation` is a small image supporting a majority of [options common across all core stacks](common.md).
It is the basis for all other stacks on which Jupyter-related applications can be built
(e.g., kernel-based containers, [nbclient](https://github.com/jupyter/nbclient) applications, etc.).
As such, it does not contain application-level software like JupyterLab, Jupyter Notebook or JupyterHub.

It contains:

- Package managers
  - [conda](https://github.com/conda/conda): "cross-platform, language-agnostic binary package manager".
  - [mamba](https://github.com/mamba-org/mamba): "reimplementation of the conda package manager in C++". We use this package manager by default when installing packages.
- Unprivileged user `jovyan` (`uid=1000`, configurable, [see options in the common features section](./common.md) of this documentation) in group `users` (`gid=100`)
  with ownership over the `/home/jovyan` and `/opt/conda` paths
- `tini` as the container entry point
- A `start.sh` script as the default command - useful for running alternative commands in the container as applications are added (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
- A `run-hooks.sh` script, which can source/run files in a given directory
- Options for a passwordless sudo
- Common system libraries like `bzip2`, `ca-certificates`, `locales`
- `wget` to download external files
- No preinstalled scientific computing packages

### jupyter/base-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/base-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/base-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/base-notebook?tab=tags)

`jupyter/base-notebook` adds base Jupyter Applications like JupyterLab, Jupyter Notebook, JupyterHub and NBClassic
and serves as the basis for all other stacks besides `jupyter/docker-stacks-foundation`.

It contains:

- Everything in `jupyter/docker-stacks-foundation`
- Minimally functional Server (e.g., no LaTeX support for saving notebooks as PDFs)
- `notebook`, `jupyterhub` and `jupyterlab` packages
- A `start-notebook.py` script as the default command
- A `start-singleuser.py` script useful for launching containers in JupyterHub
- Options for a self-signed HTTPS certificate

```{warning}
`jupyter/base-notebook` also contains `start-notebook.sh` and `start-singleuser.sh` files to maintain backwards compatibility.
External config that explicitly refers to those files should instead
update to refer to `start-notebook.py` and `start-singleuser.py`.
The shim `.sh` files will be removed at some future date.
```

### jupyter/minimal-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/minimal-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/minimal-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/minimal-notebook?tab=tags)

`jupyter/minimal-notebook` adds command-line tools useful when working in Jupyter applications.

It contains:

- Everything in `jupyter/base-notebook`
- Common useful utilities like
  [curl](https://curl.se),
  [git](https://git-scm.com/),
  [nano](https://www.nano-editor.org/) (actually `nano-tiny`),
  [tzdata](https://www.iana.org/time-zones),
  [unzip](https://code.launchpad.net/ubuntu/+source/unzip)
  and [vi](https://www.vim.org) (actually `vim-tiny`),
- [TeX Live](https://www.tug.org/texlive/) for notebook document conversion

### jupyter/r-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/r-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/r-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/r-notebook?tab=tags)

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
  [shiny](https://shiny.posit.co),
  [tidymodels](https://www.tidymodels.org/),
  [unixodbc](https://www.unixodbc.org)
  packages from [conda-forge](https://conda-forge.org/feedstock-outputs/index.html)

### jupyter/julia-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/julia-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/julia-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/julia-notebook?tab=tags)

`jupyter/julia-notebook` includes popular packages from the Julia ecosystem listed below:

- Everything in `jupyter/minimal-notebook` and its ancestor images
- The [Julia](https://julialang.org/) compiler and base environment
- [IJulia](https://github.com/JuliaLang/IJulia.jl) to support Julia code in Jupyter notebook
- [Pluto.jl](https://plutojl.org/) reactive Julia notebook interface, made accessible with [jupyter-pluto-proxy](https://github.com/yuvipanda/jupyter-pluto-proxy)
- [HDF5](https://github.com/JuliaIO/HDF5.jl) package

### jupyter/scipy-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/scipy-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/scipy-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/scipy-notebook?tab=tags)

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
  [jupyterlab-git](https://github.com/jupyterlab/jupyterlab-git),
  [matplotlib-base](https://matplotlib.org/),
  [numba](https://numba.pydata.org/),
  [numexpr](https://github.com/pydata/numexpr),
  [openpyxl](https://openpyxl.readthedocs.io/en/stable/),
  [pandas](https://pandas.pydata.org/),
  [patsy](https://patsy.readthedocs.io/en/latest/),
  [protobuf](https://protobuf.dev/getting-started/pythontutorial/),
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

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/tensorflow-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/tensorflow-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/tensorflow-notebook?tab=tags)

`jupyter/tensorflow-notebook` includes popular Python deep learning libraries.

- Everything in `jupyter/scipy-notebook` and its ancestor images
- [tensorflow](https://www.tensorflow.org/) machine learning library

### jupyter/datascience-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/datascience-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/datascience-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/datascience-notebook?tab=tags)

`jupyter/datascience-notebook` includes libraries for data analysis from the Python, and R, and Julia communities.

- Everything in the `jupyter/scipy-notebook`, `jupyter/r-notebook`, and `jupyter/julia-notebook` images and their ancestor
  images
- [rpy2](https://rpy2.github.io/doc/latest/html/index.html) package

### jupyter/pyspark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/pyspark-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/pyspark-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/pyspark-notebook?tab=tags)

`jupyter/pyspark-notebook` includes Python support for Apache Spark.

- Everything in `jupyter/scipy-notebook` and its ancestor images
- [Apache Spark](https://spark.apache.org/) with Hadoop binaries
- [grpcio-status](https://github.com/grpc/grpc/tree/master/src/python/grpcio_status)
- [grpcio](https://grpc.io/docs/languages/python/quickstart/)
- [pyarrow](https://arrow.apache.org/docs/python/)

### jupyter/all-spark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/main/images/all-spark-notebook) |
[Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/main/images/all-spark-notebook/Dockerfile) |
[Quay.io image tags](https://quay.io/repository/jupyter/all-spark-notebook?tab=tags)

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
diagram](../images/inherit.svg)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFjkFuwkAMRfecwsqKLuYACMEJuqPLSshJHDAZ7GjGIwSIuzPTRaWJWmX7_vP_br12Y894gucKoKcBk7fjoGKRHwQ72Gwz18AkhsYqGU0aLCDbdpWjJrVJLH3L-vPrADe2c85ZDAJ5wkgfDbg99HmFgouG3RjdoEn6n7ZS_l9W7trc4ESNWtWxyBUoxpWFr-grac6KFzue7pVVk-I0RhI1DF5vv7z5W80vYqYkHS1Oh0XjkjzjwnPTPU4Yxsqas-Kh925uvt4imKoO)

### Builds

Every Monday and whenever a pull request is merged, images are rebuilt and pushed to [the public container registry](https://quay.io/organization/jupyter).

### Versioning via image tags

Whenever a docker image is pushed to the container registry, it is tagged with:

- a `latest` tag
- a 12-character git commit SHA like `1ffe43816ba9`
- a date formatted like `2023-01-30`
- OS version like `ubuntu-22.04`
- a set of software version tags like `python-3.10.8` and `lab-3.5.3`

```{warning}
- Tags before `2022-07-05` were sometimes incorrect.
  Please, do not rely on them.
- Single-platform images have either `aarch64` or `x86_64` tag prefixes, for example, `jupyter/base-notebook:aarch64-python-3.10.5`
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
| [almond]       | [![bb]][almond_b]       | Scala kernel for Jupyter using **Almond** on top of the `base-notebook` image                             |

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
[almond]: https://almond.sh
[almond_b]: https://mybinder.org/v2/gh/almond-sh/examples/master?urlpath=lab%2Ftree%2Fnotebooks%2Findex.ipynb

### GPU accelerated notebooks

| Flavor             | Description                                                                                                                                                                                                                                                                                                                                                 |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GPU-Jupyter][gpu] | Power of your NVIDIA GPU and GPU calculations using Tensorflow and Pytorch in collaborative notebooks. This is done by generating a Dockerfile that consists of the **nvidia/cuda** base image, the well-maintained **docker-stacks** that is integrated as a submodule and GPU-able libraries like **Tensorflow**, **Keras** and **PyTorch** on top of it. |
| [PRP-GPU][prp_gpu] | PRP (Pacific Research Platform) maintained [registry][prp_reg] for jupyter stack based on NVIDIA CUDA-enabled image. Added the PRP image with Pytorch and some other python packages and GUI Desktop notebook based on <https://github.com/jupyterhub/jupyter-remote-desktop-proxy>.                                                                        |
| [b-data][b-data]   | GPU accelerated, multi-arch (`linux/amd64`, `linux/arm64/v8`) docker images for [R][r_cuda], [Python][python_cuda] and [Julia][julia_cuda]. Derived from nvidia/cuda `devel`-flavored images, including TensortRT and TensorRT plugin libraries. With [code-server][code-server] next to JupyterLab. Just Python – no [Conda][conda]/[Mamba][mamba].        |

[gpu]: https://github.com/iot-salzburg/gpu-jupyter
[prp_gpu]: https://gitlab.nrp-nautilus.io/prp/jupyter-stack/-/tree/prp
[prp_reg]: https://gitlab.nrp-nautilus.io/prp/jupyter-stack/container_registry
[b-data]: https://github.com/b-data
[r_cuda]: https://github.com/b-data/jupyterlab-r-docker-stack/blob/main/CUDA.md
[python_cuda]: https://github.com/b-data/jupyterlab-python-docker-stack/blob/main/CUDA.md
[julia_cuda]: https://github.com/b-data/jupyterlab-julia-docker-stack/blob/main/CUDA.md
[code-server]: https://github.com/coder/code-server
[conda]: https://github.com/conda/conda
[mamba]: https://github.com/mamba-org/mamba
