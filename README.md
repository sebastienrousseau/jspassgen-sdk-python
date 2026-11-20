<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

<p align="center">
  <img src="https://raw.githubusercontent.com/sebastienrousseau/jspassgen/main/.github/assets/logo.svg" alt="jspassgen logo" width="128" />
</p>

<h1 align="center">jspassgen-sdk-python</h1>

<p align="center">
  A native Python port of the jspassgen password and passphrase core that draws randomness only from the operating system's CSPRNG through the secrets module; this version ships the random port, not the generators.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/jspassgen-sdk-python/ci.yml?style=for-the-badge&logo=github" alt="Build" height="28" /></a>
  <a href="https://pypi.org/project/jspassgen/"><img src="https://img.shields.io/pypi/v/jspassgen?style=for-the-badge&color=fc8d62&logo=pypi&logoColor=white" alt="PyPI version" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/tree/main/docs"><img src="https://img.shields.io/badge/docs-manual-blue?style=for-the-badge&labelColor=555555&logo=readthedocs" alt="Docs" height="28" /></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/jspassgen-sdk-python"><img src="https://img.shields.io/ossf-scorecard/github.com/sebastienrousseau/jspassgen-sdk-python?style=for-the-badge&label=OpenSSF%20Scorecard&logo=openssf" alt="OpenSSF Scorecard" height="28" /></a>
  <a href="LICENSE-APACHE"><img src="https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg?style=for-the-badge" alt="License: Apache-2.0 OR MIT" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/jspassgen-sdk-python/blob/main/docs/POLICIES.md"><img src="https://img.shields.io/badge/Python-3.11%2B-93450a.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11 or newer" height="28" /></a>
</p>

<p align="center">
  <em>No demo yet: there is nothing to show until the generators are ported. The demo will record real generated passwords, not a mock-up.</em>
</p>

---

## Contents

**Getting started**

