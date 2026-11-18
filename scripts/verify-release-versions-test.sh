#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
# Tests scripts/verify-release-versions on a scratch copy of the files it
# reads: an undated `## [<version>] - Unreleased` CHANGELOG heading
# passes on a branch and fails with --tag; a dated heading passes with
# --tag only when docs/releases/<version>.md exists and the tag names
# the version; a restatement that disagrees fails. `make versions` and
# CI run it.
#
# Usage: scripts/verify-release-versions-test.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

version="$(sed -n 's/^version = "\([^"]*\)"$/\1/p' pyproject.toml | head -n 1)"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
failures=0

# fresh HEADING: a scratch copy whose CHANGELOG heading for the version
# reads `## [<version>] - HEADING`, with release highlights in place.
fresh() {
  rm -rf "$scratch/repo"
  mkdir -p "$scratch/repo/scripts" "$scratch/repo/docs/releases" \
    "$scratch/repo/.github/ISSUE_TEMPLATE"
  cp pyproject.toml uv.lock CITATION.cff CHANGELOG.md SECURITY.md SUPPORT.md \
    "$scratch/repo/"
  cp .github/ISSUE_TEMPLATE/bug_report.yml "$scratch/repo/.github/ISSUE_TEMPLATE/"
  cp scripts/verify-release-versions "$scratch/repo/scripts/"
  printf '# %s\n\n## Highlights\n' "$version" > "$scratch/repo/docs/releases/$version.md"
  sed -i.bak "s/^## \[$version\] - .*$/## [$version] - $1/" "$scratch/repo/CHANGELOG.md"
  grep -qx "## \[$version\] - $1" "$scratch/repo/CHANGELOG.md"
}

# case_ NAME WANT_STATUS WANT_STDERR [ARGS...]: run the script and
# compare its exit status and (when not empty) its stderr.
case_() {
  local name=$1 want=$2 needle=$3 status=0
  shift 3
  "$scratch/repo/scripts/verify-release-versions" "$@" > /dev/null 2> "$scratch/err" ||
    status=$?
  if [ "$status" -ne "$want" ] ||
    { [ -n "$needle" ] && ! grep -qF -- "$needle" "$scratch/err"; }; then
    echo "FAIL $name: exit $status (want $want), stderr:" >&2
    cat "$scratch/err" >&2
    failures=$((failures + 1))
  else
    echo "ok   $name"
  fi
}

fresh Unreleased
case_ "undated, branch" 0 ""
case_ "undated, tag" 1 "CHANGELOG.md does not date $version" --tag "v$version"
sed -i.bak "s/^version: \".*\"$/version: \"0.0.0\"/" "$scratch/repo/CITATION.cff"
case_ "stale CITATION.cff" 1 "CITATION.cff lacks"

fresh 2026-11-18
case_ "dated, tag" 0 "" --tag "v$version"
case_ "dated, wrong tag" 1 "tag v0.0.0, but" --tag v0.0.0
rm "$scratch/repo/docs/releases/$version.md"
case_ "dated, no highlights" 1 "docs/releases/$version.md is missing" --tag "v$version"

if [ "$failures" -ne 0 ]; then
  echo "verify-release-versions-test: $failures failure(s)" >&2
  exit 1
fi
echo "verify-release-versions-test: all cases pass"
