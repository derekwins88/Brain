#!/usr/bin/env bash
set -euo pipefail

PKG_DIR="${1:-lean}"

if [[ ! -d "$PKG_DIR" ]]; then
  echo "error: package directory '$PKG_DIR' not found" >&2
  exit 1
fi

pushd "$PKG_DIR" >/dev/null

if ! command -v lake >/dev/null; then
  echo "error: 'lake' not on PATH; install elan first." >&2
  exit 1
fi

echo "==> lake update (to resolve mathlib and generate manifest)"
lake update

MATHLIB_TC=".lake/packages/mathlib/lean-toolchain"
PROJECT_TC="lean-toolchain"

if [[ ! -f "$MATHLIB_TC" ]]; then
  echo "error: '$MATHLIB_TC' not found after 'lake update'." >&2
  exit 1
fi

NEED_COPY=1
if [[ -f "$PROJECT_TC" ]]; then
  if cmp -s "$MATHLIB_TC" "$PROJECT_TC"; then
    NEED_COPY=0
  fi
fi

if [[ "$NEED_COPY" -eq 1 ]]; then
  echo "==> syncing toolchain from mathlib → project"
  cp "$MATHLIB_TC" "$PROJECT_TC"
else
  echo "==> toolchain already in sync"
fi

popd >/dev/null