- [Install](#install): from PyPI with pip
- [Requirements](#requirements): Python floor, platforms
- [Quick Start](#quick-start): draw unbiased integers and bytes from the CSPRNG

**The jspassgen ecosystem**

- [The jspassgen ecosystem](#the-jspassgen-ecosystem): the core, its tools and the native SDKs, one version

**Library reference**

- [Capabilities at a glance](#capabilities-at-a-glance): what exists today and what is planned
- [Ecosystem comparison](#ecosystem-comparison): not written yet, and why
- [Benchmarks](#benchmarks): none yet, and why
- [Features](#features): module-level capability list
- [Configuration](#configuration): injecting a random port
- [Examples](#examples): none yet, and why

**Operational**

- [When not to use jspassgen-sdk-python](#when-not-to-use-jspassgen-sdk-python): limitations
- [Development](#development): make targets, CI
- [Security](#security): guarantees and reporting
- [Documentation](#documentation): all reference docs
- [Stability guarantees](#stability-guarantees): version axis, output contract, Python floor
- [License](#license)

---

## Install

### As a Python library

`release.yml` publishes each signed tag to PyPI through trusted
publishing. Install 0.0.22, the first release, with pip:

```bash
pip install jspassgen==0.0.22
python -c 'import jspassgen; print(jspassgen.__version__)'
```

This version ships the random port and its `secrets` adapter; the
generators come in a later version.

The distribution and the import package are both `jspassgen`. The
package has no run-time dependencies, ships type information (PEP 561,
`py.typed`) and is checked with `mypy --strict`.

---

## Requirements

- Python 3.11 or newer (`requires-python = ">=3.11"`).
- CI tests Python 3.11, 3.12, 3.13 and 3.14 on Ubuntu 24.04.
- Pure Python, standard library only. Randomness comes from `secrets`,
  which reads the operating system's CSPRNG through `os.urandom`.

The floor rises only when a Python version reaches its end of life, as
the [toolchain policy](docs/POLICIES.md) describes.

---

## Quick Start

```python
from jspassgen import SecretsRandom

rng = SecretsRandom()
print(rng.random_int(6) + 1)  # a fair die roll, 1 to 6
print(rng.random_bytes(16).hex())  # 16 bytes from the OS CSPRNG
```

`random_int(max)` returns an integer in `[0, max)` with every value
equally likely. It draws the bit length of `max - 1` and rejects any draw
of `max` or more, rather than reducing raw bytes modulo `max`, which
would favour the low values. Both methods refuse an argument below 1 with
`ValueError`, and anything that is not an `int` (including `bool`) with
`TypeError`.

This is the random port the generators will be built on. It does not
generate passwords yet.

---

## The jspassgen ecosystem

jspassgen is one core library and the tools, SDKs and site around it.
Every member is listed in
[`docs/ecosystem.json`](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/ecosystem.json)
and, from the suite's first lockstep release, every member ships the same
version ([ADR 0001](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/adr/0001-ecosystem-lockstep.md)).
The JavaScript tools depend on the core and add no generation logic of
their own; each SDK is a native port that is checked against the core's
conformance kit as its generators land.

| Component | Purpose | Use case |
| :--- | :--- | :--- |
| [`jspassgen`](https://github.com/sebastienrousseau/jspassgen) | Password and passphrase core, Node.js library, CLI, web UI and workers; source of the conformance kit | Programs that generate secrets |
| [`jspassgen-cli`](https://github.com/sebastienrousseau/jspassgen-cli) | Command-line generator built on the core | Passwords in a terminal or a script |
| [`jspassgen-mcp`](https://github.com/sebastienrousseau/jspassgen-mcp) | Local stdio MCP server | AI agents that need a generated secret |
| [`jspassgen-lsp`](https://github.com/sebastienrousseau/jspassgen-lsp) | Language server for weak literal secrets | Editors checking configuration and `.env` files |
| **`jspassgen-sdk-python`** | Native port on the `secrets` module | Python programs |
| [`jspassgen-sdk-rust`](https://github.com/sebastienrousseau/jspassgen-sdk-rust) | Native port on the OS CSPRNG | Rust programs |
| [`jspassgen-sdk-java`](https://github.com/sebastienrousseau/jspassgen-sdk-java) | Native port on `SecureRandom` | JVM programs |
| [`jspassgen-sdk-dotnet`](https://github.com/sebastienrousseau/jspassgen-sdk-dotnet) | Native port on `RandomNumberGenerator` | .NET programs |
| [`jspassgen-sdk-cpp`](https://github.com/sebastienrousseau/jspassgen-sdk-cpp) | Native C++17 port on the OS CSPRNG | C++ programs |
| [`jspassgen.github.io`](https://github.com/sebastienrousseau/jspassgen.github.io) | Source of [jspassgen.com](https://jspassgen.com) | Evaluating the suite |

Every member ships at 0.0.22, the suite's first lockstep release: the
core, CLI, MCP and LSP servers on npm, the Python, Rust, Java and .NET
SDKs on PyPI, crates.io, Maven Central and NuGet, and the C++ SDK and
the site as GitHub releases. The table gives each member's purpose, and
each README's Capabilities at a glance says what works today.

---

## Capabilities at a glance

| Area | Capability | Status |
| :--- | :--- | :--- |
| Randomness | `RandomGeneratorPort`: `random_bytes(n)`, `random_int(max)` | Released in 0.0.22 |
| Randomness | `SecretsRandom`: the port on `secrets`, unbiased `random_int` | Released in 0.0.22 |
| Conformance | The core's kit vendored into `conformance/`, every draw tape replayed in CI | Planned: the kit ships in jspassgen 0.0.21, not vendored here yet |
| Generators | The core's password types: `strong`, `base64`, `custom`, `diceware`, `memorable`, `pronounceable`, `honeyword`, `quantum-resistant` | Planned, against the kit |
| Entropy | Entropy calculation and validation with the core's error messages | Planned, against the kit |
| Wordlist | The EFF diceware list, byte-identical to the core's | Planned, against the kit |

---

## Ecosystem comparison

Not written yet. A comparison with other Python password generators
compares generators, and this package has none yet. It will be written,
with evidence, once the generators pass the conformance kit.

---

## Benchmarks

None are published yet. There is no generator to measure, and timing a
thin wrapper around `secrets` would say nothing about the port.
Benchmarks arrive with the generators.

---

## Features

- `jspassgen.ports.RandomGeneratorPort` is a runtime-checkable
  `typing.Protocol` with `random_bytes(n) -> bytes` and
  `random_int(max) -> int`, the Python form of the core's
  `RandomGeneratorPort` (`generateRandomBytes`, `generateRandomInt`).
- `jspassgen.adapters.SecretsRandom` implements the port on `secrets`.
  It is stateless and safe to share between threads.
- `jspassgen.__version__` holds the installed version, read from the
  package metadata.

The top-level package exports `RandomGeneratorPort`, `SecretsRandom` and
`__version__`.

---

## Configuration

There is nothing to configure yet. Code that needs randomness takes a
`RandomGeneratorPort`, so a test can pass a deterministic implementation
in place of `SecretsRandom`; the conformance kit replays recorded draws
this way. Never pass a non-cryptographic source when generating a real
secret.

---

## Examples

None yet. The only public surface is the random port, and the Quick
Start above covers it. Runnable examples arrive with the generators.

---

## When not to use jspassgen-sdk-python

- This version generates no passwords or passphrases. Use the
  JavaScript [`jspassgen`](https://github.com/sebastienrousseau/jspassgen)
  core, or `secrets` directly (`secrets.token_urlsafe`, `secrets.choice`).
- Byte-for-byte agreement with the JavaScript core is the goal, but no
  vector of the core's conformance kit runs here yet.
- `SecretsRandom` cannot be seeded, by design. A deterministic port is
  for tests only, so this is the wrong tool for a reproducible sequence.

---

## Development

```bash
mise install   # Python 3.14, uv 0.13.1, Node 24 (mise.toml)
make check     # versions, ruff, mypy --strict, complexity, 100% coverage
make audit     # pip-audit over every locked dependency
make build     # build and check the sdist and wheel
make fuzz      # Atheris on the API contract, 60 s (Linux x86-64 only)
make docs      # build the manual (mkdocs --strict)
```

`make check` is the gate CI runs: the version restatements, ruff (lint
and format), `mypy --strict`, the complexity ceilings (cyclomatic 10,
cognitive 15, Halstead difficulty 30, 60 lines per function, 500 per
file) and the unit tests at 100% line and branch coverage. CI also runs
shellcheck, a 60-second Atheris fuzz run, the API compatibility check
(griffe) and the docs lint (markdownlint, codespell, REUSE, links and
the README check).
[`DEVELOPMENT.md`](DEVELOPMENT.md) maps every CI gate to its command.

---

## Security

The package draws randomness only from `secrets` (the OS CSPRNG), makes
no network call, has no telemetry and never logs. A test fails if the
library imports `random`, `socket`, `ssl`, `http`, `urllib` or an HTTP
client. Error messages name the argument but never repeat its value.
`random_int` is unbiased by rejection sampling, and the tests check its
output for uniformity (chi-squared) and against the share a modulo would
give.

Report vulnerabilities according to [`SECURITY.md`](SECURITY.md).

---

## Documentation

- [Manual](docs/index.md)
- [Developer documentation](DEVELOPMENT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Policies](docs/POLICIES.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Governance](GOVERNANCE.md)
- [Support](SUPPORT.md)
- [Agent rules](AGENTS.md)

The API reference is the docstrings; there is no rendered API reference
yet.

---

## Stability guarantees

- Versions advance in `0.0.1` steps in lockstep with the jspassgen suite;
  0.0.22 is the first released suite version.
- The breaking axis is the public API of `jspassgen`: a removed or
  renamed name, argument or exception is breaking.
- Once generators exist, output is part of the contract: the same
  configuration and the same random draws must produce the same password
  as the JavaScript core, so a change to the order or number of draws is
  breaking even when no signature moves.
- Names that start with an underscore, modules included, are private.
- A public name is deprecated for at least one release before removal.
- The Python floor moves only as the [toolchain policy](docs/POLICIES.md)
  describes.

---

## License

Licensed under either [Apache License 2.0](LICENSE-APACHE) or
[MIT](LICENSE-MIT), at your option.
