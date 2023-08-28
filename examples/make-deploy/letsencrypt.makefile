# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# BE CAREFUL when using Docker engine <1.10 because running a container with
# `--rm` option while mounting a docker volume may wipe out the volume.
# See issue: https://github.com/moby/moby/issues/17907

# Use letsencrypt production server by default to get a real cert.
# Use CERT_SERVER=--staging to hit the staging server (not a real cert).

letsencrypt: NAME?=notebook
letsencrypt: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt: TMP_CONTAINER?=$(NAME)-tmp
letsencrypt: CERT_SERVER?=
letsencrypt:
	@test -n "$(FQDN)" || \
		(echo "ERROR: FQDN not defined or blank"; exit 1)
	@test -n "$(EMAIL)" || \
		(echo "ERROR: EMAIL not defined or blank"; exit 1)
	@docker volume create --name $(SECRETS_VOLUME) > /dev/null
	@docker run -it -p 80:80 \
		--name=$(TMP_CONTAINER) \
		-v $(SECRETS_VOLUME):/etc/letsencrypt \
		quay.io/letsencrypt/letsencrypt:latest \
		certonly \
		$(CERT_SERVER) \
		--keep-until-expiring \
		--standalone \
		--standalone-supported-challenges http-01 \
		--agree-tos \
		--domain '$(FQDN)' \
		--email '$(EMAIL)'; \
		docker rm --force $(TMP_CONTAINER) > /dev/null
# The letsencrypt image has an entrypoint, so we use the notebook image
# instead so we can run arbitrary commands.
# Here we set the permissions so nobody can read the cert and key.
# We also symlink the certs into the root of the /etc/letsencrypt
# directory so that the FQDN doesn't have to be known later.
	@docker run -it \
		--name=$(TMP_CONTAINER) \
		-v $(SECRETS_VOLUME):/etc/letsencrypt \
		$(NOTEBOOK_IMAGE) \
		bash -c "ln -s /etc/letsencrypt/live/$(FQDN)/* /etc/letsencrypt/ && \
			find /etc/letsencrypt -type d -exec chmod 755 {} +"; \
			docker rm --force $(TMP_CONTAINER) > /dev/null

letsencrypt-notebook: PORT?=443
letsencrypt-notebook: NAME?=notebook
letsencrypt-notebook: WORK_VOLUME?=$(NAME)-data
letsencrypt-notebook: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt-notebook: DOCKER_ARGS:=-e USE_HTTPS=yes \
	-e PASSWORD=$(PASSWORD) \
	-v $(SECRETS_VOLUME):/etc/letsencrypt
letsencrypt-notebook: ARGS:=\
	--ServerApp.certfile=/etc/letsencrypt/fullchain.pem \
	--ServerApp.keyfile=/etc/letsencrypt/privkey.pem
letsencrypt-notebook: check
	@test -n "$(PASSWORD)" || \
		(echo "ERROR: PASSWORD not defined or blank"; exit 1)
	$(RUN_NOTEBOOK)
