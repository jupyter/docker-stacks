#!/bin/bash

apt-get update && apt-get install -y nfs-common

mkdir -p /mnt/nfs

mount -t nfs4 -o hard,intr \
  $NFS_SERVER \
  /mnt/nfs
