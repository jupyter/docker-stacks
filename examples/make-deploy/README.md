# Make deploy example

This folder contains a Makefile and a set of supporting files demonstrating how to run a docker-stack notebook container on a docker-machine controlled host.

## Prerequisites

- make 3.81+
  - Ubuntu users: Be aware of [make 3.81 defect 483086](https://bugs.launchpad.net/ubuntu/+source/make-dfsg/+bug/483086) which exists in 14.04 LTS but is fixed in 15.04+
- docker-machine 0.5.0+
- docker 1.9.0+

## Quickstart

To show what's possible, here's how to run the `jupyter/minimal-notebook` on a brand-new local virtualbox.

```bash
# create a new VM
make virtualbox-vm NAME=dev
# make the new VM the active docker machine
eval $(docker-machine env dev)
# pull a docker stack and build a local image from it
make image
# start a Server in a container
make notebook
```

The last command will log the IP address and port to visit in your browser.

## FAQ

### Can I run multiple notebook containers on the same VM?

Yes. Specify a unique name and port on the `make notebook` command.

```bash
make notebook NAME=my-notebook PORT=9000
make notebook NAME=your-notebook PORT=9001
```

### Can multiple notebook containers share their notebook directory?

Yes.

```bash
make notebook NAME=my-notebook PORT=9000 WORK_VOLUME=our-work
make notebook NAME=your-notebook PORT=9001 WORK_VOLUME=our-work
```

### How do I run over HTTPS?

Instead of `make notebook`, run `make self-signed-notebook PASSWORD=your_desired_password`.
This target gives you a notebook with a self-signed certificate.

### That self-signed certificate is a pain. Let's Encrypt?

Yes. Please.

```bash
make letsencrypt FQDN=host.mydomain.com EMAIL=myemail@somewhere.com
make letsencrypt-notebook
```

The first command creates a Docker volume named after the notebook container with a `-secrets` suffix.
It then runs the `letsencrypt` client with a slew of options (one of which has you automatically agreeing to the Let's Encrypt Terms of Service, see the Makefile).
The second command mounts the secrets volume and configures Jupyter to use the full-chain certificate and private key.

Be aware: Let's Encrypt has a pretty [low rate limit per domain](https://community.letsencrypt.org/t/public-beta-rate-limits/4772/3) at the moment.
You can avoid exhausting your limit by testing against the Let's Encrypt staging servers.
To hit their staging servers, set the environment variable `CERT_SERVER=--staging`.

```bash
make letsencrypt FQDN=host.mydomain.com EMAIL=myemail@somewhere.com CERT_SERVER=--staging
```

Also, keep in mind Let's Encrypt certificates are short-lived: 90 days at the moment.
You'll need to manually set up a cron job to run the renewal steps at the moment.
(You can reuse the first command above.)

### My pip/conda/apt-get installs disappear every time I restart the container. Can I make them permanent?

```bash
# add your pip, conda, apt-get, etc. permanent features to the Dockerfile where
# indicated by the comments in the Dockerfile
vi Dockerfile
make image
make notebook
```

### How do I upgrade my Docker container?

```bash
make image DOCKER_ARGS=--pull
make notebook
```

The first line pulls the latest version of the Docker image used in the local Dockerfile.
Then it rebuilds the local Docker image containing any customizations you may have added to it.
The second line kills your currently running notebook container, and starts a fresh one using the new image.

### Can I run on another VM provider other than VirtualBox?

Yes. As an example, there's a `softlayer.makefile` included in this repo as an example.
You would use it like so:

```bash
make softlayer-vm NAME=myhost \
    SOFTLAYER_DOMAIN=your_desired_domain \
    SOFTLAYER_USER=your_user_id \
    SOFTLAYER_API_KEY=your_api_key
eval $(docker-machine env myhost)
# optional, creates a real DNS entry for the VM using the machine name as the hostname
make softlayer-dns SOFTLAYER_DOMAIN=your_desired_domain
make image
make notebook
```

If you'd like to add support for another docker-machine driver, use the `softlayer.makefile` as a template.

### Where are my notebooks stored?

`make notebook` creates a Docker volume named after the notebook container with a `-data` suffix.

### Uh ... make?

Yes, sorry Windows users. It got the job done for a simple example.
We can certainly accept other deployment mechanism examples in the parent folder or in other repos.

### Are there any other options?

Yes indeed. `cat` the Makefiles and look at the target parameters.
