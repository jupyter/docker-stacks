{%- set stack_name='base-notebook' %}
{%- set base_path='.' %}
{%- include 'partial/badges.md' %}

# Base Jupyter Notebook Stack

Small base image for defining your own stack

## What it Gives You

* Minimally-functional Jupyter Notebook 4.2.x (e.g., no pandoc for document conversion)
* Miniconda Python 3.x
* No preinstalled scientific computing packages
{% include 'partial/gives.md' with context %}

{% include 'partial/basic_use.md' with context %}

{% include 'partial/notebook_options.md' %}

{% include 'partial/docker_options.md' %}

{% include 'partial/ssl_certificates.md' with context %}

{% include 'partial/conda_py3_env.md' with context %}

{% include 'partial/alternative_commands.md' with context %}
