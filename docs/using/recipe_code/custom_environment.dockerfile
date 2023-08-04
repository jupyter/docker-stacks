FROM jupyter/base-notebook

# name your environment and choose the python version
ARG env_name=python38
ARG py_ver=3.8

# you can add additional libraries here
RUN mamba create --yes -p "${CONDA_DIR}/envs/${env_name}" \
    python=${py_ver} \
    'ipykernel' \
    'jupyterlab' && \
    mamba clean --all -f -y

# alternatively, you can comment out the lines above and uncomment those below
# if you'd prefer to use a YAML file present in the docker build context

# COPY --chown=${NB_UID}:${NB_GID} environment.yml /tmp/
# RUN mamba env create -p "${CONDA_DIR}/envs/${env_name}" -f /tmp/environment.yml && \
#     mamba clean --all -f -y

# create Python kernel and link it to jupyter
RUN "${CONDA_DIR}/envs/${env_name}/bin/python" -m ipykernel install --user --name="${env_name}" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# any additional `pip` installs can be added by using the following line
# using `mamba` is highly recommended
RUN "${CONDA_DIR}/envs/${env_name}/bin/pip" install --no-cache-dir \
    'flake8'

# if you do not want this environment to be the default one, comment this line
# hadolint ignore=DL3059
RUN echo "conda activate ${env_name}" >> "${HOME}/.bashrc"
