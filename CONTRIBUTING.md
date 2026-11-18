<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Contributing

Thanks for looking. This package is the native Python port of the
[jspassgen](https://github.com/sebastienrousseau/jspassgen) core. The
JavaScript core defines the behaviour; a change here should make the
port more faithful to it, safer or easier to use.

## Before you open a pull request

Everything CI checks, you can run locally (`mise install` provides
Python and uv):

```sh
make check            # versions, ruff, mypy --strict, complexity, 100% coverage
```

## Rules

- **CSPRNG only.** Randomness comes from `secrets` through
  `RandomGeneratorPort`. Never import `random`, and never reduce random
  bytes modulo a range.
- **Local only.** No network access, telemetry or logging in the
  library.
- **Generators follow the conformance kit.** Generators are ported once
  jspassgen publishes its conformance kit; a generator without the kit's
  vectors behind it will not be merged.
- **Complexity ceilings.** Every function stays within cyclomatic 10,
  cognitive 15, Halstead difficulty 30 and 60 lines, and every file
  within 500 lines (`make complexity`).
- **100% coverage.** `make coverage` fails below 100% of lines and
  branches in `src/`; add the test with the code.
- **No suppressions.** Fix the cause rather than adding `noqa` or
  `type: ignore`; a justified exception is a specific inline code with a
  reason.
- **Tests with the change**, in the same commit.

## Commits

Conventional commits (`feat:`, `fix:`, `docs:`, `ci:`, `test:`,
`chore:`), an imperative subject of at most 50 characters, and a body
wrapped at 72 characters that explains what and why. Every commit
carries a `Signed-off-by:` trailer (`git commit -s`), which certifies
the [DCO](DCO.txt), and is signed.

## Versioning

The version lives in `pyproject.toml` and is restated in the files
`scripts/verify-release-versions` lists; `make check` and CI run it.
**Versions increment by 0.0.1**, in lockstep with the suite.
[DEVELOPMENT.md](DEVELOPMENT.md) describes the release model.

## Licence

Apache-2.0 OR MIT, at your option. By contributing you agree your work is
released under the same dual grant.
