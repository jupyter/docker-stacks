# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/minimal-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# PHP 7.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    php7.0 php7.0-cli php7.0-common php7.0-mbstring php7.0-gd php7.0-intl php7.0-xml php7.0-mysql php7.0-mcrypt php7.0-zip \
    php-pear php7.0-dev \
    pkg-config

# Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" &&\
    php -r "if (hash_file('SHA384', 'composer-setup.php') === '669656bab3166a7aff8a7506b8cb2d1c292f042046c5a994c43155c0be6190fa0355160742ab2e1c88d40d5be660b410') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" &&\
    php composer-setup.php &&\
    php -r "unlink('composer-setup.php');" &&\
    mv composer.phar /usr/local/bin/composer

# ZMQ
RUN echo "deb http://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/ ./" >> /etc/apt/sources.list && \
    wget https://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/Release.key -O- | sudo apt-key add && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libzmq3-dev

# ZMQ PHP binding
RUN sudo pecl install zmq-beta -v
RUN echo "extension=zmq.so" >> /etc/php/7.0/mods-available/zmq.ini  && \
    phpenmod zmq

# Jupyter PHP kernel
RUN cd /tmp && \
    wget https://litipk.github.io/Jupyter-PHP-Installer/dist/jupyter-php-installer.phar && \
    chmod +x jupyter-php-installer.phar && \
    ./jupyter-php-installer.phar install -vv

# clean
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*