#!/bin/bash
# Requirements:
# - Run as non-root user
# - Julia is already set up, with the setup-julia.bash command
set -exuo pipefail

# Install base Julia packages
julia -e '
import Pkg;
Pkg.update();
Pkg.add([
    "HDF5",
    "IJulia"
]);
Pkg.precompile();
'

# Move the kernelspec out to the system share location. Avoids
# problems with runtime UID change not taking effect properly on the
# .local folder in the jovyan home dir.  move kernelspec out of home
mv "${HOME}/.local/share/jupyter/kernels/julia"* "${CONDA_DIR}/share/jupyter/kernels/"
chmod -R go+rx "${CONDA_DIR}/share/jupyter"
rm -rf "${HOME}/.local"
fix-permissions "${JULIA_PKGDIR}" "${CONDA_DIR}/share/jupyter"
