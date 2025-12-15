# Opencv_from_source

Build and install **OpenCV (cv2) for Python 3** from source, targeting an **application virtualenv** (e.g., your Passenger venv), and optionally removing Ubuntu’s `python3-opencv` package.

This role exists to replace the `apt install python3-opencv` approach (which pulls in `libopencv-videoio…` and, transitively, FFmpeg runtime libraries like `libavcodec58`) with a controlled, source-built OpenCV installation.

## What this role does

1. Removes `python3-opencv` (apt) so OpenCV/FFmpeg dependency chains can be dropped.
2. Installs build toolchain + image codec build deps.
3. Ensures `numpy` exists in the target Python environment so headers are available.
4. Clones OpenCV source at a pinned tag.
5. Builds OpenCV and installs:
   - shared libs into `/usr/local` (by default)
   - Python `cv2` module into the target Python’s site-packages
6. Verifies `import cv2` works and the version matches `opencv_version`.

## Why we disable FFmpeg/Video I/O by default

For CDH Web, the stated requirement is: **“wagtail image feature detection”**. That generally needs core image processing, not video decoding.

Disabling `WITH_FFMPEG` and `BUILD_opencv_videoio` avoids dragging FFmpeg into the dependency tree via distro packages, and reduces attack surface.

---

## Requirements

- Ubuntu 22.04 (Jammy) or similar.
- Network access to `github.com/opencv/opencv` from the host during provisioning.
- A Python interpreter that you want the bindings installed into (usually a venv Python).

### Build dependencies installed by this role

- `build-essential`, `cmake`, `ninja-build`, `pkg-config`, `git`
- image codecs: `libjpeg-dev`, `libpng-dev`, `libtiff-dev`, `libwebp-dev`
- `python3-dev` (needed for compiling Python extensions)

---

## Role variables

### Core

| Variable | Default | Purpose |
|---|---:|---|
| `opencv_from_source_enabled` | `true` | Enable/disable the role |
| `opencv_replace_apt_package` | `true` | Remove distro `python3-opencv` before building |
| `opencv_version` | `"4.10.0"` | OpenCV git tag to build |
| `opencv_python_executable` | `"/usr/bin/python3"` | Python that should receive `cv2` |
| `opencv_install_prefix` | `"/usr/local"` | Where shared libs get installed |
| `opencv_src_dir` | `"/usr/local/src/opencv-{{ opencv_version }}"` | Source checkout root |
| `opencv_build_dir` | `"{{ opencv_src_dir }}/build"` | Build directory |

### Video / FFmpeg controls (important)

| Variable | Default | Meaning |
|---|---:|---|
| `opencv_with_ffmpeg` | `false` | CMake `WITH_FFMPEG` |
| `opencv_build_videoio` | `false` | CMake `BUILD_opencv_videoio` |
| `opencv_with_gstreamer` | `false` | CMake `WITH_GSTREAMER` |

### Optional build toggles

| Variable | Default |
|---|---:|
| `opencv_build_tests` | `false` |
| `opencv_build_examples` | `false` |

---

## Usage (CDH Web)

### 1) Stop installing `python3-opencv` via apt

In `inventory/group_vars/cdhweb/vars.yml` remove the package from `app_dependencies`:

```yaml
app_dependencies:
  # - python3-opencv  # remove this; replaced by source build

Then add role configuration (example):

```

```yaml
opencv_from_source_enabled: true
opencv_replace_apt_package: true

opencv_version: "4.10.0"
opencv_python_executable: "{{ passenger_python }}"

# keep these off unless you need video support
opencv_with_ffmpeg: false
opencv_build_videoio: false
opencv_with_gstreamer: false
```
