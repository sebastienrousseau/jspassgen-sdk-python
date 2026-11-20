<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Getting support

## Read first

- [README.md](README.md): what exists today, install from PyPI, and
  the limits of the package.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): the port and its
  adapter.
- [DEVELOPMENT.md](DEVELOPMENT.md): setup, testing and every CI gate.

## Supported versions

`0.0.22` is the latest release. While pre-`1.0`, the latest released
`0.0.x` is supported; older ones are not. The package follows the
jspassgen suite's version.

| Version | Status | Supported |
| :--- | :--- | :--- |
| `0.0.23` (next) | Unreleased, in development | Yes |
| `0.0.22` (latest) | Released 2026-11-18 | Yes |
| `main` | In development | Yes |

## Questions and bugs

Open an [issue](https://github.com/sebastienrousseau/jspassgen-sdk-python/issues/new/choose).
For a bug, include the package version or commit, your Python version
and platform, and a minimal reproducer. Never include a real password or
secret.

A behaviour that comes from the JavaScript core (a generator rule, an
entropy figure, an error code) belongs in
[jspassgen's issues](https://github.com/sebastienrousseau/jspassgen/issues).

## Security

Never report a vulnerability in a public issue; follow
[SECURITY.md](SECURITY.md).

## Response times

The project is maintained in a personal capacity, with no SLA. The goal
is a first answer within a few working days.
