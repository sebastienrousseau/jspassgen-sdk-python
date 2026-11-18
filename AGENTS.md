<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# AGENTS.md

`jspassgen-sdk-python` is the native Python port of jspassgen's core
(`packages/core` in [jspassgen](https://github.com/sebastienrousseau/jspassgen)),
a planned member of the jspassgen suite
([ADR 0001](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/adr/0001-ecosystem-lockstep.md)).
Its value is that a Python caller gets the same passwords, entropy and
errors as the JavaScript core, generated on their own machine from the
OS CSPRNG, with nothing sent anywhere. Today it holds the random port
and its `secrets` adapter only; the generators wait for the core's
conformance kit. Read [CONTRIBUTING.md](CONTRIBUTING.md) and
[DEVELOPMENT.md](DEVELOPMENT.md) as well.

## Rules

- **Version.** `0.0.x`, moving by exactly `0.0.1`, in lockstep with the
  jspassgen suite; never propose a jump. The version lives once, in
  `pyproject.toml`; when it moves, every file
  `scripts/verify-release-versions` lists moves with it (`uv.lock`,
  `CITATION.cff`, the SECURITY and SUPPORT tables, the bug template) and
  `CHANGELOG.md` gets the new `## [0.0.N] - Unreleased` heading. Work for
  the next version happens on `feat/v<next-version>`; every other
  branch, Dependabot's included, reaches it as commits, never as a merge
  into `main`.
- **Native port, local only.** No network call, no telemetry, no
  logging. Randomness comes only from `secrets` through
  `RandomGeneratorPort`; never import `random`. `tests/test_package.py`
  enforces the imports.
- **Unbiased draws.** `random_int` uses rejection sampling, never a
  modulo of raw bytes.
- **Do not port generators before the kit.** The generators, entropy,
  validation and wordlist are ported against jspassgen's conformance kit
  (draw tapes), vendored unchanged into `conformance/` with the source
  commit in `ci/core.ref`. Neither exists yet; do not invent vectors.
- **Never log or expose secrets.** No generated value in an exception
  message, `repr` or debug output; error messages name the argument, not
  its value.
- **Gates.** `make check` must pass: versions, ruff lint and format,
  `mypy --strict`, complexity (cyclomatic 10, cognitive 15, Halstead
  difficulty 30, 60 lines per function, 500 lines per file;
  `scripts/complexity-baseline.json` is empty and only shrinks), and 100%
  line and branch coverage. No blanket suppressions.
- **Commits.** Conventional, signed off by the maintainer
  (`git commit -s`, one `Signed-off-by:` line naming the human only),
  SSH-signed, with an `Assisted-by:` trailer for agent work. Never
  rewrite pushed history; never merge into `main` without the
  maintainer.

## The gate

```sh
make check
```

## Leave alone

`LICENSE*`, `LICENSES/`, `DCO.txt` and `KEYS.asc`, unless the task is to
update them.
