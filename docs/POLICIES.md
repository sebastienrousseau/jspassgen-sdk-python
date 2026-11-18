<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Policies

## Toolchain

- **Python floor: 3.11.** CI tests every supported CPython from the floor
  to the newest (3.11, 3.12, 3.13, 3.14). The floor rises only when that
  version reaches its end of life, in a release whose changelog says so.
- **No run-time dependencies.** The package uses the standard library
  only.
- Development tools are locked in `uv.lock` and updated weekly by
  Dependabot.

## Versioning

Lockstep with the jspassgen suite, in `0.0.1` steps. Package 0.0.N will
pass the conformance kit of jspassgen 0.0.N once it vendors the kit,
which jspassgen has shipped since 0.0.21.

## Deprecation

A public name is deprecated for at least one release (with a
`DeprecationWarning` and a changelog entry) before it is removed.

## Supported versions

The latest release and `main`; see [SECURITY.md](https://github.com/sebastienrousseau/jspassgen-sdk-python/blob/main/SECURITY.md).
