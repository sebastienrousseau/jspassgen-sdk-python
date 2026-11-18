<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Roadmap

The order follows
[jspassgen ADR 0001](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/adr/0001-ecosystem-lockstep.md).
Nothing here is dated.

1. **Random port and CSPRNG adapter.** Done on `feat/v0.0.22`.
2. **Conformance kit, in jspassgen.** Draw tapes, error cases, the EFF
   wordlist and `SHA256SUMS`, generated from the core. Done in jspassgen
   0.0.21.
3. **Vendor the kit.** `conformance/` unchanged, `ci/core.ref` naming the
   source commit, a checksum test and a CI job that replays every tape.
4. **Port the generators**, entropy calculation and validation, each
   passing the kit.
5. **Release.** The release workflow (`release.yml`: tag checks, PyPI
   trusted publishing, `SHA256SUMS`, a draft GitHub release) lands in
   0.0.22. Still to come: a dry-run mode and an SBOM; then examples,
   benchmarks and the README demo, all against real output.
