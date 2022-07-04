# Self-hosted runners

For `aarch64` images, we have self-hosted VMs, provided by [Oracle OCI](https://www.oracle.com/cloud/).

To setup a new runner:

1. Create a compute instance `VM.Standard.A1.Flex` with _1 OCPU_ and _6 GB_ using `Ubuntu 22.04` image.
2. Run under `root`:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/mathbunnyru/docker-stacks/asalikhov/new_build_system/aarch64-runner/setup.sh)"
   ```

   This will perform initial runner setup and create a non-root user `runner-user`.

3. Setup new GitHub Runner under `runner-user` using [GitHub Instructions](https://github.com/jupyter/docker-stacks/settings/actions/runners/new?arch=arm64&os=linux).
   Do not `./run.sh` yet.
4. Run under `root`:

   ```bash
   cd /home/runner-user/actions-runner/ && ./svc.sh install runner-user
   ```

5. Reboot VM to apply all updates and run GitHub runner.
