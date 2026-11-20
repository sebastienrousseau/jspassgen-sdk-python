<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# jspassgen for Python

A native Python port of the
[jspassgen](https://github.com/sebastienrousseau/jspassgen) password and
passphrase core. This version provides the random port the generators
will be built on, and its adapter on the `secrets` module. It is on PyPI
as `jspassgen` (`pip install jspassgen==0.0.23`).

```python
from jspassgen import SecretsRandom

rng = SecretsRandom()
print(rng.random_int(6) + 1)  # a fair die roll, 1 to 6
print(rng.random_bytes(16).hex())
```

- [Architecture](ARCHITECTURE.md): the port, the adapter, and how the
  generators will use them.
- [Policies](POLICIES.md): toolchain, versioning, deprecation.
- [Roadmap](ROADMAP.md): what comes next and in which order.
