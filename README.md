<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

<p align="center">
  <img src="https://raw.githubusercontent.com/sebastienrousseau/jspassgen/main/.github/assets/logo.svg" alt="jspassgen logo" width="128" />
</p>

<h1 align="center">jspassgen for Python</h1>

<p align="center">
  A native Python port of the jspassgen password and passphrase core, drawing only from the operating system's CSPRNG through the secrets module. In development: this version ships the random port and nothing else yet.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/actions"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/jspassgen-sdk-python/ci.yml?style=for-the-badge&logo=github" alt="Build" height="28" /></a>
  <a href="#install"><img src="https://img.shields.io/badge/PyPI-not%20published-lightgrey?style=for-the-badge&color=fc8d62&logo=pypi&logoColor=white" alt="PyPI: not published yet" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/tree/main/docs"><img src="https://img.shields.io/badge/docs-manual-blue?style=for-the-badge&labelColor=555555&logo=readthedocs" alt="Docs" height="28" /></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/jspassgen-sdk-python"><img src="https://img.shields.io/ossf-scorecard/github.com/sebastienrousseau/jspassgen-sdk-python?style=for-the-badge&label=OpenSSF%20Scorecard&logo=openssf" alt="OpenSSF Scorecard" height="28" /></a>
  <a href="LICENSE-APACHE"><img src="https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg?style=for-the-badge" alt="License: Apache-2.0 OR MIT" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/blob/main/docs/POLICIES.md"><img src="https://img.shields.io/badge/Python-3.11%2B-3776ab.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11 or newer" height="28" /></a>
</p>

<p align="center">
  <em>No demo yet: there is nothing to show until the generators are ported. The demo will record real generated passwords, not a mock-up.</em>
</p>

---

## Contents

**Getting started**

