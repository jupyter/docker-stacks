# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import pathlib

import pytest  # type: ignore

from tests.utils.tracked_container import TrackedContainer

LOGGER = logging.getLogger(__name__)

DEFAULT_HOME_ENTRIES = [".bash_logout", ".bashrc", ".profile"]
DATA_DIR = pathlib.Path(__file__).parent.resolve() / "data" / "populate"
ROOTLESS_TRIPLET_ENV = ["NB_USER=root", "NB_UID=0", "NB_GID=0"]


@pytest.fixture
def host_home(tmp_path: pathlib.Path) -> pathlib.Path:
    """An empty host directory to be mounted as the home directory,
    writable by any container user."""
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    home_dir.chmod(0o777)
    return home_dir


@pytest.mark.parametrize("nb_user", ["jovyan", "kitten"])
def test_populate_mounted_home(
    container: TrackedContainer, host_home: pathlib.Path, nb_user: str
) -> None:
    """Files created during the build should be restored to an empty mounted
    home directory and owned by the (possibly renamed) default user."""
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=[f"NB_USER={nb_user}"],
        volumes={host_home: {"bind": f"/home/{nb_user}", "mode": "rw"}},
        command=[
            "stat",
            "-c",
            "%n %U %G",
            *[f"/home/{nb_user}/{entry}" for entry in DEFAULT_HOME_ENTRIES],
        ],
    )
    for entry in DEFAULT_HOME_ENTRIES:
        assert f"Populating missing /home/{nb_user}/{entry}" in logs
        assert f"/home/{nb_user}/{entry} {nb_user} users" in logs


