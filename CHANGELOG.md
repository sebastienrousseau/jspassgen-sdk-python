<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions
advance in `0.0.1` steps in lockstep with the jspassgen suite.

## [0.0.22] - Unreleased

The repository's first version, planned as the first jspassgen suite
release. Nothing is published yet.

### Added

- `RandomGeneratorPort`, the Python form of the core's random port:
  `random_bytes(n)` and `random_int(max)`.
- `SecretsRandom`, the port on the `secrets` module, with `random_int`
  unbiased by rejection sampling; `TypeError` for a non-`int` argument,
  `ValueError` for one below 1.
- Tests for range, uniformity (chi-squared), the absence of modulo bias,
  the rejection loop and every error; a test that the library imports
  nothing that reaches the network and not `random`.
- The repository standard: `make check` gate, CI on Python 3.11 to 3.14,
  CodeQL, DCO, docs lint (markdownlint, codespell, REUSE, links), OpenSSF
  Scorecard, Dependabot, community files and the manual in `docs/`.
- The release workflow (`.github/workflows/release.yml`), run on a
  pushed `v*` tag: it refuses a tag that is not annotated and signed,
  not on the checked-out commit, or whose message or version does not
  match `pyproject.toml`; runs `make check` and `make audit`; builds the
  sdist and wheel with `SHA256SUMS`; publishes to PyPI through trusted
  publishing behind the `pypi` environment; and drafts the GitHub
  release with the files and checksums.
