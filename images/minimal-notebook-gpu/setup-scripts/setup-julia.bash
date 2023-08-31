#!/bin/bash
set -exuo pipefail
# Requirements:
# - Run as the root user
# - The JULIA_PKGDIR environment variable is set

# Default julia version to install if env var is not set
# Check https://julialang.org/downloads/
JULIA_VERSION="${JULIA_VERSION:-1.9.3}"

# Figure out what architecture we are installing in
JULIA_ARCH=$(uname -m)
JULIA_SHORT_ARCH="${JULIA_ARCH}"
if [ "${JULIA_SHORT_ARCH}" == "x86_64" ]; then
    JULIA_SHORT_ARCH="x64"
fi

# Figure out Julia Installer URL
JULIA_INSTALLER="julia-${JULIA_VERSION}-linux-${JULIA_ARCH}.tar.gz"
JULIA_MAJOR_MINOR=$(echo "${JULIA_VERSION}" | cut -d. -f 1,2)

# Download and install Julia
cd /tmp
mkdir "/opt/julia-${JULIA_VERSION}"
curl --progress-bar --location --output "${JULIA_INSTALLER}" \
    "https://julialang-s3.julialang.org/bin/linux/${JULIA_SHORT_ARCH}/${JULIA_MAJOR_MINOR}/${JULIA_INSTALLER}"
tar xzf "${JULIA_INSTALLER}" -C "/opt/julia-${JULIA_VERSION}" --strip-components=1
rm "${JULIA_INSTALLER}"

# Link Julia installed version to /usr/local/bin, so julia launches it
ln -fs /opt/julia-*/bin/julia /usr/local/bin/julia

# Tell Julia where conda libraries are
mkdir -p /etc/julia
echo "push!(Libdl.DL_LOAD_PATH, \"${CONDA_DIR}/lib\")" >> /etc/julia/juliarc.jl

# Create JULIA_PKGDIR, where user libraries are installed
mkdir "${JULIA_PKGDIR}"
chown "${NB_USER}" "${JULIA_PKGDIR}"
fix-permissions "${JULIA_PKGDIR}"
