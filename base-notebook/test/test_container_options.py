# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import time

import pytest


def test_cli_args(container, http_client):
    """Container should respect notebook server command line args
    (e.g., disabling token security)"""
    container.run(
        command=['start-notebook.sh', '--NotebookApp.token=""']
    )
    resp = http_client.get('http://localhost:8888')
    resp.raise_for_status()
    assert 'login_submit' not in resp.text


@pytest.mark.filterwarnings('ignore:Unverified HTTPS request')
def test_unsigned_ssl(container, http_client):
    """Container should generate a self-signed SSL certificate
    and notebook server should use it to enable HTTPS.
    """
    c = container.run(
        environment=['GEN_CERT=yes']
    )
    # NOTE: The requests.Session backing the http_client fixture  does not retry
    # properly while the server is booting up. An SSL handshake error seems to
    # abort the retry logic. Forcing a long sleep for the moment until I have
    # time to dig more.
    time.sleep(5)
    resp = http_client.get('https://localhost:8888', verify=False)
    resp.raise_for_status()
    assert 'login_submit' in resp.text


@pytest.mark.skip('placeholder')
def test_uid_change():
    pass


@pytest.mark.skip('placeholder')
def test_gid_change():
    pass


@pytest.mark.skip('placeholder')
def test_group_add():
    pass


@pytest.mark.skip('placeholder')
def test_sudo():
    pass


@pytest.mark.skip('placeholder')
def test_host_mount():
    pass


@pytest.mark.skip('placeholder')
def test_alt_command():
    pass

