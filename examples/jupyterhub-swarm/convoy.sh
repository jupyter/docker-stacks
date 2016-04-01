#!/bin/bash

cd /tmp && \
  curl -L https://github.com/rancher/convoy/releases/download/v0.5.0.2-rancher/convoy.tar.gz | tar xzv && \
  cp convoy/convoy convoy/convoy-pdata_tools /usr/local/bin/ && \
  rm -rf ./convoy && \
  cd -

mkdir -p /etc/docker/plugins/

echo "unix:///var/run/convoy/convoy.sock" > /etc/docker/plugins/convoy.spec

cat << EOF > /etc/default/convoy
CONVOY_OPTS="--drivers vfs --driver-opts vfs.path=/mnt/nfs"
EOF
