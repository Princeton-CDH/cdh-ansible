# Nodejs

Installs a pinned Node.js runtime and optionally runs npm dependency
installation and webpack asset builds for CDH applications.

## What this role does

- Installs Node.js from the Princeton mirror using the upstream prebuilt
  Linux tarball.
- Symlinks `node`, `npm`, `npx`, and `corepack` into `/usr/local/bin`.
- Optionally enables Yarn Berry through Corepack.
- Optionally installs npm dependencies for an application release path.
- Optionally runs the application's webpack build.
- Validates the webpack stats file when the application uses
  `webpack-bundle-tracker`.
- Provides clearer diagnostics when webpack prerequisites, build output,
  or stats files are missing.

## Task files

The role is organized into task files so playbooks can run only the
pieces they need.

-----------------------------------------------------------------------

  Task file Purpose

  ----------------------------------- -----------------------------------

  `tasks/install.yml` Install and verify Node.js, npm,
                                      npx, corepack, and optional Yarn
                                      Berry

  `tasks/npm.yml` Run npm dependency installation for
                                      an application path

  `tasks/webpack.yml` Run the webpack build and validate
                                      the stats file

  `tasks/main.yml`                    Expected to include the install
                                      task and conditionally include npm

## and webpack tasks

-----------------------------------------------------------------------

Expected `tasks/main.yml` wiring:

    ---
    - name: Nodejs | Install Node.js
      ansible.builtin.import_tasks: install.yml

    - name: Nodejs | Install npm dependencies
      ansible.builtin.import_tasks: npm.yml
      when: nodejs_npm_enabled | bool

    - name: Nodejs | Build webpack assets
      ansible.builtin.import_tasks: webpack.yml
      when: nodejs_webpack_enabled | bool

## Basic usage

Install Node.js only:

    - name: Install Node.js
      ansible.builtin.include_role:
        name: nodejs

Install Node.js and run npm install:

    - name: Install Node.js and npm dependencies
      ansible.builtin.include_role:
        name: nodejs
      vars:
        nodejs_npm_enabled: true
        nodejs_npm_install_path: /srv/www/myapp/current
        nodejs_npm_install_mode: production
        nodejs_build_user: deploy

Install Node.js, run npm install, and build webpack assets:

    - name: Install Node.js and build assets
      ansible.builtin.include_role:
        name: nodejs
      vars:
        nodejs_npm_enabled: true
        nodejs_webpack_enabled: true
        nodejs_npm_install_path: /srv/www/myapp/current
        nodejs_npm_install_mode: production
        nodejs_build_user: deploy
        runtime_env: staging

## Important variables

### Node.js installation

-----------------------------------------------------------------------

  Variable                    Default Description

  --------------------------- ---------------------------------------------------- -----------------------

  `nodejs_version`            `{{ desired_nodejs_version | default('22.4.0') }}`   Node.js version to
                                                                                   install. Accepts either
                                                                                   `22.4.0` or `v22.4.0`.

  `nodejs_install_method` `prebuilt` Installation method.
                                                                                   Currently supports
                                                                                   prebuilt tarball
                                                                                   installs.

  `nodejs_release_base_url` `https://pulmirror.princeton.edu/mirror/nodejs` Base URL for Node.js
                                                                                   release downloads.

  `nodejs_prefix_root`        `/usr/local` Parent directory where
                                                                                   Node.js is unpacked.

  `nodejs_remove_apt_node`    `true` Removes distro-packaged
                                                                                   `nodejs` to avoid PATH

## conflicts

-----------------------------------------------------------------------

### Yarn

-----------------------------------------------------------------------

  Variable                Default Description

  ----------------------- ----------------------- -----------------------

  `nodejs_yarn_enabled` `false` Enable Yarn Berry
                                                  through Corepack.

  `nodejs_yarn_version` `4.15.0`                Yarn version to
                                                  activate through

## Corepack

-----------------------------------------------------------------------

### npm install

-----------------------------------------------------------------------

  Variable                    Default                                                        Description

  --------------------------- -------------------------------------------------------------- -----------------------

  `nodejs_npm_enabled`        `false`                                                        Whether to run
                                                                                             `tasks/npm.yml`.

  `nodejs_npm_install_path`   `{{ npm_install_path | default(deploy | default('')) }}`       Application path
                                                                                             containing
                                                                                             `package.json`.

  `nodejs_npm_install_mode`   `{{ npm_install_mode | default('production') }}`               npm install mode.
                                                                                             Supports `production`,
                                                                                             `ci`, and `dev`.

  `nodejs_build_user`         `{{ deploy_user | default(django_user | default('root')) }}`   User that runs npm and

