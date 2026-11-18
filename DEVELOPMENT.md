<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Development

## Setup

```sh
mise install          # Python 3.14, uv 0.13.1, Node 24 (mise.toml)
make sync             # uv sync --frozen: the locked development environment
```

The project is built with hatchling and developed with uv; `uv.lock` is
committed and every `make` target runs with `--frozen`.

## Layout

| Path | What it holds |
| :--- | :--- |
| `src/jspassgen/ports.py` | `RandomGeneratorPort`, the interface generators will depend on |
| `src/jspassgen/adapters.py` | `SecretsRandom`, the port on `secrets`, and the rejection sampler |
| `tests/` | Unit tests: the port, the adapter's range, uniformity and errors, the import guard |
| `scripts/` | The version check and its test, the complexity check and its baseline, the README template check |
| `docs/` | The manual (MkDocs) |

## CI gates and their local commands

| CI job | What it checks | Local command |
| :--- | :--- | :--- |
| `ci.yml` lint | Version restatements, shellcheck, ruff, mypy --strict, complexity, pip-audit, the manual | `make versions lint format-check typecheck complexity audit docs` |
| `ci.yml` test (3.11 to 3.14) | Unit tests at 100% line and branch coverage | `make coverage` |
| `ci.yml` build | sdist and wheel, `twine check --strict`, a clean install | `make build` |
| `ci.yml` api | Public API against the last tag (griffe); informational until the first tag | `uvx --from griffe==2.4.1 griffe check jspassgen --search src --against <tag>` |
| `codeql.yml` | CodeQL for Python and for the workflows | (GitHub only) |
| `docs-lint.yml` | markdownlint, the README template, codespell, REUSE, links | `scripts/readme-check.sh` and the tools named in the workflow |
| `dco.yml` | `Signed-off-by:` on every commit | `git log --format=%B` |
| `scorecard.yml` | OpenSSF Scorecard | (GitHub only) |
| `release.yml` (on a `v*` tag) | The tag, `make check`, `make audit`, the build and `SHA256SUMS`; then PyPI and a draft GitHub release | `make check audit build` |

There is no fuzz or conformance workflow yet. Fuzzing has no input
parser to target; the conformance job arrives with the first ported
generator, which replays jspassgen's kit.

## Coverage

`make coverage` runs the unit tests under coverage.py with branch
coverage and fails below 100% (`fail_under = 100` in `pyproject.toml`).
There are no exclusion markers in `src/`.

## Complexity

`scripts/check_complexity.py` measures every function in `src/`,
`tests/` and `scripts/` with radon (cyclomatic, Halstead difficulty) and
complexipy (cognitive), plus function and file length, against
`scripts/complexity-baseline.json`. The baseline is empty; it can only
shrink. Ruff's `C90` rule enforces the cyclomatic ceiling too.

## Randomness tests

`tests/test_random.py` checks `random_int` two ways a broken sampler
would fail. A chi-squared test over 60,000 draws for 6 and 10 buckets
uses the critical value at p = 1e-6, so a correct generator fails about
once in a million runs. A bias test compares the share of draws below a
cut with the unbiased share and with the share a modulo reduction would
give, at 20,000 draws for a small `max` (200) and a large one
(`3 * 2**62`). The rejection loop itself is tested with a scripted bit
source.

## Release model

`.github/workflows/release.yml` releases a pushed `v<version>` tag.
Nothing has been released yet; the first release is the suite's first
lockstep version, 0.0.22.

1. On `feat/v<version>`: move the version in `pyproject.toml` and every
   restatement (`scripts/verify-release-versions`), and date the
   `CHANGELOG.md` heading. Merge the release pull request into `main`
   once CI is green.
2. Tag `main` with a signed annotated tag, check it with
   `git verify-tag v<version>` (`KEYS.asc`), and push it:
   `git tag -s v<version> -m "jspassgen-sdk-python v<version>"`.
3. The `check` job refuses a tag that is not annotated, not signed, not
   on the checked-out commit, or whose message or version does not match
   `pyproject.toml`. It runs `make check` and `make audit`, builds the
   sdist and wheel with `make build` (`twine check --strict`), and writes
   `SHA256SUMS`. CI cannot verify the signature itself; step 2 does.
4. The `publish-pypi` job waits for a maintainer to approve the `pypi`
   environment, checks the files against `SHA256SUMS`, and uploads them
   to PyPI through trusted publishing
   (`pypa/gh-action-pypi-publish`, which also uploads PEP 740
   attestations); no PyPI token is stored. A version already on PyPI is
   skipped, so a rerun is safe.
5. The `github-release` job drafts the GitHub release
   `jspassgen-sdk-python <version>` with the sdist, the wheel and
   `SHA256SUMS`. The maintainer writes the Highlights and publishes the
   draft.

Trusted publishing is configured on PyPI for the `jspassgen` project:
the trusted publisher names this repository, `release.yml` and the
`pypi` environment. Until the project exists on PyPI, that is a pending
publisher. There is no dry-run mode, SBOM or SLSA provenance yet.
