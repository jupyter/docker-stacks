#!/bin/bash
set -exuo pipefail
# Requirements:
# - Run as the root user

# Install baseline packages to get X and xfce working
apt-get update -qq --yes > /dev/null
apt-get install --yes --no-install-recommends -qq \
    xfce4 \
    xorg \
    dbus-x11 \
    > /dev/null

# Install tigervnc from apt repos - these are newer and more architecture
# appropriate than whatever is bundled with jupyter-remote-desktop-proxy
apt-get install --yes --no-install-recommends -qq \
        tigervnc-standalone-server \
        tigervnc-xorg-extension > /dev/null

# Install add-apt-repositories so we can add PPA for latest firefox
apt-get install --yes --no-install-recommends -qq \
    software-properties-common gpg-agent > /dev/null

# Install Firefox from a PPA - default Ubuntu's Firefox no longer
# provides it via apt, using snap instead. That does not work inside
# containers. We do this before our apt update in the script so that
# needs to run only once.
add-apt-repository ppa:mozillateam/ppa

# Install Firefox from the PPA explicitly
apt-get update -qq --yes > /dev/null
apt-get install -qq --yes -t 'o=LP-PPA-mozillateam' --yes firefox

# Cleanup apt-get update side effects
rm -rf /var/lib/apt/lists/*

# Install packages required for linux desktop VPN setup to work
# websockify and jupyter-server-proxy available from conda-forge, but
# jupyter-remote-desktop-proxy is not.
mamba install -c conda-forge --yes \
      websockify \
      jupyter-server-proxy

python -m pip install --no-cache jupyter-remote-desktop-proxy

fix-permissions "${CONDA_DIR}"
fix-permissions "/home/${NB_USER}"
