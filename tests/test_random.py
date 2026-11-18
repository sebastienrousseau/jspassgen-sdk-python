# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The random port and its ``secrets`` adapter."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from jspassgen import RandomGeneratorPort, SecretsRandom
from jspassgen.adapters import _below

RNG = SecretsRandom()

# chi-squared critical values for p = 1e-6, so a correct generator fails a
# run about once in a million (scipy.stats.chi2.isf(1e-6, df)).
CHI2_CRITICAL_P1E6 = {5: 35.888, 9: 44.811}

NOT_INTS = [1.0, 1.5, "1", None, b"\x01", True, False]
BELOW_ONE = [0, -1, -(2**70)]


def chi_squared(counts: Counter[int], buckets: int, draws: int) -> float:
    """Pearson's statistic of ``counts`` against a uniform distribution."""
    expected = draws / buckets
    return sum((counts[value] - expected) ** 2 / expected for value in range(buckets))


class FakeBits:
    """A ``randbits`` that returns a fixed sequence and records each call."""

    def __init__(self, values: list[int]) -> None:
        self._values: Iterator[int] = iter(values)
        self.calls: list[int] = []

    def __call__(self, bits: int) -> int:
        self.calls.append(bits)
        return next(self._values)


# --- the port ----------------------------------------------------------------


class Replay:
    """A deterministic port, the shape the conformance kit's tapes will use."""

    def random_bytes(self, n: int) -> bytes:
        return bytes(n)

    def random_int(self, max: int) -> int:
        return max - 1


def test_secrets_random_satisfies_the_port() -> None:
    assert isinstance(RNG, RandomGeneratorPort)


def test_a_deterministic_implementation_satisfies_the_port() -> None:
    port: RandomGeneratorPort = Replay()
    assert isinstance(port, RandomGeneratorPort)
    assert port.random_bytes(2) == b"\x00\x00"
    assert port.random_int(5) == 4


def test_an_object_without_the_methods_is_not_a_port() -> None:
    assert not isinstance(object(), RandomGeneratorPort)


def test_repr_holds_no_state() -> None:
    assert repr(RNG) == "SecretsRandom()"


# --- random_bytes ------------------------------------------------------------


@pytest.mark.parametrize("n", [1, 16, 32, 1000])
def test_random_bytes_returns_n_bytes(n: int) -> None:
    out = RNG.random_bytes(n)
    assert type(out) is bytes
    assert len(out) == n


def test_random_bytes_draws_differ() -> None:
    assert RNG.random_bytes(32) != RNG.random_bytes(32)


@pytest.mark.parametrize("n", NOT_INTS)
def test_random_bytes_refuses_a_non_int(n: Any) -> None:
    with pytest.raises(TypeError, match=r"^n must be an int$"):
        RNG.random_bytes(n)


@pytest.mark.parametrize("n", BELOW_ONE)
def test_random_bytes_refuses_less_than_one(n: int) -> None:
    with pytest.raises(ValueError, match=r"^n must be a positive integer$"):
        RNG.random_bytes(n)


# --- random_int --------------------------------------------------------------


def test_random_int_of_one_is_always_zero() -> None:
    assert {RNG.random_int(1) for _ in range(100)} == {0}


@given(st.integers(min_value=1, max_value=2**130))
def test_random_int_stays_in_range(max_: int) -> None:
    assert 0 <= RNG.random_int(max_) < max_


@pytest.mark.parametrize("max_", NOT_INTS)
def test_random_int_refuses_a_non_int(max_: Any) -> None:
    with pytest.raises(TypeError, match=r"^max must be an int$"):
        RNG.random_int(max_)


@pytest.mark.parametrize("max_", BELOW_ONE)
def test_random_int_refuses_less_than_one(max_: int) -> None:
    with pytest.raises(ValueError, match=r"^max must be a positive integer$"):
        RNG.random_int(max_)


@pytest.mark.parametrize("buckets", [6, 10])
def test_random_int_is_uniform(buckets: int) -> None:
    draws = 60_000
    counts = Counter(RNG.random_int(buckets) for _ in range(draws))
    assert set(counts) == set(range(buckets))
    assert chi_squared(counts, buckets, draws) < CHI2_CRITICAL_P1E6[buckets - 1]


@pytest.mark.parametrize(
    ("max_", "cut", "modulo_share"),
    [
        # A byte modulo 200 makes 0..55 twice as likely: 112/256 = 0.4375
        # of draws fall below 56 instead of 56/200 = 0.28.
        (200, 56, 0.4375),
        # 64 bits modulo 3 * 2**62 put 0.75 of draws below 2**63 instead of
        # 2/3.
        (3 * 2**62, 2**63, 0.75),
    ],
)
def test_random_int_has_no_modulo_bias(max_: int, cut: int, modulo_share: float) -> None:
    draws = 20_000
    share = sum(RNG.random_int(max_) < cut for _ in range(draws)) / draws
    unbiased = cut / max_
    # Five standard deviations of the unbiased share is under 0.016; the
    # biased share is at least 0.08 away.
    assert abs(share - unbiased) < 0.025
    assert abs(share - modulo_share) > 0.05


# --- rejection sampling ------------------------------------------------------


def test_below_rejects_draws_at_or_over_max() -> None:
    bits = FakeBits([7, 6, 5, 2])
    assert _below(5, bits) == 2
    assert bits.calls == [3, 3, 3, 3]


def test_below_accepts_the_first_draw_in_range() -> None:
    bits = FakeBits([4])
    assert _below(5, bits) == 4
    assert bits.calls == [3]


@pytest.mark.parametrize(("max_", "bits"), [(1, 0), (2, 1), (8, 3), (9, 4), (2**64, 64)])
def test_below_draws_the_bit_length_of_max_minus_one(max_: int, bits: int) -> None:
    fake = FakeBits([0])
    assert _below(max_, fake) == 0
    assert fake.calls == [bits]