- [Install](#install): from a commit with pip; not on PyPI yet
- [Requirements](#requirements): Python floor, platforms
- [Quick Start](#quick-start): draw unbiased integers and bytes from the CSPRNG

**The jspassgen ecosystem**

- [The jspassgen ecosystem](#the-jspassgen-ecosystem): the core, the tools and the native SDKs, one version

**Library reference**

- [Capabilities at a glance](#capabilities-at-a-glance): what exists today and what is planned
- [Ecosystem comparison](#ecosystem-comparison): not written yet, and why
- [Benchmarks](#benchmarks): none yet, and why
- [Features](#features): module-level capability list
- [Configuration](#configuration): injecting a random port
- [Examples](#examples): none yet, and why

**Operational**

- [When not to use jspassgen](#when-not-to-use-jspassgen): limitations
- [Development](#development): make targets, CI
- [Security](#security): guarantees and reporting
- [Documentation](#documentation): all reference docs
- [Stability guarantees](#stability-guarantees): version axis, deprecations, toolchain discipline
- [License](#license)

---

## Install

### As a Python library

Nothing is published yet. The suite plan names `jspassgen` as this
package's PyPI name, but no release has been uploaded, so
`pip install jspassgen` does not install this code. Until the first
release, install from a commit:

```sh
pip install "git+https://github.com/sebastienrousseau/jspassgen-sdk-python@<commit>"
python -c 'import jspassgen; print(jspassgen.__version__)'
```

The distribution and the import package are both `jspassgen`. It has no
run-time dependencies, is typed (PEP 561, `py.typed`) and is checked with
`mypy --strict`.

---

## Requirements

- Python 3.11 or newer ([toolchain policy](docs/POLICIES.md)). CI tests
  3.11, 3.12, 3.13 and 3.14 on Ubuntu 24.04.
- Pure Python, standard library only. Randomness comes from `secrets`,
  which reads the operating system's CSPRNG through `os.urandom`.

---

## Quick Start

```python
from jspassgen import SecretsRandom

rng = SecretsRandom()
print(rng.random_int(6) + 1)  # a fair die roll, 1 to 6
print(rng.random_bytes(16).hex())  # 16 bytes from the OS CSPRNG
```

`random_int(max)` returns an integer in `[0, max)` with every value
equally likely: it draws the bit length of `max - 1` and rejects any draw
of `max` or more, rather than reducing raw bytes modulo `max`, which would
favour the low values. Both methods refuse an argument below 1 with
`ValueError` and anything that is not an `int` (including `bool`) with
`TypeError`.

This is the random port the generators will be built on, not a password
generator yet.

---

## The jspassgen ecosystem

jspassgen is one suite in lockstep: every member releases the same
version, as decided in
[jspassgen ADR 0001](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/adr/0001-ecosystem-lockstep.md).
The SDKs are native ports of the JavaScript core, not network clients: a
password is made on the user's machine and never leaves it. The member
list lives in [`docs/ecosystem.json`](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/ecosystem.json)
in the core repository.

| Component | Purpose | Use case |
| :--- | :--- | :--- |
| [`jspassgen`][core] | The zero-dependency core, Node.js library, web UI and workers; the source of the planned conformance kit | JavaScript and the reference behaviour |
| **`jspassgen-sdk-python`** | This repository: the native Python port (planned member, nothing released) | Python applications and scripts |
| `jspassgen-sdk-rust`, `-java`, `-dotnet`, `-cpp` | Native ports to Rust, Java, .NET and C++ (planned) | Other languages, same output |
| `jspassgen-cli`, `-mcp`, `-lsp` | Command line, MCP server and language server on the core (planned) | Terminals, AI agents, editors |
| [jspassgen.com][site] | The product site | Evaluating the suite |

---

## Capabilities at a glance

| Area | Capability | Status |
| :--- | :--- | :--- |
| Randomness | `RandomGeneratorPort`: `random_bytes(n)`, `random_int(max)` | On this branch (0.0.22, unreleased) |
| Randomness | `SecretsRandom`: the port on `secrets`, unbiased `random_int` | On this branch (0.0.22, unreleased) |
| Generators | The password and passphrase types of the core | Planned, after the conformance kit |
| Entropy | Entropy calculation and validation with the core's error codes | Planned, after the conformance kit |
| Wordlist | The EFF diceware list, byte-identical to the core's | Planned, after the conformance kit |
| Conformance | Draw tapes replayed through the port, checked in CI | Planned: the kit does not exist yet |

---

## Ecosystem comparison

Not written yet. A comparison with other Python password generators
means comparing generators, and this package has none yet; it will be
written, with evidence, once the generators pass the conformance kit.

---

## Benchmarks

None yet. There is no generator to measure, and timing a thin wrapper
around `secrets` would say nothing about the port. Benchmarks arrive with
the generators.

---

## Features

- **`jspassgen.ports.RandomGeneratorPort`**: a runtime-checkable
  `typing.Protocol` with `random_bytes(n) -> bytes` and
  `random_int(max) -> int`, the Python form of the core's
  `RandomGeneratorPort` (`generateRandomBytes`, `generateRandomInt`).
- **`jspassgen.adapters.SecretsRandom`**: the port on `secrets`;
  stateless and safe to share between threads.
- **`jspassgen.__version__`**: the installed version, read from the
  package metadata.

---

## Configuration

There is nothing to configure yet. Code that needs randomness takes a
`RandomGeneratorPort`, so a test can pass a deterministic implementation
in place of `SecretsRandom`; the conformance kit will use this to replay
recorded draws. Never pass a non-cryptographic source when generating a
real secret.

---

## Examples

None yet. The only public surface is the random port, and the Quick
Start above covers it; runnable examples arrive with the generators.

---

## When not to use jspassgen

- **You need passwords today.** This version generates no passwords or
  passphrases. Use the JavaScript [`jspassgen`][core], or `secrets`
  directly (`secrets.token_urlsafe`, `secrets.choice`).
- **You need it from PyPI.** Nothing is published yet.
- **You need byte-for-byte agreement with the JavaScript core.** That is
  the goal, proven by the conformance kit, which does not exist yet.
- **You need a seeded, reproducible generator.** `SecretsRandom` cannot
  be seeded by design; a deterministic port is for tests only.

---

## Development

```sh
mise install   # Python 3.14, uv 0.13.1, Node 24 (mise.toml)
make check     # versions, ruff, mypy --strict, complexity, 100% coverage
```

`make check` is the gate CI runs: the version restatements, ruff (lint
and format), `mypy --strict`, the complexity ceilings (cyclomatic 10,
cognitive 15, Halstead difficulty 30, 60 lines per function, 500 per
file) and the unit tests at 100% line and branch coverage. `make audit`
runs pip-audit, `make build` builds and checks the sdist and wheel, and
`make docs` builds the manual. [`DEVELOPMENT.md`](DEVELOPMENT.md) maps
every CI gate to its command.

---

## Security

The package draws randomness only from `secrets` (the OS CSPRNG), makes
no network call, has no telemetry and never logs. A test fails if the
library imports `random`, `socket`, `ssl`, `http`, `urllib` or an HTTP
client. Error messages name the argument but never repeat its value.
`random_int` is unbiased by rejection sampling, and the tests check its
output for uniformity and against the share a modulo would give.

Report vulnerabilities according to [`SECURITY.md`](SECURITY.md).

---

## Documentation

[Manual](docs/index.md) · API reference: the docstrings (no rendered API
reference yet) · [Developer docs](DEVELOPMENT.md) ·
[Family map](#the-jspassgen-ecosystem)

Also: [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) ·
[Policies](docs/POLICIES.md) · [Changelog](CHANGELOG.md) ·
[Contributing](CONTRIBUTING.md) · [Governance](GOVERNANCE.md) ·
[Support](SUPPORT.md) · [Agent rules](AGENTS.md)

---

## Stability guarantees

The project is pre-1.0 and versions advance in `0.0.1` steps, in
lockstep with the jspassgen suite; 0.0.22 is the planned first suite
version and is not released. The breaking axis is the public API of
`jspassgen`: a removed or renamed name, argument or exception is
breaking. Once generators exist, output is part of the contract too: the
same configuration and the same random draws must produce the same
password as the JavaScript core, so a change to the order or number of
draws is breaking even when no signature moves. Names that start
with an underscore, modules included, are private. The Python
floor moves only as the [toolchain policy](docs/POLICIES.md) describes.

---

## License

This project is dual-licensed under either:

- Apache License, Version 2.0 ([`LICENSE-APACHE`](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT License ([`LICENSE-MIT`](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option. There are no run-time dependencies.

[core]: https://github.com/sebastienrousseau/jspassgen
[site]: https://jspassgen.com
