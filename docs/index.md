<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# jspassgen for Python

A native Python port of the
[jspassgen](https://github.com/sebastienrousseau/jspassgen) password and
passphrase core, in development. This version provides the random port
the generators will be built on, and its adapter on the `secrets`
module. Nothing is published to PyPI yet.

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
