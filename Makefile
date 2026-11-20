# SPDX-License-Identifier: Apache-2.0 OR MIT
#
# `make check` is the gate: version restatements, ruff (lint and format),
# mypy --strict, the complexity ceilings, and the unit tests at 100% line
# and branch coverage. Everything runs through uv in the locked
# environment (`uv sync` first; `make` does it).

UV  ?= uv
RUN  = $(UV) run --frozen

.PHONY: check sync versions lint format format-check typecheck complexity test coverage \
  fuzz audit build docs clean

check: sync versions lint format-check typecheck complexity coverage

sync:
	$(UV) sync --frozen --all-groups

versions:
	./scripts/verify-release-versions
	./scripts/verify-release-versions-test.sh

lint:
	$(RUN) ruff check .

format:
	$(RUN) ruff check --fix --select I .
	$(RUN) ruff format .

format-check:
	$(RUN) ruff format --check .

typecheck:
	$(RUN) mypy

# Cyclomatic 10, cognitive 15, Halstead difficulty 30, 60 lines per
# function, 500 lines per file (radon and complexipy), against
# scripts/complexity-baseline.json, which is empty.
complexity:
	$(RUN) python scripts/check_complexity.py

test:
	$(RUN) pytest

# The unit tests, gated at 100% line and branch.
coverage:
	$(RUN) coverage run -m pytest
	$(RUN) coverage report
	$(RUN) coverage xml -q

# Atheris (libFuzzer) on tests/fuzz_contract.py for FUZZ_SECONDS, from a
# scratch copy of fuzz/corpus. Atheris installs only on Linux x86-64 with
# CPython 3.12 to 3.14 (pyproject.toml); the unit tests replay the same
# contract everywhere. A crash is written to .fuzz-corpus/.
FUZZ_SECONDS ?= 60

fuzz:
	rm -rf .fuzz-corpus
	mkdir -p .fuzz-corpus/new
	$(RUN) python -m fuzz.fuzz_random -max_total_time=$(FUZZ_SECONDS) \
	  -artifact_prefix=.fuzz-corpus/ .fuzz-corpus/new fuzz/corpus

# pip-audit over every locked dependency, development tools included.
audit:
	$(UV) export --frozen --all-groups --no-emit-project --format requirements-txt \
	  -o .audit-requirements.txt -q
	$(RUN) pip-audit --strict --require-hashes --disable-pip -r .audit-requirements.txt
	rm -f .audit-requirements.txt

build:
	rm -rf dist
	$(UV) build
	$(RUN) twine check --strict dist/*

docs:
	$(UV) run --frozen --group docs mkdocs build --strict

clean:
	rm -rf dist build site htmlcov .coverage coverage.xml .hypothesis .fuzz-corpus
