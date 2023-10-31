# Docker Compose example

This example demonstrate how to deploy docker-stack notebook containers to any Docker Machine-controlled host using Docker Compose.

## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/) 1.10.0+
- [Docker Machine](https://docs.docker.com/machine/) 0.6.0+
- [Docker Compose](https://docs.docker.com/compose/) 1.6.0+

See the [installation instructions](https://docs.docker.com/engine/installation/) for your environment.

## Quickstart

Build and run a `jupyter/minimal-notebook` container on a VirtualBox VM on local desktop.

```bash
# create a Docker Machine-controlled VirtualBox VM
bin/vbox.sh mymachine

# activate the docker machine
eval "$(docker-machine env mymachine)"

# build the notebook image on the machine
notebook/build.sh

# bring up the notebook container
notebook/up.sh
```

To stop and remove the container:

```bash
notebook/down.sh
```

## FAQ

### How do I specify which docker-stack notebook image to deploy?

You can customize the docker-stack notebook image to deploy by modifying the `notebook/Dockerfile`.
For example, you can build and deploy a `jupyter/all-spark-notebook` by modifying the Dockerfile like so:

```dockerfile
FROM quay.io/jupyter/all-spark-notebook
# Your RUN commands and so on
```

Once you modify the Dockerfile, don't forget to rebuild the image.

```bash
# activate the docker machine
eval "$(docker-machine env mymachine)"

notebook/build.sh
```

### Can I run multiple notebook containers on the same VM?

Yes. Set environment variables to specify unique names and ports when running the `up.sh` command.

```bash
NAME=my-notebook PORT=9000 notebook/up.sh
NAME=your-notebook PORT=9001 notebook/up.sh
```

To stop and remove the containers:

```bash
NAME=my-notebook notebook/down.sh
NAME=your-notebook notebook/down.sh
```

### Where are my notebooks stored?

The `up.sh` creates a Docker volume named after the notebook container with a `-work` suffix, e.g., `my-notebook-work`.

### Can multiple notebook containers share the same notebook volume?

Yes. Set the `WORK_VOLUME` environment variable to the same value for each notebook.

```bash
NAME=my-notebook PORT=9000 WORK_VOLUME=our-work notebook/up.sh
NAME=your-notebook PORT=9001 WORK_VOLUME=our-work notebook/up.sh
```

### How do I run over HTTPS?

To run the Jupyter Server with a self-signed certificate, pass the `--secure` option to the `up.sh` script.
You must also provide a password, which will be used to secure the Jupyter Server.
You can specify the password by setting the `PASSWORD` environment variable, or by passing it to the `up.sh` script.

```bash
PASSWORD=a_secret notebook/up.sh --secure

# or
notebook/up.sh --secure --password a_secret
```

### Can I use Let's Encrypt certificate chains?

Sure. If you want to secure access to publicly addressable notebook containers, you can generate a free certificate using the [Let's Encrypt](https://letsencrypt.org) service.

This example includes the `bin/letsencrypt.sh` script, which runs the `letsencrypt` client to create a full-chain certificate and private key, and stores them in a Docker volume.

```{note}
The script hard codes several `letsencrypt` options, one of which automatically agrees to the Let's Encrypt Terms of Service.
```

The following command will create a certificate chain and store it in a Docker volume named `mydomain-secrets`.

```bash
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
    SECRETS_VOLUME=mydomain-secrets \
    bin/letsencrypt.sh
```

Now run `up.sh` with the `--letsencrypt` option.
You must also provide the name of the secrets volume and a password.

```bash
PASSWORD=a_secret SECRETS_VOLUME=mydomain-secrets notebook/up.sh --letsencrypt

# or
notebook/up.sh --letsencrypt --password a_secret --secrets mydomain-secrets
```

Be aware that Let's Encrypt has a pretty [low rate limit per domain](https://community.letsencrypt.org/t/public-beta-rate-limits/4772/3) at the moment.
You can avoid exhausting your limit by testing against the Let's Encrypt staging servers.
To hit their staging servers, set the environment variable `CERT_SERVER=--staging`.

```bash
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
    CERT_SERVER=--staging \
    bin/letsencrypt.sh
```

Also, be aware that Let's Encrypt certificates are short-lived (90 days).
If you need them for a longer period of time, you'll need to manually set up a cron job to run the renewal steps.
(You can reuse the command above.)

### Can I deploy to any Docker Machine host?

Yes, you should be able to deploy to any Docker Machine-controlled host.
To make it easier to get up and running, this example includes scripts to provision Docker Machines to VirtualBox and IBM SoftLayer, but more scripts are welcome!

To create a Docker machine using a VirtualBox VM on local desktop:

```bash
bin/vbox.sh mymachine
```

To create a Docker machine using a virtual device on IBM SoftLayer:

```bash
export SOFTLAYER_USER=my_softlayer_username
export SOFTLAYER_API_KEY=my_softlayer_api_key
export SOFTLAYER_DOMAIN=my.domain

# Create virtual device
bin/softlayer.sh myhost

# Add DNS entry (SoftLayer DNS zone must exist for SOFTLAYER_DOMAIN)
bin/sl-dns.sh myhost
```

## Troubleshooting

### Unable to connect to VirtualBox VM on Mac OS X when using Cisco VPN client

The Cisco VPN client blocks access to IP addresses that it does not know about, and may block access to a new VM if it is created while the Cisco VPN client is running.

1. Stop Cisco VPN client. (It does not allow modifications to route table).
2. Run `ifconfig` to list `vboxnet` virtual network devices.
3. Run `sudo route -nv add -net 192.168.99 -interface vboxnetX`, where X is the number of the virtual device assigned to the VirtualBox VM.
4. Start Cisco VPN client.
