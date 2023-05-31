# Self-hosted runners

For building `aarch64` images, we use self-hosted GitHub runners.
It is recommended to have at least two runners to allow better parallelism.
Each runner is recommended to have at least _2 cores_ and _30 GB_ of disk space.

Add a new runner:

- To use [Oracle OCI](https://www.oracle.com/cloud/), create a compute instance `VM.Standard.A1.Flex` .
- To use [Google Cloud](https://cloud.google.com), use [this instruction](https://cloud.google.com/compute/docs/instances/create-arm-vm-instance#armpublicimage).

Configure your runner:

1. Run under `root`:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jupyter/docker-stacks/HEAD/aarch64-runner/setup.sh)"
   ```

   This will perform the initial runner setup and create a user `runner-user` without `sudo` capabilities.

2. Setup new GitHub Runner under `runner-user` using [GitHub Instructions](https://github.com/jupyter/docker-stacks/settings/actions/runners/new?arch=arm64&os=linux).
   **Do not `./run.sh` yet**.
3. Run under `root`:

   ```bash
   cd /home/runner-user/actions-runner/ && ./svc.sh install runner-user
   ```

4. Reboot the VM to apply all updates and run GitHub runner.
