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
set +e
cp "/home/${SUDO_USER}/.ssh/authorized_keys" "/home/${GITHUB_RUNNER_USER}/.ssh/authorized_keys"
set -e
chown --recursive ${GITHUB_RUNNER_USER}:${GITHUB_RUNNER_USER} /home/${GITHUB_RUNNER_USER}/.ssh

echo "Setting up python3"
apt-get install --yes --no-install-recommends python3
curl -sS https://bootstrap.pypa.io/get-pip.py | python3

echo "Setting up docker"
apt-get remove --yes docker.io docker-doc docker-compose podman-docker containerd runc
apt-get update --yes
apt-get install --yes ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update --yes
apt-get install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

usermod -aG docker ${GITHUB_RUNNER_USER}
chmod 666 /var/run/docker.sock
