# SPDX-License-Identifier: Apache-2.0 OR MIT
"""jspassgen for Python: a native port of the jspassgen core, in progress.

This version provides the random port and its CSPRNG adapter only. The
password and passphrase generators follow, each checked against
jspassgen's conformance kit (shipped in jspassgen 0.0.21).
"""

from __future__ import annotations

from importlib.metadata import version as _version

from jspassgen.adapters import SecretsRandom
from jspassgen.ports import RandomGeneratorPort

__all__ = ["RandomGeneratorPort", "SecretsRandom", "__version__"]

#: The installed distribution's version; ``pyproject.toml`` is its source.
__version__: str = _version("jspassgen")
