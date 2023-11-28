#!/bin/bash
set -exuo pipefail
# Requirements:
# - Run as a non-root user
# - The JULIA_PKGDIR environment variable is set
# - Julia is already set up, with the setup-julia.bash command


# For amd64 (x86_64), we should specify what specific targets the precompilation should be done for.
# If we don't specify it, it's *only* done for the target of the host doing the compilation.
# When the container runs on a host that's still x86_64, but a *different* generation of CPU
# than what the build host was, the precompilation is useless and Julia takes a long long time
# to start up. This specific multitarget comes from https://docs.julialang.org/en/v1/devdocs/sysimg/#Specifying-multiple-system-image-targets,
# and is the same set of options that the official Julia x86_64 build is compiled with.
# If the architecture the container runs on is different, precompilation may still have to be
# re-done on first startup - but this *should* catch most of the issues.
# See https://github.com/jupyter/docker-stacks/issues/2015 for more information
if [ "$(uname -m)" == "x86_64" ]; then
    export JULIA_CPU_TARGET="generic;sandybridge,-xsaveopt,clone_all;haswell,-rdrnd,base(1)"
fi

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
