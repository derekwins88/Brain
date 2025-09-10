#!/usr/bin/env bash
# Sync project's lean-toolchain with Mathlib's pinned toolchain (idempotent).
# - Uses existing mathlib toolchain if available.
# - If missing and 'lake' exists, runs 'lake update' to materialize it.
# - If 'lake' is missing and toolchain isn't present, exits 0 (no-op).

set -euo pipefail

PKG_DIR="${1:-lean}"
MATHLIB_TC_REL=".lake/packages/mathlib/lean-toolchain"
PROJECT_TC_REL="lean-toolchain"

if [[ ! -d "$PKG_DIR" ]]; then
  echo "sync_toolchain: package dir '$PKG_DIR' not found; nothing to do."
  exit 0
fi

pushd "$PKG_DIR" >/dev/null

have_lake=0
if command -v lake >/dev/null 2>&1; then
  have_lake=1
fi

# If mathlib's toolchain isn't there yet, try to create it via 'lake update' when possible.
if [[ ! -f "$MATHLIB_TC_REL" ]]; then
  if [[ "$have_lake" -eq 1 ]]; then
    echo "sync_toolchain: '$MATHLIB_TC_REL' missing; running 'lake update' to materialize it..."
    lake update
  else
    echo "sync_toolchain: '$MATHLIB_TC_REL' missing and 'lake' not found; skip (will be retried later)."
    popd >/dev/null
    exit 0
  fi
fi

# If still missing after lake update, nothing to sync.
if [[ ! -f "$MATHLIB_TC_REL" ]]; then
  echo "sync_toolchain: mathlib toolchain still not found after 'lake update'; skipping."
  popd >/dev/null
  exit 0
fi

# Sync only when different (keeps git diffs clean).
if [[ -f "$PROJECT_TC_REL" ]] && cmp -s "$MATHLIB_TC_REL" "$PROJECT_TC_REL"; then
  echo "sync_toolchain: toolchain already in sync ✅"
else
  echo "sync_toolchain: syncing mathlib → project toolchain"
  cp "$MATHLIB_TC_REL" "$PROJECT_TC_REL"
fi

popd >/dev/null
