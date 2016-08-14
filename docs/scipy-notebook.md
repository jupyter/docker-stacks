{%- set stack_name='scipy-notebook' %}
{%- set base_path='../base-notebook' %}
{%- include 'partial/badges.md' %}

# Jupyter Notebook Scientific Python Stack

## What it Gives You

* Jupyter Notebook 4.2.x
* Conda Python 3.x and Python 2.7.x environments
* pandas, matplotlib, scipy, seaborn, scikit-learn, scikit-image, sympy, cython, patsy, statsmodel, cloudpickle, dill, numba, bokeh pre-installed
{% include 'partial/gives.md' with context %}

{% include 'partial/basic_use.md' with context %}

{% include 'partial/notebook_options.md' %}

{% include 'partial/docker_options.md' %}

{% include 'partial/ssl_certificates.md' with context %}

{% include 'partial/conda_py23_env.md' %}

{% include 'partial/alternative_commands.md' with context %}
