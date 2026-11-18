<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Governance

How jspassgen-sdk-python is run, who decides, and what happens if the
maintainer is unavailable.

## Scope

The package is the native Python port of the jspassgen core. Changes are
weighed against that: agreement with the JavaScript core (proven by the
conformance kit once it exists), security and clarity over feature
breadth.

## Roles

| Role | Who | Responsibilities |
| :--- | :--- | :--- |
| **Maintainer** | Sebastien Rousseau (single maintainer) | Reviews and merges pull requests, cuts and signs releases, triages issues and security reports, sets direction, holds the repository's admin rights |
| **Contributor** | Anyone with a merged pull request | Proposes changes with tests, reviews others' pull requests |
| **User** | Everyone | Reports bugs, asks questions, requests features through issues |

## Decisions

- **Day-to-day changes** (fixes, tests, docs, additive features within
  scope) land on the release branch `feat/v<next-version>`; the
  maintainer merges it once CI is green.
- **Significant changes** (a breaking change to the public API, a new
  dependency, a change to how randomness is drawn) start as an issue and
  get an ADR in `docs/adr/`.
- **Behaviour shared with the core** (generators, entropy, error codes,
  the order of random draws) is decided in
  [jspassgen](https://github.com/sebastienrousseau/jspassgen) and lands
  here through its conformance kit.
- **The suite version** is decided for the whole jspassgen family: this
  package moves in lockstep, one `0.0.1` step at a time.

Every change passes the CI gates (lint, types, complexity, 100% line and
branch coverage on Python 3.11 to 3.14, CodeQL, the DCO check) before
merge. At most one pull request targets `main` at a time: the release
branch.

## Releases

Releases follow the process in [DEVELOPMENT.md](DEVELOPMENT.md#release-model).
Only the maintainer pushes tags.

## Access continuity

- **Code and history** are public on GitHub; anyone can fork and build
  from them. Every commit and tag is signed.
- **No secret is needed to build or test.** PyPI publishing will use
  trusted publishing (OIDC), with no stored token.
- **If the maintainer is unreachable** for 90 days, the project should
  be treated as unmaintained: users should pin a release, and a fork may
  continue it under a new name. Adding a second maintainer is a standing
  goal.

## Code of conduct

Everyone in the project follows [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
