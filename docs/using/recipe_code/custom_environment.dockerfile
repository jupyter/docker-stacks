FROM quay.io/jupyter/base-notebook

# Name your environment and choose the Python version
ARG env_name=python310
ARG py_ver=3.10

# You can add additional libraries here
RUN mamba create --yes -p "${CONDA_DIR}/envs/${env_name}" \
    python=${py_ver} \
    'ipykernel' \
    'jupyterlab' && \
    mamba clean --all -f -y

# Alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml /tmp/
# RUN mamba env create -p "${CONDA_DIR}/envs/${env_name}" -f /tmp/environment.yml && \
#     mamba clean --all -f -y

# Create Python kernel and link it to jupyter
RUN "${CONDA_DIR}/envs/${env_name}/bin/python" -m ipykernel install --user --name="${env_name}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Any additional `pip` installs can be added by using the following line
# Using `mamba` is highly recommended though
RUN "${CONDA_DIR}/envs/${env_name}/bin/pip" install --no-cache-dir \
    'flake8'

# This changes a startup hook, which will activate our custom environment by default in Jupyter Notebook and Terminal
# More information here: https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/activate_conda_env.sh
USER root
RUN echo conda activate "${env_name}" >> /usr/local/bin/before-notebook.d/activate_conda_env.sh

USER ${NB_UID}