## webpack commands

-----------------------------------------------------------------------

Install modes:

-----------------------------------------------------------------------

  Mode                                Behavior

  ----------------------------------- -----------------------------------

  `production`                        Runs `npm install --production`

  `ci`                                Runs `npm ci`; requires
                                      `package-lock.json`

  `dev` Runs `npm install` with development

## dependencies

-----------------------------------------------------------------------

## Webpack

Enable webpack with:

    nodejs_webpack_enabled: true

Webpack builds are selected by `runtime_env` through
`nodejs_webpack_build_commands`.

Default mapping:

    nodejs_webpack_build_commands:
      staging: "{{ webpack_build_qa | default('build:qa') }}"
      production: "{{ webpack_build_prod | default('build:prod') }}"
      preproduction: "{{ webpack_build_prod | default('build:prod') }}"

For an application with different npm scripts, override the mapping in
inventory or group vars:

    nodejs_webpack_build_commands:
      staging: build:staging
      production: build
      preproduction: build

The webpack task runs:

    npm run <mapped command>

from `nodejs_npm_install_path`.

## Webpack stats file convention

By default, the role expects webpack to write:

    nodejs_webpack_stats_default: "{{ nodejs_npm_install_path }}/sitemedia/webpack-stats.json"

This matches the common `webpack-bundle-tracker` convention used by
Django applications.

Applications that write the stats file somewhere else should set:

    nodejs_webpack_stats_file: /srv/www/myapp/current/path/to/webpack-stats.json

Applications that do not use `webpack-bundle-tracker` should disable the
stats check:

    nodejs_webpack_stats_check: false

When stats checking is enabled, the role verifies that the file exists,
is not empty, and parses as JSON.

## Debugging webpack builds

Enable verbose webpack diagnostics with:

    nodejs_webpack_debug: true

On failure, the webpack task reports:

- the failed task name
- the npm command that was run
- the expected stats file path
- npm stdout
- npm stderr
- candidate stats files found under `nodejs_npm_install_path`

If the build succeeds but the expected stats file is missing, either set
`nodejs_webpack_stats_file` to the actual path or set
`nodejs_webpack_stats_check: false` for applications that do not produce
a stats file.

## Molecule

The default Molecule scenario verifies the full Node.js + npm + webpack
workflow.

The scenario:

- installs Node.js `22.4.0`
- creates a fixture application in `/opt/fixture`
- writes a minimal `package.json`
- installs webpack dependencies
- runs the `build:qa` npm script
- verifies that `/opt/fixture/sitemedia/webpack-stats.json` exists, is
  non-empty, and parses as JSON

Run:

    cd roles/nodejs
    molecule test

For local Apple Silicon testing, use an untracked local env file instead
of committing platform overrides:

    ---
    MOLECULE_DOCKER_PLATFORM: linux/arm64

Then run:

    cd roles/nodejs
    MOLECULE_ENV_FILE=.env.local.yml molecule test

CI should control its own platform, usually `linux/amd64`.

## Migration notes

Playbooks that previously used `build_npm` and `run_webpack` should
migrate to `nodejs`.

Before:

    - role: build_npm
    - role: run_webpack

After:

    - role: nodejs
      vars:
        nodejs_npm_enabled: true
        nodejs_webpack_enabled: true
        nodejs_npm_install_path: /srv/www/myapp/current
        nodejs_build_user: deploy
        runtime_env: "{{ runtime_env }}"

Applications with non-standard stats paths must set
`nodejs_webpack_stats_file`.

Applications without webpack stats output must set:

    nodejs_webpack_stats_check: false

## Legacy variable compatibility

The role currently honors several legacy variables to make migration
easier:

-----------------------------------------------------------------------

  Legacy variable New variable

  ----------------------------------- --------------------------------------------

  `desired_nodejs_version`            `nodejs_version`

  `npm_install_path` `nodejs_npm_install_path`

  `npm_install_mode` `nodejs_npm_install_mode`

  `deploy_user` / `django_user` `nodejs_build_user`

  `webpack_build_qa` `nodejs_webpack_build_commands.staging`

## `webpack_build_prod`                `nodejs_webpack_build_commands.production`

-----------------------------------------------------------------------

Prefer the `nodejs_*` variables for new configuration.

## Requirements

- Ubuntu Jammy or compatible Linux host
- `community.general.npm`
- `community.docker` for Molecule Docker scenarios
- npm dependencies available from the configured package registry
- Node.js tarballs available from `nodejs_release_base_url`
