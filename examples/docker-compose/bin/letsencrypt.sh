#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Use https://letsencrypt.org to create a certificate for a single domain
# and store it in a Docker volume.

set -e

# Get domain and email from environment
[ -z "$FQDN" ] && \
	echo "ERROR: Must set FQDN environment varable" && \
  exit 1

[ -z "$EMAIL" ] && \
	echo "ERROR: Must set EMAIL environment varable" && \
  exit 1

# letsencrypt certificate server type (default is production).
# Set `CERT_SERVER=--staging` for staging.
: ${CERT_SERVER=''}

# Create Docker volume to contain the cert
: ${SECRETS_VOLUME:=my-notebook-secrets}
docker volume create --name $SECRETS_VOLUME 1>/dev/null
# Generate the cert and save it to the Docker volume
docker run --rm -it \
  -p 80:80 \
  -v $SECRETS_VOLUME:/etc/letsencrypt \
  quay.io/letsencrypt/letsencrypt:latest \
  certonly \
  --non-interactive \
  --keep-until-expiring \
  --standalone \
  --standalone-supported-challenges http-01 \
  --agree-tos \
  --domain "$FQDN" \
  --email "$EMAIL" \
  $CERT_SERVER

# Set permissions so nobody can read the cert and key.
# Also symlink the certs into the root of the /etc/letsencrypt
# directory so that the FQDN doesn't have to be known later.
docker run --rm -it \
  -v $SECRETS_VOLUME:/etc/letsencrypt \
  debian:jessie \
		bash -c "ln -s /etc/letsencrypt/live/$FQDN/* /etc/letsencrypt/ && \
			find /etc/letsencrypt -type d -exec chmod 755 {} +"
