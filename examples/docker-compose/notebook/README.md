Run a docker-stack notebook container using Docker Compose on a Docker Machine-controlled host.

## Pre-requisites

* [Docker Engine](https://docs.docker.com/engine/) 1.10.0+
* [Docker Machine](https://docs.docker.com/machine/) 0.6.0+
* [Docker Compose](https://docs.docker.com/compose/) 1.6.0+

See the [installation instructions](https://docs.docker.com/engine/installation/) for your environment.

## Quickstart

Here's how to build and run a `jupyter/minimal-notebook` container on an existing Docker machine.

```
# activate docker machine
eval "$(docker-machine env mymachine)"

# build notebook image on the machine
notebook/build.sh

# bring up notebook container
notebook/up.sh
```

To stop and remove the container:

```
notebook/down.sh
```

## FAQ

### Can I run multiple notebook containers on the same VM?

Yes. Set environment variables to specify unique names and ports when running the `up.sh` command.

```
NAME=my-notebook PORT=9000 notebook/up.sh
NAME=your-notebook PORT=9001 notebook/up.sh
```

To stop and remove the containers:

```
NAME=my-notebook notebook/down.sh
NAME=your-notebook notebook/down.sh
```

### Where are my notebooks stored?

The `up.sh` creates a Docker volume named after the notebook container with a `-work` suffix, e.g., `my-notebook-work`.


### Can multiple notebook containers share the same notebook volume?

Yes. Set the `WORK_VOLUME` environment variable to the same value for each notebook.

```
NAME=my-notebook PORT=9000 WORK_VOLUME=our-work notebook/up.sh
NAME=your-notebook PORT=9001 WORK_VOLUME=our-work notebook/up.sh
```

### How do I run over HTTPS?

To run the notebook server with a self-signed certificate, pass the `--secure` option to the `up.sh` script.  You must also provide a password, which will be used to secure the notebook server.  You can specify the password by setting the `PASSWORD` environment variable, or by passing it to the `up.sh` script.  

```
PASSWORD=a_secret notebook/up.sh --secure

# or
notebook/up.sh --secure --password a_secret
```

To use a real certificate from Let's Encrypt, first run the `bin/letsencrypt.sh` script to create the certificate chain and store it in a Docker volume.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com bin/letsencrypt.sh
```

The following command will store the certificate chain in a Docker volume named `mydomain-secrets`.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
  SECRETS_VOLUME=mydomain-secrets \
  bin/letsencrypt.sh
```

Now run `up.sh` with the `--letsencrypt` option.  You must also provide the name of the secrets volume and a password.

```
PASSWORD=a_secret SECRETS_VOLUME=mydomain-secrets notebook/up.sh --letsencrypt

# or
notebook/up.sh --letsencrypt --password a_secret --secrets mydomain-secrets
```
