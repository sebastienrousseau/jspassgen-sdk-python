<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Security Policy

## Supported versions

This package follows the [jspassgen](https://github.com/sebastienrousseau/jspassgen)
suite cadence. `0.0.24` is the latest release. While
pre-`1.0`, the latest released `0.0.x` receives security fixes; older
`0.0.x` versions do not.

| Version | Status | Receives security fixes? |
| :--- | :--- | :--- |
| `0.0.24` (latest) | Released 2026-11-21 | Yes |
| `0.0.23` | Released 2026-11-20 | No |
| `0.0.22` | Released 2026-11-18 | No |
| `main` | In development | Yes |

## Reporting a vulnerability

**Do not open a public issue for security reports.**

Use GitHub Private Vulnerability Reporting:
<https://github.com/sebastienrousseau/jspassgen-sdk-python/security/advisories/new>.
The maintainer is notified automatically. A vulnerability in the
JavaScript core belongs in
[jspassgen's advisories](https://github.com/sebastienrousseau/jspassgen/security/advisories/new).

Please include a description and its impact, a minimal reproducer
(preferably a failing test), the commit or version affected, and any
proposed fix. Never include a real password or secret.

These are goals, not guarantees: the project is maintained in a personal
capacity, with no SLA. **Acknowledgement**: the goal is within 5 working
days. **Triage**: a severity assessment and remediation plan after
acknowledgement.

## Security posture

### Scope

The package generates random values on the caller's machine. Today it
provides the random port and its `secrets` adapter; password and
passphrase generation are not implemented yet.

### Threat model

| Surface | How it is handled |
| :--- | :--- |
| **Weak randomness** | Every draw comes from `secrets` (the OS CSPRNG, through `os.urandom`). The library never imports `random`; a test enforces it. |
| **Modulo bias** | `random_int(max)` uses rejection sampling over `max - 1`'s bit length, so every value in `[0, max)` is equally likely. Tests check uniformity and the absence of modulo bias. |
| **Secrets leaving the machine** | No network call, no telemetry, no logging. A test fails if the library imports a networking module. |
| **Secrets in errors** | Error messages name the argument, never its value. `SecretsRandom` holds no state, and its `repr` shows none. |
| **Bad arguments** | A non-`int` (including `bool`) raises `TypeError`; a value below 1 raises `ValueError`. |

### Dependency audit

The package has no run-time dependencies. `make audit` runs pip-audit
over every locked development dependency in `uv.lock`; CI runs it on
every push. Dependabot proposes weekly updates of `uv.lock` and of the
pinned workflow actions.

### Release integrity

`release.yml` publishes each version from a signed annotated tag
(`git verify-tag v<version>` against `KEYS.asc`), after the `make check`
gate and `make audit`, through PyPI trusted publishing with no stored
token. The GitHub release carries the sdist, the wheel and `SHA256SUMS`.
