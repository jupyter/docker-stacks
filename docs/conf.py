# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "docker-stacks"
copyright = "2023, Project Jupyter"
author = "Project Jupyter"

version = "latest"
release = "latest"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# File above was generated using sphinx 5.3.0 with this command:
# sphinx-quickstart --project "docker-stacks" --author "Project Jupyter" -v "latest" -r "latest" -l en --no-sep --no-makefile --no-batchfile
# These are custom options for this project

html_theme = "sphinx_book_theme"
html_title = "Docker Stacks documentation"
html_logo = "_static/jupyter-logo.svg"
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/jupyter/docker-stacks",
    "repository_branch": "main",
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "logo": {
        "text": html_title,
    },
}
html_last_updated_fmt = "%Y-%m-%d"

extensions = ["myst_parser", "sphinx_copybutton", "sphinx_last_updated_by_git"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
pygments_style = "sphinx"

# MyST configuration reference: https://myst-parser.readthedocs.io/en/latest/sphinx/reference.html
myst_heading_anchors = 3

linkcheck_ignore = [
    r".*github\.com.*#",  # javascript based anchors
    r"https://github\.com/jupyter/docker-stacks/settings/actions/runners/new\?arch=arm64\&amp;os=linux",  # only works for users with permissions to change runners
    r"http://127\.0\.0\.1:.*",  # various examples
]

linkcheck_allowed_redirects = {
    r"https://results\.pre-commit\.ci/latest/github/jupyter/docker-stacks/main": r"https://results\.pre-commit\.ci/run/github/.*",  # Latest main CI build
    r"https://github\.com/jupyter/docker-stacks/issues/new.*": r"https://github\.com/login.*",  # GitHub wants user to be logon to use this features
    r"https://github\.com/orgs/jupyter/teams/docker-image-maintainers/members": r"https://github\.com/login.*",
}
