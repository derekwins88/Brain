#!/usr/bin/env bash
# Sync project's lean-toolchain with Mathlib's pinned toolchain.
# Strategy:
#  1) Parse Mathlib `rev` from Lake.toml and curl that commit's `lean-toolchain`.
#     (Avoids running `lake update`, so no cache/toolchain mismatch explosions.)
#  2) If curl path fails (no rev / no network), fall back to `elan`+`lake update || true`
#     and then copy `.lake/packages/mathlib/lean-toolchain` if present.
# Idempotent and safe for CI/local.

set -euo pipefail

PKG_DIR="${1:-lean}"
LAKE_TOML="$PKG_DIR/Lake.toml"
PROJECT_TC="$PKG_DIR/lean-toolchain"

if [[ ! -d "$PKG_DIR" ]]; then
  echo "sync_toolchain: package dir '$PKG_DIR' not found; nothing to do."
  exit 0
fi

# --- Try to extract Mathlib rev and fetch toolchain directly from GitHub ---
REV=""
if [[ -f "$LAKE_TOML" ]]; then
  # Grab the first 'rev = "...“' under the mathlib requirement if present
  REV="$(awk '
    BEGIN{inreq=0}
    /^\s*\[\[require\]\]/{inreq=0}
    /^\s*\[\[require\]\]/{block=1}
    block && /^\s*name\s*=\s*"mathlib"\s*$/ {inreq=1}
    inreq && /^\s*rev\s*=\s*"/ {
      match($0, /rev\s*=\s*"([^"]+)"/, m); if (m[1]!="") {print m[1]; exit}
    }
  ' "$LAKE_TOML" || true)"
fi

fetch_from_github() {
  local ref="$1"
  local url="https://raw.githubusercontent.com/leanprover-community/mathlib4/${ref}/lean-toolchain"
  echo "sync_toolchain: attempting to curl mathlib toolchain at ref '${ref}'"
  if curl -fsSL "$url" -o "$PROJECT_TC.tmp"; then
    mv "$PROJECT_TC.tmp" "$PROJECT_TC"
    echo "sync_toolchain: wrote $PROJECT_TC from mathlib4@${ref} ✅"
    return 0
  fi
  return 1
}

if [[ -n "${REV}" ]]; then
  if fetch_from_github "${REV}"; then exit 0; fi
fi

# If no rev in Lake.toml, try master/main heads in order
for ref in master main; do
  if fetch_from_github "${ref}"; then exit 0; fi
done

echo "sync_toolchain: curl path unavailable; falling back to lake materialization…"

# --- Fallback: ensure `lake` exists and materialize via `lake update || true` ---
if ! command -v lake >/dev/null 2>&1; then
  if command -v curl >/dev/null 2>&1; then
    echo "sync_toolchain: installing elan to obtain 'lake'…"
    curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | bash -s -- -y >/dev/null
    export PATH="$HOME/.elan/bin:$PATH"
  fi
fi

pushd "$PKG_DIR" >/dev/null

if command -v lake >/dev/null 2>&1; then
  # Don’t let cache mismatch kill us here.
  lake update || true
  MTC=".lake/packages/mathlib/lean-toolchain"
  if [[ -f "$MTC" ]]; then
    if [[ -f "lean-toolchain" ]] && cmp -s "$MTC" "lean-toolchain"; then
      echo "sync_toolchain: toolchain already in sync ✅"
    else
      cp "$MTC" "lean-toolchain"
      echo "sync_toolchain: synced toolchain from .lake/packages/mathlib ✅"
    fi
    popd >/dev/null
    exit 0
  else
    echo "sync_toolchain: mathlib toolchain file not found after lake update; skipping."
  fi
else
  echo "sync_toolchain: 'lake' not available; skipping."
fi

popd >/dev/null
exit 0

