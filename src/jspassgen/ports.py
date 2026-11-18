# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Ports: the interfaces the generators will depend on.

``RandomGeneratorPort`` is the Python form of ``RandomGeneratorPort`` in
jspassgen's ``packages/core/src/ports/RandomGeneratorPort.js``: the two
required methods, ``generateRandomBytes`` and ``generateRandomInt``,
become ``random_bytes`` and ``random_int``. The JavaScript methods return
promises; these return values directly, since every Python source of
randomness the port wraps is synchronous.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class RandomGeneratorPort(Protocol):
    """A source of cryptographically secure randomness.

    Every implementation used to generate a secret must draw from a
    cryptographically secure generator. A deterministic implementation is
    for tests only (the conformance kit replays recorded draws through
    one).
    """

    def random_bytes(self, n: int) -> bytes:
        """Return ``n`` random bytes.

        Raises:
            TypeError: ``n`` is not an ``int`` (``bool`` is refused).
            ValueError: ``n`` is less than 1.
        """
        ...

    def random_int(self, max: int) -> int:
        """Return a uniformly distributed integer in ``[0, max)``.

        Raises:
            TypeError: ``max`` is not an ``int`` (``bool`` is refused).
            ValueError: ``max`` is less than 1.
        """
        ...
