#!/bin/bash

set -exuo pipefail

# Figure out what architecture we are building for
JULIA_ARCH=$(uname -m)
JULIA_SHORT_ARCH="${JULIA_ARCH}"
if [ "${JULIA_SHORT_ARCH}" == "x86_64" ]; then
    JULIA_SHORT_ARCH="x64"
fi

# Figure out Julia Installer URL
JULIA_INSTALLER="julia-${JULIA_VERSION}-linux-${JULIA_ARCH}.tar.gz"
JULIA_MAJOR_MINOR=$(echo "${JULIA_VERSION}" | cut -d. -f 1,2)

# Download and install Julia
mkdir "/opt/julia-${JULIA_VERSION}"
wget --progress=dot:giga "https://julialang-s3.julialang.org/bin/linux/${JULIA_SHORT_ARCH}/${JULIA_MAJOR_MINOR}/${JULIA_INSTALLER}"
tar xzf "${JULIA_INSTALLER}" -C "/opt/julia-${JULIA_VERSION}" --strip-components=1
rm "${julia_installer}"

# Link Julia installed version to /usr/local/bin, so julia launches it
ln -fs /opt/julia-*/bin/julia /usr/local/bin/julia

# Tell Julia where conda libraries are
mkdir -p /etc/julia
echo "push!(Libdl.DL_LOAD_PATH, \"${CONDA_DIR}/lib\")" >> /etc/julia/juliarc.jl

# Create JULIA_PKGDIR, where user libraries are installed
mkdir "${JULIA_PKGDIR}"
chown "${NB_USER}" "${JULIA_PKGDIR}"
fix-permissions "${JULIA_PKGDIR}"
