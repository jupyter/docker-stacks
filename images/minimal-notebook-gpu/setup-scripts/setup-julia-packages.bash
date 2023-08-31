#!/bin/bash
set -exuo pipefail
# Requirements:
# - Run as non-root user
# - The JULIA_PKGDIR environment variable is set
# - Julia is already set up, with the setup-julia.bash command

# Install base Julia packages
julia -e '
import Pkg;
Pkg.update();
Pkg.add([
    "HDF5",
    "IJulia",
    "Pluto"
]);
Pkg.precompile();
'

# Move the kernelspec out of ${HOME} to the system share location.
# Avoids problems with runtime UID change not taking effect properly
# on the .local folder in the jovyan home dir.
mv "${HOME}/.local/share/jupyter/kernels/julia"* "${CONDA_DIR}/share/jupyter/kernels/"
chmod -R go+rx "${CONDA_DIR}/share/jupyter"
rm -rf "${HOME}/.local"
fix-permissions "${JULIA_PKGDIR}" "${CONDA_DIR}/share/jupyter"

# Install jupyter-pluto-proxy to get Pluto to work on JupyterHub
mamba install --yes \
    'jupyter-pluto-proxy' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
