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
    container.run(
        environment=['GEN_CERT=yes']
    )
    # NOTE: The requests.Session backing the http_client fixture does not retry
    # properly while the server is booting up. An SSL handshake error seems to
    # abort the retry logic. Forcing a long sleep for the moment until I have
    # time to dig more.
    time.sleep(5)
    resp = http_client.get('https://localhost:8888', verify=False)
    resp.raise_for_status()
    assert 'login_submit' in resp.text


def test_uid_change(container):
    """Container should change the UID of the default user."""
    c = container.run(
        tty=True,
        user='root',
        environment=['NB_UID=1010'],
        command=['start.sh', 'bash', '-c', 'id && touch /opt/conda/test-file']
    )
    # usermod is slow so give it some time
    c.wait(timeout=120)
    assert 'uid=1010(jovyan)' in c.logs(stdout=True).decode('utf-8')


def test_gid_change(container):
    """Container should change the GID of the default user."""
    c = container.run(
        tty=True,
        user='root',
        environment=['NB_GID=110'],
        command=['start.sh', 'id']
    )
    c.wait(timeout=10)
    logs = c.logs(stdout=True).decode('utf-8')
    assert 'gid=110(jovyan)' in logs
    assert 'groups=110(jovyan),100(users)' in logs


def test_sudo(container):
    """Container should grant passwordless sudo to the default user."""
    c = container.run(
        tty=True,
        user='root',
        environment=['GRANT_SUDO=yes'],
        command=['start.sh', 'sudo', 'id']
    )
    rv = c.wait(timeout=10)
    assert rv == 0 or rv["StatusCode"] == 0
    assert 'uid=0(root)' in c.logs(stdout=True).decode('utf-8')


def test_sudo_path(container):
    """Container should include /opt/conda/bin in the sudo secure_path."""
    c = container.run(
        tty=True,
        user='root',
        environment=['GRANT_SUDO=yes'],
        command=['start.sh', 'sudo', 'which', 'jupyter']
    )
    rv = c.wait(timeout=10)
    assert rv == 0 or rv["StatusCode"] == 0
    assert c.logs(stdout=True).decode('utf-8').rstrip().endswith('/opt/conda/bin/jupyter')


def test_sudo_path_without_grant(container):
    """Container should include /opt/conda/bin in the sudo secure_path."""
    c = container.run(
        tty=True,
        user='root',
        command=['start.sh', 'which', 'jupyter']
    )
    rv = c.wait(timeout=10)
    assert rv == 0 or rv["StatusCode"] == 0
    assert c.logs(stdout=True).decode('utf-8').rstrip().endswith('/opt/conda/bin/jupyter')


def test_group_add(container, tmpdir):
    """Container should run with the specified uid, gid, and secondary
    group.
    """
    c = container.run(
        user='1010:1010',
        group_add=['users'],
        command=['start.sh', 'id']
    )
    rv = c.wait(timeout=5)
    assert rv == 0 or rv["StatusCode"] == 0
    assert 'uid=1010 gid=1010 groups=1010,100(users)' in c.logs(stdout=True).decode('utf-8')
