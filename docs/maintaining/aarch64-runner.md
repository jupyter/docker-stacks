# Self-hosted runners

For building `aarch64` images, we use VMs, provided by [Oracle OCI](https://www.oracle.com/cloud/).
Currently, there are 2 self-hosted GitHub runners with _2 OCPU_ and _12 GB_ each.

To setup a new runner:

1. Create a compute instance `VM.Standard.A1.Flex` with _2 OCPU_ and _12 GB_ using `Ubuntu 22.04` image.
2. Run under `root`:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jupyter/docker-stacks/HEAD/aarch64-runner/setup.sh)"
   ```

   This will perform initial runner setup and create a user `runner-user` without `sudo` capabilities.

3. Setup new GitHub Runner under `runner-user` using [GitHub Instructions](https://github.com/jupyter/docker-stacks/settings/actions/runners/new?arch=arm64&os=linux).
   Do not `./run.sh` yet.
4. Run under `root`:

   ```bash
   cd /home/runner-user/actions-runner/ && ./svc.sh install runner-user
   ```

5. Reboot VM to apply all updates and run GitHub runner.