def test_populate_mounted_home_as_non_root(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """The default files should also be restored when the container runs as
    a non-root user able to write to the mounted home directory."""
    logs = container.run_and_wait(
        timeout=10,
        volumes={host_home: {"bind": "/home/jovyan", "mode": "rw"}},
        command=[
            "stat",
            "-c",
            "%n %U",
            "/home/jovyan/.bashrc",
            "/home/jovyan/.profile",
        ],
    )
    assert "Populating missing /home/jovyan/.profile" in logs
    assert "/home/jovyan/.bashrc jovyan" in logs
    assert "/home/jovyan/.profile jovyan" in logs


def test_populate_keeps_existing_files(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """Files existing in the mounted home directory should never be
    overwritten, and only the missing ones should be restored."""
    custom_bashrc = "# my-custom-bashrc\n"
    (host_home / ".bashrc").write_text(custom_bashrc)
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        volumes={host_home: {"bind": "/home/jovyan", "mode": "rw"}},
        command=["cat", "/home/jovyan/.bashrc"],
    )
    assert "Skipping /home/jovyan/.bashrc, it already exists" in logs
    assert "Populating missing /home/jovyan/.profile" in logs
    assert "my-custom-bashrc" in logs
    assert (host_home / ".bashrc").read_text() == custom_bashrc
    assert (host_home / ".profile").exists()


def test_populate_skipped_without_write_access(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """A non-root user without write access to the mounted home directory
    should only get a warning, and nothing should be restored."""
    # This test needs to have tty disabled, the reason is explained here:
    # https://github.com/jupyter/docker-stacks/pull/2260#discussion_r2008821257
    logs = container.run_and_wait(
        timeout=10,
        no_warnings=False,
        user="1010",
        tty=False,
        volumes={host_home: {"bind": "/home/jovyan", "mode": "ro"}},
        command=["ls", "-A", "/home/jovyan"],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == 1
    assert "No write access" in warnings[0]
    assert "Populating" not in logs
    assert not list(host_home.iterdir())


def test_populate_custom_uid_gid_ownership(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """The restored files should be owned by NB_UID:NB_GID
    even without CHOWN_HOME set."""
    logs = container.run_and_wait(
        timeout=120,  # user/group modification is slow so give it some time
        user="root",
        environment=["NB_UID=1010", "NB_GID=110"],
        volumes={host_home: {"bind": "/home/jovyan", "mode": "rw"}},
        command=[
            "stat",
            "-c",
            "%n %u %g",
            "/home/jovyan/.bashrc",
            "/home/jovyan/.profile",
        ],
    )
    assert "/home/jovyan/.bashrc 1010 110" in logs
    assert "/home/jovyan/.profile 1010 110" in logs


def test_populate_with_chown_home(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """CHOWN_HOME should also change the ownership of the mounted home
    directory itself, populated with the restored files."""
    logs = container.run_and_wait(
        timeout=120,  # user/group modification and chown are slow so give them some time
        user="root",
        environment=[
            "NB_USER=kitten",
            "NB_UID=1010",
            "NB_GID=101",
            "CHOWN_HOME=yes",
            "CHOWN_HOME_OPTS=-R",
        ],
        volumes={host_home: {"bind": "/home/kitten", "mode": "rw"}},
        command=["stat", "-c", "%n %u %g", "/home/kitten", "/home/kitten/.bashrc"],
    )
    assert "/home/kitten 1010 101" in logs
    assert "/home/kitten/.bashrc 1010 101" in logs


def test_populate_rootless_triplet(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """The restored files should be owned by root for the triplet
    NB_USER=root, NB_UID=0, NB_GID=0."""
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOTLESS_TRIPLET_ENV,
        volumes={host_home: {"bind": "/home/root", "mode": "rw"}},
        command=[
            "stat",
            "-c",
            "%n %U %G",
            "/home/root/.bashrc",
            "/home/root/.profile",
        ],
    )
    assert "/home/root/.bashrc root root" in logs
    assert "/home/root/.profile root root" in logs


def test_populate_new_home_when_old_home_mounted_empty(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """The new NB_USER home directory, created as a copy of the empty mounted
    /home/jovyan directory, should be populated as well."""
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=["NB_USER=kitten"],
        volumes={host_home: {"bind": "/home/jovyan", "mode": "rw"}},
        command=["stat", "-c", "%n %U %G", "/home/kitten/.bashrc"],
    )
    assert "Populating missing /home/kitten/.bashrc" in logs
    assert "/home/kitten/.bashrc kitten users" in logs
    # The empty mounted directory is left as is
    assert not list(host_home.iterdir())


def test_populate_home_when_subfolder_mounted(
    container: TrackedContainer, tmp_path: pathlib.Path
) -> None:
    """When only a subfolder of the new NB_USER home directory is mounted,
    docker auto-creates the home directory,
    and the missing files should be restored to it."""
    host_data = tmp_path / "data"
    host_data.mkdir()
    host_data.chmod(0o777)
    (host_data / "keep.txt").write_text("some-content")
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=["NB_USER=kitten"],
        volumes={host_data: {"bind": "/home/kitten/data", "mode": "rw"}},
        command=[
            "bash",
            "-c",
            "cat /home/kitten/data/keep.txt && stat -c '%n %U %G' /home/kitten/.bashrc",
        ],
    )
    assert "Populating missing /home/kitten/.bashrc" in logs
    assert "/home/kitten/.bashrc kitten users" in logs
    assert "some-content" in logs
    assert (host_data / "keep.txt").read_text() == "some-content"


def test_populate_hook_ordering(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """Files created by start-notebook.d hooks should be kept,
    and before-notebook.d hooks should see the restored files."""
    seed_bashrc = DATA_DIR / "seed-bashrc.sh"
    check_profile = DATA_DIR / "check-profile.sh"
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        volumes={
            host_home: {"bind": "/home/jovyan", "mode": "rw"},
            seed_bashrc: {
                "bind": "/usr/local/bin/start-notebook.d/10-seed-bashrc.sh",
                "mode": "ro",
            },
            check_profile: {
                "bind": "/usr/local/bin/before-notebook.d/10-check-profile.sh",
                "mode": "ro",
            },
        },
        command=["cat", "/home/jovyan/.bashrc"],
    )
    assert "Skipping /home/jovyan/.bashrc, it already exists" in logs
    assert "seeded-by-hook" in logs
    assert "HOOK_SEES_PROFILE" in logs
    assert "HOOK_MISSES_PROFILE" not in logs


def test_populate_script_restores_missing_files(container: TrackedContainer) -> None:
    """populate-home-dir.sh should restore all the backed up files
    to an empty target directory."""
    logs = container.run_and_wait(
        timeout=10,
        command=["bash", "-c", "mkdir /tmp/target && populate-home-dir.sh /tmp/target"],
    )
    for entry in DEFAULT_HOME_ENTRIES:
        assert f"Populating missing /tmp/target/{entry}" in logs


def test_populate_script_skips_existing_entries(container: TrackedContainer) -> None:
    """populate-home-dir.sh should not touch the entries that already exist
    in the target directory, even dangling symlinks."""
    command = (
        "mkdir /tmp/target && "
        "touch /tmp/target/.profile && "
        "ln -s /does-not-exist /tmp/target/.bashrc && "
        "populate-home-dir.sh /tmp/target"
    )
    logs = container.run_and_wait(timeout=10, command=["bash", "-c", command])
    assert "Skipping /tmp/target/.profile, it already exists" in logs
    assert "Skipping /tmp/target/.bashrc, it already exists" in logs
    assert "Populating missing /tmp/target/.bash_logout" in logs


def test_populate_script_chowns_restored_files(container: TrackedContainer) -> None:
    """populate-home-dir.sh should change the owner of the restored files
    to the one provided in the second argument."""
    command = (
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target 1010:110 && "
        "stat -c '%n %u %g' /tmp/target/.bashrc /tmp/target/.profile"
    )
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOTLESS_TRIPLET_ENV,
        command=["bash", "-c", command],
    )
    assert "/tmp/target/.bashrc 1010 110" in logs
    assert "/tmp/target/.profile 1010 110" in logs


def test_populate_script_restores_directories_and_symlinks(
    container: TrackedContainer,
) -> None:
    """The extension point for derived images: directories added to the backup
    should be restored recursively, keeping the setgid bit and the given owner,
    and symlinks should be restored and chowned as symlinks, without being followed."""
    command = (
        "mkdir /opt/default-home/custom && "
        "echo nested > /opt/default-home/custom/nested.txt && "
        "chmod 2750 /opt/default-home/custom && "
        "ln -s .bashrc /opt/default-home/.zshrc && "
        "ln -s /etc/hostname /opt/default-home/.outside && "
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target 1010:110 && "
        "stat -c '%n %u %g %a' /tmp/target/custom /tmp/target/custom/nested.txt && "
        "stat -c '%n %u %g %F' /tmp/target/.zshrc && "
        'echo "LINK_TARGET=$(readlink /tmp/target/.zshrc)" && '
        "stat -c '%n %u' /etc/hostname"
    )
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOTLESS_TRIPLET_ENV,
        command=["bash", "-c", command],
    )
    assert "/tmp/target/custom 1010 110 2750" in logs
    assert "/tmp/target/custom/nested.txt 1010 110 644" in logs
    assert "/tmp/target/.zshrc 1010 110 symbolic link" in logs
    assert "LINK_TARGET=.bashrc" in logs
    # The file the restored symlink points to is not chowned
    assert "/etc/hostname 0" in logs


def test_populate_script_does_not_follow_symlinks(container: TrackedContainer) -> None:
    """An existing symlink in the target directory should be skipped,
    and the file it points to should not be modified or chowned."""
    command = (
        "mkdir /tmp/target && "
        "ln -s /etc/hostname /tmp/target/.bashrc && "
        "populate-home-dir.sh /tmp/target 1010:110 && "
        "stat -c '%n %F %u' /etc/hostname && "
        "stat -c '%n %F' /tmp/target/.bashrc"
    )
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOTLESS_TRIPLET_ENV,
        command=["bash", "-c", command],
    )
    assert "Skipping /tmp/target/.bashrc, it already exists" in logs
    assert "Populating missing /tmp/target/.profile" in logs
    assert "/etc/hostname regular file 0" in logs
    assert "/tmp/target/.bashrc symbolic link" in logs


def test_populate_script_created_target_reported_as_skip(
    container: TrackedContainer,
) -> None:
    """When cp fails, but the target entry exists (created concurrently
    or left by a partial copy), populate-home-dir.sh should report a skip
    instead of warning, leaving the cp error visible."""
    make_backup_dir_unreadable = (
        "mkdir /opt/default-home/secret && "
        "touch /opt/default-home/secret/hidden && "
        "chmod 700 /opt/default-home/secret"
    )
    command = (
        f"sudo bash -c '{make_backup_dir_unreadable}' && "
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target && "
        "stat -c '%n %F' /tmp/target/secret"
    )
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=["GRANT_SUDO=yes"],
        command=["bash", "-c", command],
    )
    assert "Skipping /tmp/target/secret, it appeared concurrently" in logs
    assert "Permission denied" in logs
    assert "/tmp/target/secret directory" in logs


