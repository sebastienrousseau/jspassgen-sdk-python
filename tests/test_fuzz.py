# SPDX-License-Identifier: Apache-2.0 OR MIT
"""The fuzz contract, replayed: the seed corpus and Hypothesis bytes.

``fuzz/fuzz_random.py`` runs ``check`` under Atheris where Atheris
installs; these tests run the same properties everywhere, so a seed or a
property that breaks fails the unit tests, not only the fuzz job.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.fuzz_contract import check

CORPUS = sorted((Path(__file__).parent.parent / "fuzz" / "corpus").iterdir())


def test_the_corpus_is_not_empty() -> None:
    assert len(CORPUS) >= 10


@pytest.mark.parametrize("seed", CORPUS, ids=lambda path: path.name)
def test_seed_keeps_the_contract(seed: Path) -> None:
    check(seed.read_bytes())


@given(st.binary(max_size=64))
def test_any_input_keeps_the_contract(data: bytes) -> None:
    check(data)
