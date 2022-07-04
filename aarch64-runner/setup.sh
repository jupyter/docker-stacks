#!/bin/bash
set -ex

GITHUB_RUNNER_USER="runner-user"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

apt-get update --yes
apt-get upgrade --yes

echo "Setting up runner-user, who will run GitHub Actions runner"
adduser --disabled-password --gecos "" ${GITHUB_RUNNER_USER}
mkdir /home/${GITHUB_RUNNER_USER}/.ssh/
cp /home/ubuntu/.ssh/authorized_keys /home/${GITHUB_RUNNER_USER}/.ssh/authorized_keys
chown ${GITHUB_RUNNER_USER}:${GITHUB_RUNNER_USER} /home/${GITHUB_RUNNER_USER}/.ssh/authorized_keys

echo "Setting up python3"
apt-get install --yes --no-install-recommends python3
curl -sS https://bootstrap.pypa.io/get-pip.py | python3

echo "Setting up docker"
apt-get install --yes --no-install-recommends docker.io
usermod -aG docker ${GITHUB_RUNNER_USER}
chmod 666 /var/run/docker.sock
