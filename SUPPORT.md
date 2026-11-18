<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Getting support

## Read first

- [README.md](README.md): what exists today, install from a commit, and
  the limits of the package.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): the port and its
  adapter.
- [DEVELOPMENT.md](DEVELOPMENT.md): setup, testing and every CI gate.

## Supported versions

Nothing has been released yet. While pre-`1.0`, the latest released
`0.0.x` will be supported; older ones will not. The package follows the
jspassgen suite's version.

| Version | Status | Supported |
| :--- | :--- | :--- |
| `0.0.22` (next) | Unreleased | Not yet released |
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
