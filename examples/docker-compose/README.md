This folder contains files and sub-folders that demonstrate how to run docker-stack notebook containers using Docker Compose on a Docker Machine-controlled host.

## Pre-requisites

* [Docker Engine](https://docs.docker.com/engine/) 1.10.0+
* [Docker Machine](https://docs.docker.com/machine/) 0.6.0+
* [Docker Compose](https://docs.docker.com/compose/) 1.6.0+

See the [installation instructions](https://docs.docker.com/engine/installation/) for your environment.

## Provision Docker machines

### Provision a VirtualBox VM on local desktop

```
bin/vbox.sh mymachine
```

### Provision a virtual device on IBM SoftLayer

```
export SOFTLAYER_USER=my_softlayer_username
export SOFTLAYER_API_KEY=my_softlayer_api_key
export SOFTLAYER_DOMAIN=my.domain

# Create virtual device
bin/softlayer.sh myhost

# Add DNS entry (SoftLayer DNS zone must exist for SOFTLAYER_DOMAIN)
bin/sl-dns.sh myhost
```

## Deploy stand-alone Jupyter Notebook

Build and run a `jupyter/minimal-notebook` container on an existing Docker machine.

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

See [notebook README](notebook/README.md) for more details.

## Let's Encrypt

If you want to secure access to publicly addressable notebook containers, you can generate a free certificate using the [Let's Encrypt](https://letsencrypt.org) service.

The following command creates a Docker volume, runs the `letsencrypt` client to create a full-chain certificate and private key, and stores them in the volume.  Note: The script uses several `letsencrypt` options, one of which automatically agrees to the Let's Encrypt Terms of Service.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com bin/letsencrypt.sh
```

Be aware that Let's Encrypt has a pretty [low rate limit per domain](https://community.letsencrypt.org/t/public-beta-rate-limits/4772/3) at the moment.  You can avoid exhausting your limit by testing against the Let's Encrypt staging servers.  To hit their staging servers, set the environment variable `CERT_SERVER=--staging`.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
  CERT_SERVER=--staging \
  bin/letsencrypt.sh
```

Also, be aware that Let's Encrypt certificates are short lived (90 days).  If you need them for a longer period of time, you'll need to manually setup a cron job to run the renewal steps. (You can reuse the command above.)

## Troubleshooting

### Unable to connect to VirtualBox VM on Mac OS X when using Cisco VPN client.

The Cisco VPN client blocks access to IP addresses that it does not know about, and may block access to a new VM if it is created while the Cisco VPN client is running.

1. Stop Cisco VPN client. (It does not allow modifications to route table).
2. Run `ifconfig` to list `vboxnet` virtual network devices.
3. Run `sudo route -nv add -net 192.168.99 -interface vboxnetX`, where X is the number of the virtual device assigned to the VirtualBox VM.
4. Start Cisco VPN client.
