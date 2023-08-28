# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import pathlib
import time

import pytest  # type: ignore

from tests.conftest import TrackedContainer

LOGGER = logging.getLogger(__name__)


def test_uid_change(container: TrackedContainer) -> None:
    """Container should change the UID of the default user."""
    logs = container.run_and_wait(
        timeout=120,  # usermod is slow so give it some time
        tty=True,
        user="root",
        environment=["NB_UID=1010"],
        command=["start.sh", "bash", "-c", "id && touch /opt/conda/test-file"],
    )
    assert "uid=1010(jovyan)" in logs


def test_gid_change(container: TrackedContainer) -> None:
    """Container should change the GID of the default user."""
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        user="root",
        environment=["NB_GID=110"],
        command=["start.sh", "id"],
    )
    assert "gid=110(jovyan)" in logs
    assert "groups=110(jovyan),100(users)" in logs


def test_nb_user_change(container: TrackedContainer) -> None:
    """Container should change the username (`NB_USER`) of the default user."""
    nb_user = "nayvoj"
    running_container = container.run_detached(
        tty=True,
        user="root",
        environment=[f"NB_USER={nb_user}", "CHOWN_HOME=yes"],
        command=["start.sh", "bash", "-c", "sleep infinity"],
    )

    # Give the chown time to complete.
    # Use sleep, not wait, because the container sleeps forever.
    time.sleep(1)
    LOGGER.info(f"Checking if the user is changed to {nb_user} by the start script ...")
    output = running_container.logs().decode("utf-8")
    assert "ERROR" not in output
    assert "WARNING" not in output
    assert (
        f"username: jovyan       -> {nb_user}" in output
    ), f"User is not changed to {nb_user}"

    LOGGER.info(f"Checking {nb_user} id ...")
    command = "id"
    expected_output = f"uid=1000({nb_user}) gid=100(users) groups=100(users)"
    cmd = running_container.exec_run(command, user=nb_user, workdir=f"/home/{nb_user}")
    output = cmd.output.decode("utf-8").strip("\n")
    assert output == expected_output, f"Bad user {output}, expected {expected_output}"

    LOGGER.info(f"Checking if {nb_user} owns his home folder ...")
    command = f'stat -c "%U %G" /home/{nb_user}/'
    expected_output = f"{nb_user} users"
    cmd = running_container.exec_run(command, workdir=f"/home/{nb_user}")
    output = cmd.output.decode("utf-8").strip("\n")
    assert (
        output == expected_output
    ), f"Bad owner for the {nb_user} home folder {output}, expected {expected_output}"

    LOGGER.info(
        f"Checking if home folder of {nb_user} contains the 'work' folder with appropriate permissions ..."
    )
    command = f'stat -c "%F %U %G" /home/{nb_user}/work'
    expected_output = f"directory {nb_user} users"
    cmd = running_container.exec_run(command, workdir=f"/home/{nb_user}")
    output = cmd.output.decode("utf-8").strip("\n")
    assert (
        output == expected_output
    ), f"Folder work was not copied properly to {nb_user} home folder. stat: {output}, expected {expected_output}"


def test_chown_extra(container: TrackedContainer) -> None:
    """Container should change the UID/GID of a comma separated
    CHOWN_EXTRA list of folders."""
    logs = container.run_and_wait(
        timeout=120,  # chown is slow so give it some time
        tty=True,
        user="root",
        environment=[
            "NB_UID=1010",
            "NB_GID=101",
            "CHOWN_EXTRA=/home/jovyan,/opt/conda/bin",
            "CHOWN_EXTRA_OPTS=-R",
        ],
        command=[
            "start.sh",
            "bash",
            "-c",
            "stat -c '%n:%u:%g' /home/jovyan/.bashrc /opt/conda/bin/jupyter",
        ],
    )
    assert "/home/jovyan/.bashrc:1010:101" in logs
    assert "/opt/conda/bin/jupyter:1010:101" in logs


def test_chown_home(container: TrackedContainer) -> None:
    """Container should change the NB_USER home directory owner and
    group to the current value of NB_UID and NB_GID."""
    logs = container.run_and_wait(
        timeout=120,  # chown is slow so give it some time
        tty=True,
        user="root",
        environment=[
            "CHOWN_HOME=yes",
            "CHOWN_HOME_OPTS=-R",
            "NB_USER=kitten",
            "NB_UID=1010",
            "NB_GID=101",
        ],
        command=["start.sh", "bash", "-c", "stat -c '%n:%u:%g' /home/kitten/.bashrc"],
    )
    assert "/home/kitten/.bashrc:1010:101" in logs


def test_sudo(container: TrackedContainer) -> None:
    """Container should grant passwordless sudo to the default user."""
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        user="root",
        environment=["GRANT_SUDO=yes"],
        command=["start.sh", "sudo", "id"],
    )
    assert "uid=0(root)" in logs


