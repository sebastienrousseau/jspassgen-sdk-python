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

There is no release, fuzz or conformance workflow yet. Release is added
with the first publishable version; fuzzing has no input parser to
target; the conformance job arrives with jspassgen's kit.

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

Planned; nothing has been released. For each version:

1. On `feat/v<version>`: move the version in `pyproject.toml` and every
   restatement (`scripts/verify-release-versions`), date the
   `CHANGELOG.md` heading, and write `docs/releases/<version>.md` with a
   `## Highlights` section.
2. Merge the release pull request into `main` once CI is green.
3. Tag `main` with a signed annotated tag:
   `git tag -s v<version> -m "jspassgen-sdk-python v<version>"`, and push
   the tag.

The release workflow (build, `SHA256SUMS`, SBOM, provenance, GitHub
release, PyPI trusted publishing) is not written yet; it lands before
the first release, with a dry-run mode.
