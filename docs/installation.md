# Installation

Harmonize comes in two forms:

- **A headers-only CUDA/HIP C++ library**, in `harmonize/cpp`.
- **A Python package**, which builds GPU programs from Numba-compiled Python
  functions.

## 1. Install your GPU toolkit

Harmonize compiles code for your GPU, so it needs the compiler from your GPU's
manufacturer.

::::{tab-set}
:sync-group: gpu

:::{tab-item} NVIDIA
:sync: nvidia
Install the [CUDA Toolkit](https://docs.nvidia.com/cuda/cuda-quick-start-guide/index.html),
or just its `nvcc` compiler: from your system, an environment module
(`module load cuda`), or conda (`conda install -c nvidia cuda-nvcc`). Use a
version no newer than your driver supports (shown by `nvidia-smi`).
:::

:::{tab-item} AMD
:sync: amd
Install [ROCm](https://rocm.docs.amd.com/en/latest/), including `hipcc`,
`clang-offload-bundler`, `llvm-link`, and `llvm-as`.
:::
::::

The C++ library needs nothing else.

## 2. Install the Python package

Harmonize is published on PyPI as `harmonize-python` and imported as
`harmonize`. (The PyPI project named `harmonize` is unrelated.)

::::{tab-set}
:sync-group: gpu

:::{tab-item} NVIDIA
:sync: nvidia
Install the extra matching your CUDA toolkit's major version:

```sh
pip install "harmonize-python[cuda13]"   # or harmonize-python[cuda12]
```
:::

:::{tab-item} AMD
:sync: amd
Install AMD's Numba backend, `numba-hip`, built for your ROCm release, then
Harmonize. For ROCm 6.3.0 to 7.2.2, `numba-hip` comes from AMD's original
repository (here, for ROCm 7.2.1):

```sh
pip install --extra-index-url https://test.pypi.org/simple \
    "numba-hip[rocm-7-2-1] @ git+https://github.com/ROCm/numba-hip.git"
pip install harmonize-python
```

For newer ROCm releases, AMD publishes `numba-hip` on PyPI
(`pip install numba-hip`). `python -m harmonize check` prints the command for
the ROCm you have loaded.
:::
::::

To install from a clone of the repository instead, run `pip install ".[cuda13]"`
(or `pip install .` for AMD) in it; add `-e` to work on Harmonize itself.

## 3. Check your setup

```sh
python -m harmonize info    # detected platform, toolchain, and devices
python -m harmonize check   # problems that would stop GPU builds; exits non-zero if any
```

`check` reports, for example, a missing `nvcc`, a CUDA toolkit newer than the
driver, a toolkit too old for your GPU, or Numba emitting PTX newer than `nvcc`
can assemble. Include the output of `info` when reporting problems.

By default, Harmonize uses ROCm when `numba-hip` is installed and CUDA
otherwise. To require a platform, set `HARMONIZE_PLATFORM` to `cuda` or `rocm`.
