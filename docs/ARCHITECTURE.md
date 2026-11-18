<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Architecture

## Ports and adapters

The package follows the JavaScript core's layout: generators depend on
ports, and adapters implement them for a platform.

| Module | Role | JavaScript counterpart |
| :--- | :--- | :--- |
| `jspassgen.ports` | `RandomGeneratorPort`: `random_bytes(n)`, `random_int(max)` | `packages/core/src/ports/RandomGeneratorPort.js` (`generateRandomBytes`, `generateRandomInt`) |
| `jspassgen.adapters` | `SecretsRandom`: the port on `secrets` | `src/adapters/node/crypto-random.js` (`NodeCryptoRandom`) |

The core's two optional methods, `generateRandomBase64` and
`generateRandomString`, are not part of the Python port yet; they are
added only if the conformance kit's draw tapes need them.

## Synchronous by design

The JavaScript port's methods return promises. `secrets` is
synchronous, so the Python port returns values directly. The order and number of draws, which is what the conformance
kit pins, does not depend on this.

## Drawing an integer

`random_int(max)` computes `k`, the bit length of `max - 1`, draws `k`
bits with `secrets.randbits(k)`, and repeats while the draw is `max` or
more. Every value in `[0, max)` is equally likely, and each draw is
accepted with probability above one half. `max = 1` draws zero bits and
always returns 0. There is no upper bound on `max`.

Arguments are checked before any draw: a non-`int` (including `bool`)
raises `TypeError`, a value below 1 raises `ValueError`. The JavaScript
core raises `RangeError` for both; how the Python errors map to the
core's error codes is settled with the conformance kit.

## How the generators will use the port

Each generator will take a `RandomGeneratorPort`. In production that is
`SecretsRandom`; under the conformance kit it is a replay port that
returns the recorded draws in order and fails if the generator asks for
a different draw. That is how a port proves it makes the same draws as
the core, in the same order, and so produces the same password
([jspassgen ADR 0001](https://github.com/sebastienrousseau/jspassgen/blob/main/docs/adr/0001-ecosystem-lockstep.md),
section 4).
