# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Coverage-guided fuzzing of ``SecretsRandom`` with Atheris (libFuzzer).

Every input goes through ``tests.fuzz_contract.check``, the same
properties the unit tests replay. Run from the repository root, on Linux
x86-64 with Python 3.12 or later (where Atheris ships wheels):

    uv run --frozen python -m fuzz.fuzz_random -max_total_time=60 \\
      .fuzz-corpus fuzz/corpus

``make fuzz`` does this with a scratch copy of the corpus.
"""

from __future__ import annotations

import sys

import atheris

with atheris.instrument_imports():
    from tests.fuzz_contract import check


def main() -> None:
    """Hand ``check`` to libFuzzer with the command-line options."""
    atheris.Setup(sys.argv, check)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
