FROM ubuntu:14.04

# Setting the language and encoding won't work without this tweak.
# See bug here ( https://bugs.launchpad.net/ubuntu/+bug/920601 ).
RUN DEBIAN_FRONTEND=noninteractive locale-gen en_US.UTF-8 && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
