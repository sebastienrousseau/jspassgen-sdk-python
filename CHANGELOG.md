<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions
advance in `0.0.1` steps in lockstep with the jspassgen suite.

## [0.0.24] - Unreleased

### Added

- Releases carry their SLSA build provenance. The release workflow
  attests every release file with `actions/attest-build-provenance`,
  signed through Sigstore and stored as a GitHub attestation, and
  attaches the bundle, listed in the release checksums, as
  `jspassgen-sdk-python-<version>.intoto.jsonl`. Check a download with
  `gh attestation verify <file> --repo sebastienrousseau/jspassgen-sdk-python`.
  This answers the OpenSSF Scorecard Signed-Releases check.

## [0.0.23] - 2026-11-20

The suite's second lockstep version. The library is unchanged: same
`RandomGeneratorPort` and `SecretsRandom`, same behaviour.

### Added

- Fuzzing with Atheris: `fuzz/fuzz_random.py` runs the public API's
  contract (`tests/fuzz_contract.py`: range, length, errors and their
  messages, and the rejection loop) under libFuzzer from a seed corpus,
  through `make fuzz` and a 60-second CI job on Linux. The unit tests
  replay the corpus and Hypothesis input through the same contract on
  every platform. Atheris is a `fuzz` dependency group, installed only
  on Linux x86-64 with CPython 3.12 to 3.14.
- `.github/CODEOWNERS`, naming the maintainer as owner of every file.

### Changed

- The release workflow's post-publish check saves PyPI's JSON and reads
  the file digests with `jq` instead of piping `curl` into `python3`
  (OpenSSF Scorecard, PinnedDependencies). An empty file list now
  retries instead of passing.

## [0.0.22] - 2026-11-18

The repository's first version, released as the first jspassgen suite
release.

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
