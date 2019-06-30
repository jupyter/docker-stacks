# Selecting an Image

* [Core Stacks](#core-stacks)
* [Image Relationships](#image-relationships)
* [Community Stacks](#community-stacks)

Using one of the Jupyter Docker Stacks requires two choices:

1. Which Docker image you wish to use
2. How you wish to start Docker containers from that image

This section provides details about the first.

## Core Stacks

The Jupyter team maintains a set of Docker image definitions in the [https://github.com/jupyter/docker-stacks](https://github.com/jupyter/docker-stacks) GitHub repository. The following sections describe these images including their contents, relationships, and versioning strategy.

### jupyter/base-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/base-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/base-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/base-notebook/tags/)

`jupyter/base-notebook` is a small image supporting the [options common across all core stacks](common.md). It is the basis for all other stacks.

* Minimally-functional Jupyter Notebook server (e.g., no [pandoc](https://pandoc.org/) for saving notebooks as PDFs)
* [Miniconda](https://conda.io/miniconda.html) Python 3.x in `/opt/conda`
* No preinstalled scientific computing packages
* Unprivileged user `jovyan` (`uid=1000`, configurable, see options) in group `users` (`gid=100`) with ownership over the `/home/jovyan` and `/opt/conda` paths
* `tini` as the container entrypoint and a `start-notebook.sh` script as the default command
* A `start-singleuser.sh` script useful for launching containers in JupyterHub
* A `start.sh` script useful for running alternative commands in the container (e.g. `ipython`, `jupyter kernelgateway`, `jupyter lab`)
* Options for a self-signed HTTPS certificate and passwordless sudo

### jupyter/minimal-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/minimal-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/minimal-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/minimal-notebook/tags/)

`jupyter/minimal-notebook` adds command line tools useful when working in Jupyter applications.

* Everything in `jupyter/base-notebook`
* [Pandoc](http://pandoc.org) and [TeX Live](https://www.tug.org/texlive/) for notebook document conversion
* [git](https://git-scm.com/), [emacs](https://www.gnu.org/software/emacs/), [jed](https://www.jedsoft.org/jed/), [nano](https://www.nano-editor.org/), tzdata, and unzip

### jupyter/r-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/r-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/r-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/r-notebook/tags/)

`jupyter/r-notebook` includes popular packages from the R ecosystem.

* Everything in `jupyter/minimal-notebook` and its ancestor images
* The [R](https://www.r-project.org/) interpreter and base environment
* [IRKernel](https://irkernel.github.io/) to support R code in Jupyter notebooks
* [tidyverse](https://www.tidyverse.org/) packages, including [ggplot2](http://ggplot2.org/), [dplyr](http://dplyr.tidyverse.org/), [tidyr](http://tidyr.tidyverse.org/), [readr](http://readr.tidyverse.org/), [purrr](http://purrr.tidyverse.org/), [tibble](http://tibble.tidyverse.org/), [stringr](http://stringr.tidyverse.org/), [lubridate](http://lubridate.tidyverse.org/), and [broom](https://cran.r-project.org/web/packages/broom/vignettes/broom.html) from [conda-forge](https://conda-forge.github.io/feedstocks)
* [plyr](https://cran.r-project.org/web/packages/plyr/index.html), [devtools](https://cran.r-project.org/web/packages/devtools/index.html), [shiny](https://shiny.rstudio.com/), [rmarkdown](http://rmarkdown.rstudio.com/), [forecast](https://cran.r-project.org/web/packages/forecast/forecast.pdf), [rsqlite](https://cran.r-project.org/web/packages/RSQLite/index.html), [reshape2](https://cran.r-project.org/web/packages/reshape2/reshape2.pdf), [nycflights13](https://cran.r-project.org/web/packages/nycflights13/index.html), [caret](http://topepo.github.io/caret/index.html), [rcurl](https://cran.r-project.org/web/packages/RCurl/index.html), and [randomforest](https://cran.r-project.org/web/packages/randomForest/randomForest.pdf) packages from [conda-forge](https://conda-forge.github.io/feedstocks)

### jupyter/scipy-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/scipy-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/scipy-notebook/tags/)

`jupyter/scipy-notebook` includes popular packages from the scientific Python ecosystem.

* Everything in `jupyter/minimal-notebook` and its ancestor images
* [pandas](https://pandas.pydata.org/), [numexpr](https://github.com/pydata/numexpr), [matplotlib](https://matplotlib.org/), [scipy](https://www.scipy.org/), [seaborn](https://seaborn.pydata.org/), [scikit-learn](http://scikit-learn.org/stable/), [scikit-image](http://scikit-image.org/), [sympy](http://www.sympy.org/en/index.html), [cython](http://cython.org/), [patsy](https://patsy.readthedocs.io/en/latest/), [statsmodel](http://www.statsmodels.org/stable/index.html), [cloudpickle](https://github.com/cloudpipe/cloudpickle), [dill](https://pypi.python.org/pypi/dill), [numba](https://numba.pydata.org/), [bokeh](https://bokeh.pydata.org/en/latest/), [sqlalchemy](https://www.sqlalchemy.org/), [hdf5](http://www.h5py.org/), [vincent](http://vincent.readthedocs.io/en/latest/), [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/), [protobuf](https://developers.google.com/protocol-buffers/docs/pythontutorial), and [xlrd](http://www.python-excel.org/) packages
* [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/) for interactive visualizations in Python notebooks
* [Facets](https://github.com/PAIR-code/facets) for visualizing machine learning datasets

### jupyter/tensorflow-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/tensorflow-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/tensorflow-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/tensorflow-notebook/tags/)

`jupyter/tensorflow-notebook` includes popular Python deep learning libraries.

* Everything in `jupyter/scipy-notebook` and its ancestor images
* [tensorflow](https://www.tensorflow.org/) and [keras](https://keras.io/) machine learning libraries

### jupyter/datascience-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/datascience-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/datascience-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/datascience-notebook/tags/)

`jupyter/datascience-notebook` includes libraries for data analysis from the Julia, Python, and R communities.

* Everything in the `jupyter/scipy-notebook` and `jupyter/r-notebook` images, and their ancestor images
* The [Julia](https://julialang.org/) compiler and base environment
* [IJulia](https://github.com/JuliaLang/IJulia.jl) to support Julia code in Jupyter notebooks
* [HDF5](https://github.com/JuliaIO/HDF5.jl), [Gadfly](http://gadflyjl.org/stable/), and [RDatasets](https://github.com/johnmyleswhite/RDatasets.jl) packages

### jupyter/pyspark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/pyspark-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/pyspark-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/pyspark-notebook/tags/)

`jupyter/pyspark-notebook` includes Python support for Apache Spark, optionally on Mesos.

* Everything in `jupyter/scipy-notebook` and its ancestor images
* [Apache Spark](https://spark.apache.org/) with Hadoop binaries
* [Mesos](http://mesos.apache.org/) client libraries

### jupyter/all-spark-notebook

[Source on GitHub](https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook)
| [Dockerfile commit history](https://github.com/jupyter/docker-stacks/commits/master/all-spark-notebook/Dockerfile)
| [Docker Hub image tags](https://hub.docker.com/r/jupyter/all-spark-notebook/tags/)

`jupyter/all-spark-notebook` includes Python, R, and Scala support for Apache Spark, optionally on Mesos.

* Everything in `jupyter/pyspark-notebook` and its ancestor images
* [IRKernel](https://irkernel.github.io/) to support R code in Jupyter notebooks
* [Apache Toree](https://toree.apache.org/) and [spylon-kernel](https://github.com/maxpoint/spylon-kernel) to support Scala code in Jupyter notebooks
* [ggplot2](http://ggplot2.org/), [sparklyr](http://spark.rstudio.com/), and [rcurl](https://cran.r-project.org/web/packages/RCurl/index.html) packages

### Image Relationships

The following diagram depicts the build dependency tree of the core images. (i.e., the `FROM` statements in their Dockerfiles). Any given image inherits the complete content of all ancestor images pointing to it.

[![Image inheritance diagram](../images/inherit.svg)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFzTEPgjAQhuHdX9Gws5sQjGzujsaYKxzmQrlr2msMGv-71K0srO_3XGud9NNA8DSfgzESCFlBSdi0xkvQAKTNugw4QnL6GIU10hvX-Zh7Z24OLLq2SjaxpvP10lX35vCf6pOxELFmUbQiUz4oQhYzMc3gCrRt2cWe_FKosmSjyFHC6OS1AwdQWCtyj7sfh523_BI9hKlQ25YdOFdv5fcH0kiEMA)

### Builds

Pull requests to the `jupyter/docker-stacks` repository trigger builds of all images on Travis CI. These images are for testing purposes only and are not saved for use. When pull requests merge to master, all images rebuild on Docker Cloud and become available to `docker pull` from Docker Hub.

### Versioning

The `latest` tag in each Docker Hub repository tracks the master branch `HEAD` reference on GitHub. `latest` is a moving target, by definition, and will have backward-incompatible changes regularly.

Every image on Docker Hub also receives a 12-character tag which corresponds with the git commit SHA that triggered the image build. You can inspect the state of the `jupyter/docker-stacks` repository for that commit to review the definition of the image (e.g., images with tag 7c45ec67c8e7 were built from [https://github.com/jupyter/docker-stacks/tree/7c45ec67c8e7](https://github.com/jupyter/docker-stacks/tree/7c45ec67c8e7)).

You must refer to git-SHA image tags when stability and reproducibility are important in your work. (e.g. `FROM jupyter/scipy-notebook:7c45ec67c8e7`, `docker run -it --rm jupyter/scipy-notebook:7c45ec67c8e7`). You should only use `latest` when a one-off container instance is acceptable (e.g., you want to briefly try a new library in a notebook).

## Community Stacks

The core stacks are just a tiny sample of what's possible when combining Jupyter with other technologies. We encourage members of the Jupyter community to create their own stacks based on the core images and link them below.

* [csharp-notebook is a community Jupyter Docker Stack image. Try C# in Jupyter Notebooks](https://github.com/tlinnet/csharp-notebook). The image includes more than 200 Jupyter Notebooks with example C# code and can readily be tried online via mybinder.org. Click here to launch [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tlinnet/csharp-notebook/master).

* [education-notebook is a community Jupyter Docker Stack image](https://github.com/umsi-mads/education-notebook). The image includes nbgrader and RISE on top of the datascience-notebook image. Click here to launch it on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/umsi-mads/education-notebook/master).

* __crosscompass/ihaskell-notebook__

  [Source on GitHub](https://github.com/jamesdbrock/ihaskell-notebook)
  | [Dockerfile commit history](https://github.com/jamesdbrock/ihaskell-notebook/commits/master/Dockerfile)
  | [Docker Hub image tags](https://hub.docker.com/r/crosscompass/ihaskell-notebook/tags)

  `crosscompass/ihaskell-notebook` is based on [IHaskell](https://github.com/gibiansky/IHaskell). Includes popular packages and example notebooks.

  Try it on binder: [![launch Learn You a Haskell for Great Good!](https://img.shields.io/badge/launch-Learn%20You%20A%20Haskell%20For%20Great%20Good!-579ACA.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/jamesdbrock/learn-you-a-haskell-notebook/master?urlpath=lab/tree/learn_you_a_haskell/00-preface.ipynb)

See the [contributing guide](../contributing/stacks.md) for information about how to create your own Jupyter Docker Stack.
