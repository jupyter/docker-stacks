# Creating aarch64 self-hosted GitHub runner

For `aarch64` runners, we have self-hosted VMs, provided by [Oracle OCI](https://www.oracle.com/cloud/).

To setup new runner, please:

1. Create an Oracle `VM.Standard.A1.Flex` with `1 OCPU` and `4 GB` using `Ubuntu 22.04` image.
2. Run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/mathbunnyru/docker-stacks/asalikhov/new_build_system/aarch64-runner/setup.sh)"`
   This will perform initial runner setup and create a non-root user `runner-user`.
3. Setup new GitHub Runner with this user: <https://github.com/jupyter/docker-stacks/settings/actions/runners/new>
4. Run under `root` user in Runner directory: `./svc.sh install runner-user`
