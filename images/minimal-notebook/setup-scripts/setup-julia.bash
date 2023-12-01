#!/bin/bash
set -exuo pipefail
# Requirements:
# - Run as the root user
# - The JULIA_PKGDIR environment variable is set

# Get the last stable version of Julia
# https://github.com/JuliaLang/www.julialang.org/issues/878#issuecomment-749234813

JULIA_LATEST_INFO=$(
    wget -O - -o /dev/null 'https://julialang-s3.julialang.org/bin/versions.json' |
    jq '
        with_entries(select(.value.stable==true)) |
        to_entries |
        max_by(.key).value.files |
        .[]
    ' |
    jq "select(.triplet == \"$(uname -m)-linux-gnu\")"
)
JULIA_INSTALLER_URL=$(echo "${JULIA_LATEST_INFO}" | jq --raw-output ".url")
JULIA_VERSION=$(echo "${JULIA_LATEST_INFO}" | jq --raw-output ".version")

# Download and install Julia
cd /tmp
mkdir "/opt/julia-${JULIA_VERSION}"
curl --progress-bar --location --output /tmp/julia.tar.gz "${JULIA_INSTALLER_URL}"
tar xzf /tmp/julia.tar.gz -C "/opt/julia-${JULIA_VERSION}" --strip-components=1
rm /tmp/julia.tar.gz

# Link Julia installed version to /usr/local/bin, so julia launches it
ln -fs /opt/julia-*/bin/julia /usr/local/bin/julia

# Tell Julia where conda libraries are
mkdir -p /etc/julia
echo "push!(Libdl.DL_LOAD_PATH, \"${CONDA_DIR}/lib\")" >> /etc/julia/juliarc.jl

# Create JULIA_PKGDIR, where user libraries are installed
mkdir "${JULIA_PKGDIR}"
chown "${NB_USER}" "${JULIA_PKGDIR}"
fix-permissions "${JULIA_PKGDIR}"
