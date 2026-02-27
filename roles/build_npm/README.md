# Build NPM

An Ansible role that installs a specific version of **Node.js** (including `npm` and `npx`) from prebuilt binaries. This role is architecture-aware, supporting both `x86_64` and `arm64` (Apple Silicon/Graviton), and is optimized for use within the Princeton University Library (PUL) infrastructure.

## Features

- **Version Management**: Ensures the specific version defined in `desired_nodejs_version` is installed.

- **Architecture Detection**: Automatically selects the correct binary for `x64` or `arm64` systems.

- **PUL Mirror Integration**: Defaults to the internal Princeton mirror for faster, more reliable downloads.

- **Clean Symlinking**: Links binaries to `/usr/local/bin/` for global accessibility.

- **Resilient Downloads**: Built-in retries and timeouts to handle intermittent network issues.

## Role Variables

The following variables are defined in `defaults/main.yml`:

| **Variable**              | **Default**            | **Description**                                    |
| ------------------------- | ---------------------- | -------------------------------------------------- |
| `desired_nodejs_version`  | `"22.4.0"`             | The version of Node.js to install.                 |
| `nodejs_install_method`   | `"prebuilt"`           | Method of installation (`prebuilt` or `source`).   |
| `nodejs_release_base_url` | `https://pulmirror...` | Base URL for fetching Node.js distributions.       |
| `nodejs_prefix_root`      | `/usr/local`           | The base directory where Node.js will be unpacked. |
| `nodejs_download_retries` | `6`                    | Number of retries for the download task.           |
| `nodejs_download_timeout` | `600`                  | Timeout in seconds for the download.               |

## Dependencies

None.

## Example Playbook

YAML

```text
- hosts: servers
  roles:
    - role: build_npm
      vars:
        desired_nodejs_version: "20.11.0"
```

## Architecture & Development (Molecule)

This role supports multi-arch development. When testing locally on **Apple Silicon (M1/M2/M3)** versus **GitHub Actions (amd64)**, Molecule handles the platform via environment variables.

### Local Testing (Apple Silicon)

To run molecule tests locally on an ARM-based Mac, use a local environment file to prevent architecture mismatches:

1. Create a `.env.local.yml` (this is ignored by git):

   YAML

   ```text
   ---
   MOLECULE_DOCKER_PLATFORM: linux/arm64
   ```

2. Run molecule:

   Bash

   ```text
   MOLECULE_ENV_FILE=.env.local.yml molecule test
   ```

> [!IMPORTANT]
>
> Do **not** commit `MOLECULE_DOCKER_PLATFORM` to the main `.env.yml` file, as this will break the GitHub Actions CI which requires `linux/amd64`.

## File Structure

- `tasks/main.yml`: Contains the logic for version normalization, binary downloading, and symlinking.

- `meta/main.yml`: Role metadata and platform support (Ubuntu Jammy).

- `molecule/`: Contains the Docker-based testing suite.

## License

MIT
