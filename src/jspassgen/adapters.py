# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Adapters: implementations of the ports.

``SecretsRandom`` implements ``RandomGeneratorPort`` on the standard
library's ``secrets`` module, which draws from the operating system's
CSPRNG (``os.urandom``). It is the Python counterpart of jspassgen's
``NodeCryptoRandom`` (Node.js ``crypto``).
"""

from __future__ import annotations

import secrets
from collections.abc import Callable

__all__ = ["SecretsRandom"]


def _require_positive_int(value: object, name: str) -> int:
    """Return ``value`` if it is an ``int`` of at least 1, else raise.

    The message names the argument but never repeats its value.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")
    if value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _below(max: int, randbits: Callable[[int], int]) -> int:
    """Return an unbiased integer in ``[0, max)`` by rejection sampling.

    Draws ``k`` random bits, where ``k`` is the bit length of ``max - 1``,
    and discards any draw of ``max`` or more. Every value in range is
    equally likely, which a modulo of raw bytes would not give. Each draw
    is accepted with probability greater than one half, so the expected
    number of draws is below two.
    """
    bits = (max - 1).bit_length()
    while True:
        candidate = randbits(bits)
        if candidate < max:
            return candidate


class SecretsRandom:
    """``RandomGeneratorPort`` on ``secrets``, the OS CSPRNG.

    Stateless and safe to share between threads.
    """

    __slots__ = ()

    def random_bytes(self, n: int) -> bytes:
        """Return ``n`` bytes from ``secrets.token_bytes``.

        Raises:
            TypeError: ``n`` is not an ``int`` (``bool`` is refused).
            ValueError: ``n`` is less than 1.
        """
        return secrets.token_bytes(_require_positive_int(n, "n"))

    def random_int(self, max: int) -> int:
        """Return a uniform integer in ``[0, max)``, unbiased.

        Rejection sampling over ``secrets.randbits``; no upper bound on
        ``max``.

        Raises:
            TypeError: ``max`` is not an ``int`` (``bool`` is refused).
            ValueError: ``max`` is less than 1.
        """
        return _below(_require_positive_int(max, "max"), secrets.randbits)

    def __repr__(self) -> str:
        return "SecretsRandom()"
