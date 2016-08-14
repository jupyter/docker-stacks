{%- set stack_name='minimal-notebook' %}
{%- set base_path='../base-notebook' %}
{%- include 'partial/badges.md' %}

# Minimal Jupyter Notebook Stack

Small image for working in the notebook and installing your own libraries

## What it Gives You

* Fully-functional Jupyter Notebook 4.2.x
* Miniconda Python 3.x
* No preinstalled scientific computing packages
{% include 'partial/gives.md' with context %}

{% include 'partial/basic_use.md' with context %}

{% include 'partial/notebook_options.md' %}

{% include 'partial/docker_options.md' %}

{% include 'partial/ssl_certificates.md' with context %}

{% include 'partial/conda_py3_env.md' with context %}

{% include 'partial/alternative_commands.md' with context %}
