# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

letsencrypt: NAME?=notebook
letsencrypt: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt:
	@test -n "$(FQDN)" || \
		(echo "ERROR: FQDN not defined or blank"; exit 1)
	@test -n "$(EMAIL)" || \
		(echo "ERROR: EMAIL not defined or blank"; exit 1)
	@docker volume create --name $(SECRETS_VOLUME) > /dev/null
# Specifying an alternative cert path doesn't work with the --duplicate
# setting which we want to use for renewal.
	@docker run -it --rm -p 80:80 \
		-v $(SECRETS_VOLUME):/etc/letsencrypt \
		quay.io/letsencrypt/letsencrypt:latest \
		certonly \
		--standalone \
		--standalone-supported-challenges http-01 \
		--agree-tos \
		--duplicate \
		--domain '$(FQDN)' \
		--email '$(EMAIL)'
# The lets encrypt image has an entrypoint so we use the notebook image
# instead which we know uses tini as the entry and can run arbitrary commands.
# Here we need to set the permissions so nobody in the proxy container can read
# the cert and key. Plus we want to symlink the certs into the root of the 
# /etc/letsencrypt directory so that the FQDN doesn't have to be known later.
	@docker run -it --rm \
		-v $(SECRETS_VOLUME):/etc/letsencrypt \
		$(NOTEBOOK_IMAGE) \
		bash -c "ln -s /etc/letsencrypt/live/$(FQDN)/* /etc/letsencrypt/ && \
			find /etc/letsencrypt -type d -exec chmod 755 {} +"

letsencrypt-notebook: PORT?=443
letsencrypt-notebook: NAME?=notebook
letsencrypt-notebook: WORK_VOLUME?=$(NAME)-data
letsencrypt-notebook: SECRETS_VOLUME?=$(NAME)-secrets
letsencrypt-notebook: DOCKER_ARGS:=-e USE_HTTPS=yes \
	-e PASSWORD=$(PASSWORD) \
	-v $(SECRETS_VOLUME):/etc/letsencrypt
letsencrypt-notebook: ARGS:=\
	--NotebookApp.certfile=/etc/letsencrypt/fullchain.pem \
	--NotebookApp.keyfile=/etc/letsencrypt/privkey.pem
letsencrypt-notebook: check
	@test -n "$(PASSWORD)" || \
		(echo "ERROR: PASSWORD not defined or blank"; exit 1)
	$(RUN_NOTEBOOK)