def test_populate_script_idempotent(container: TrackedContainer) -> None:
    """Re-running populate-home-dir.sh should only skip the restored files,
    never re-copying them."""
    command = (
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target && "
        "populate-home-dir.sh /tmp/target"
    )
    logs = container.run_and_wait(timeout=10, command=["bash", "-c", command])
    assert logs.count("Populating missing /tmp/target/") == len(DEFAULT_HOME_ENTRIES)
    assert logs.count("Skipping /tmp/target/") == len(DEFAULT_HOME_ENTRIES)


def test_populate_script_chown_failure_is_not_fatal(
    container: TrackedContainer,
) -> None:
    """When the files are copied, but changing their owner fails,
    populate-home-dir.sh should keep the files and only warn."""
    command = (
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target 1010:110 && "
        "stat -c '%n exists' "
        + " ".join(f"/tmp/target/{entry}" for entry in DEFAULT_HOME_ENTRIES)
    )
    logs = container.run_and_wait(
        timeout=10,
        no_warnings=False,
        command=["bash", "-c", command],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == len(DEFAULT_HOME_ENTRIES)
    assert all(
        "Failed to change the owner of /tmp/target/" in warning for warning in warnings
    )
    for entry in DEFAULT_HOME_ENTRIES:
        assert f"/tmp/target/{entry} exists" in logs


def test_populate_root_skipped_without_write_access(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """Even as root, nothing should be restored to a home directory mounted
    without write access (e.g. read-only), and a warning should be given."""
    logs = container.run_and_wait(
        timeout=10,
        no_warnings=False,
        user="root",
        volumes={host_home: {"bind": "/home/jovyan", "mode": "ro"}},
        command=["ls", "-A", "/home/jovyan"],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == 1
    assert "No write access to /home/jovyan" in warnings[0]
    assert "Populating" not in logs
    assert not list(host_home.iterdir())


def test_populate_script_no_backup_dir(container: TrackedContainer) -> None:
    """populate-home-dir.sh should recognize a removed backup directory
    as an opt-out and do nothing, only reporting it."""
    command = (
        "rm -rf /opt/default-home && "
        "mkdir /tmp/target && "
        "populate-home-dir.sh /tmp/target"
    )
    logs = container.run_and_wait(
        timeout=10,
        user="root",
        environment=ROOTLESS_TRIPLET_ENV,
        command=["bash", "-c", command],
    )
    assert "Backup directory /opt/default-home doesn't exist" in logs
    assert "Populating missing /tmp/target" not in logs


def test_populate_script_usage_error(container: TrackedContainer) -> None:
    """populate-home-dir.sh called without arguments should fail
    with an error showing the usage."""
    logs = container.run_and_wait(
        timeout=10,
        no_errors=False,
        command=["bash", "-c", "populate-home-dir.sh || echo POPULATE_FAILED"],
    )
    errors = TrackedContainer.get_errors(logs)
    assert len(errors) == 1
    assert "Usage: populate-home-dir.sh <target_home> [<owner>]" in errors[0]
    assert "POPULATE_FAILED" in logs


def test_populate_script_failure_is_not_fatal(container: TrackedContainer) -> None:
    """populate-home-dir.sh should only warn when it fails to restore files,
    because it is run during startup, which it should never prevent."""
    command = (
        "mkdir /tmp/target && "
        "chmod a-w /tmp/target && "
        "populate-home-dir.sh /tmp/target && "
        "echo POPULATE_DID_NOT_FAIL"
    )
    logs = container.run_and_wait(
        timeout=10,
        no_warnings=False,
        command=["bash", "-c", command],
    )
    warnings = TrackedContainer.get_warnings(logs)
    assert len(warnings) == len(DEFAULT_HOME_ENTRIES)
    assert all("Failed to populate /tmp/target/" in warning for warning in warnings)
    assert "POPULATE_DID_NOT_FAIL" in logs


def test_populate_restores_terminal_colors(
    container: TrackedContainer, host_home: pathlib.Path
) -> None:
    """The restored .bashrc should enable the colored prompt and keep conda
    activation working, so mounting an empty home directory doesn't lose them.
    https://github.com/jupyter/docker-stacks/issues/815"""
    logs = container.run_and_wait(
        timeout=10,
        volumes={host_home: {"bind": "/home/jovyan", "mode": "rw"}},
        command=["bash", "-i", "-c", "echo PROMPT=${PS1@Q} && which python"],
    )
    # The colored prompt is enabled by the force_color_prompt=yes setting
    assert r"\[\033[01;32m\]\u@\h\[\033[00m\]" in logs
    # The conda environment is activated by the conda hook in .bashrc
    assert "/opt/conda/bin/python" in logs
