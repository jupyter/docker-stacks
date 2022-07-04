#!/bin/bash -e

GITHUB_RUNNER_USER="runner-user"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

apt-get update --yes
apt-get upgrade --yes

echo "Creating runner-user, who will run GitHub Actions runner"
adduser --disabled-password --gecos "" ${GITHUB_RUNNER_USER}

echo "Setting up python3"
apt-get install --yes --no-install-recommends python3
curl -sS https://bootstrap.pypa.io/get-pip.py | python3

echo "Setting up docker"
apt-get install --yes --no-install-recommends docker.io
usermod -aG docker ${GITHUB_RUNNER_USER}
chmod 666 /var/run/docker.sock