def test_sudo_path(container: TrackedContainer) -> None:
    """Container should include /opt/conda/bin in the sudo secure_path."""
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        user="root",
        environment=["GRANT_SUDO=yes"],
        command=["start.sh", "sudo", "which", "jupyter"],
    )
    assert logs.rstrip().endswith("/opt/conda/bin/jupyter")


def test_sudo_path_without_grant(container: TrackedContainer) -> None:
    """Container should include /opt/conda/bin in the sudo secure_path."""
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        user="root",
        command=["start.sh", "which", "jupyter"],
    )
    assert logs.rstrip().endswith("/opt/conda/bin/jupyter")


def test_group_add(container: TrackedContainer) -> None:
    """Container should run with the specified uid, gid, and secondary
    group. It won't be possible to modify /etc/passwd since gid is nonzero, so
    additionally verify that setting gid=0 is suggested in a warning.
    """
    logs = container.run_and_wait(
        timeout=5,
        no_warnings=False,
        user="1010:1010",
        group_add=["users"],  # Ensures write access to /home/jovyan
        command=["start.sh", "id"],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == 1
    assert "Try setting gid=0" in warnings[0]
    assert "uid=1010 gid=1010 groups=1010,100(users)" in logs


def test_set_uid(container: TrackedContainer) -> None:
    """Container should run with the specified uid and NB_USER.
    The /home/jovyan directory will not be writable since it's owned by 1000:users.
    Additionally verify that "--group-add=users" is suggested in a warning to restore
    write access.
    """
    logs = container.run_and_wait(
        timeout=5,
        no_warnings=False,
        user="1010",
        command=["start.sh", "id"],
    )
    assert "uid=1010(jovyan) gid=0(root)" in logs
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == 1
    assert "--group-add=users" in warnings[0]


def test_set_uid_and_nb_user(container: TrackedContainer) -> None:
    """Container should run with the specified uid and NB_USER."""
    logs = container.run_and_wait(
        timeout=5,
        no_warnings=False,
        user="1010",
        environment=["NB_USER=kitten"],
        group_add=["users"],  # Ensures write access to /home/jovyan
        command=["start.sh", "id"],
    )
    assert "uid=1010(kitten) gid=0(root)" in logs
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == 1
    assert "user is kitten but home is /home/jovyan" in warnings[0]


def test_container_not_delete_bind_mount(
    container: TrackedContainer, tmp_path: pathlib.Path
) -> None:
    """Container should not delete host system files when using the (docker)
    -v bind mount flag and mapping to /home/jovyan.
    """
    d = tmp_path / "data"
    d.mkdir()
    p = d / "foo.txt"
    p.write_text("some-content")

    container.run_and_wait(
        timeout=5,
        tty=True,
        user="root",
        working_dir="/home/",
        environment=[
            "NB_USER=user",
            "CHOWN_HOME=yes",
        ],
        volumes={d: {"bind": "/home/jovyan/data", "mode": "rw"}},
        command=["start.sh", "ls"],
    )
    assert p.read_text() == "some-content"
    assert len(list(tmp_path.iterdir())) == 1


@pytest.mark.parametrize("enable_root", [False, True])
def test_jupyter_env_vars_to_unset(
    container: TrackedContainer, enable_root: bool
) -> None:
    """Environment variables names listed in JUPYTER_ENV_VARS_TO_UNSET
    should be unset in the final environment."""
    root_args = {"user": "root"} if enable_root else {}
    logs = container.run_and_wait(
        timeout=10,
        tty=True,
        environment=[
            "JUPYTER_ENV_VARS_TO_UNSET=SECRET_ANIMAL,UNUSED_ENV,SECRET_FRUIT",
            "FRUIT=bananas",
            "SECRET_ANIMAL=cats",
            "SECRET_FRUIT=mango",
        ],
        command=[
            "start.sh",
            "bash",
            "-c",
            "echo I like $FRUIT and ${SECRET_FRUIT:-stuff}, and love ${SECRET_ANIMAL:-to keep secrets}!",
        ],
        **root_args,  # type: ignore
    )
    assert "I like bananas and stuff, and love to keep secrets!" in logs


def test_secure_path(container: TrackedContainer, tmp_path: pathlib.Path) -> None:
    """Make sure that the sudo command has conda's python (not system's) on path.
    See <https://github.com/jupyter/docker-stacks/issues/1053>.
    """
    d = tmp_path / "data"
    d.mkdir()
    p = d / "wrong_python.sh"
    p.write_text('#!/bin/bash\necho "Wrong python executable invoked!"')
    p.chmod(0o755)

    logs = container.run_and_wait(
        timeout=5,
        tty=True,
        user="root",
        volumes={p: {"bind": "/usr/bin/python", "mode": "ro"}},
        command=["start.sh", "python", "--version"],
    )
    assert "Wrong python" not in logs
    assert "Python" in logs
