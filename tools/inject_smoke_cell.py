#!/usr/bin/env python3
"""
Idempotently injects a smoke-guard cell at the top of a notebook so CI can
render a fast placeholder image without running heavy cells.

Usage:
  python tools/inject_smoke_cell.py notebooks/render_infographic.ipynb
"""
import json, sys, pathlib

MARK = "# --- SMOKE-GUARD: day3 infographic ---"

SMOKE_CELL = f"{MARK}\n" + """
import os, datetime as dt, json, pathlib
SMOKE = os.getenv("SMOKE", "0") == "1"
OUT_PNG = pathlib.Path("docs/day3_infographic.png")
OUT_JSON = pathlib.Path("docs/day3_infographic.json")
CAP_JSON = pathlib.Path("capsules/SIEVE_DAY2.json")

def utc_now_z():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

if SMOKE:
    import PIL.Image, PIL.ImageDraw
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img = PIL.Image.new("RGB", (1280, 720), (18,18,18))
    d = PIL.ImageDraw.Draw(img)
    d.text((40, 40), "Day-3 Infographic (SMOKE)", fill=(235,235,235))
    d.text((40,120), f"Timestamp: {utc_now_z()}", fill=(180,180,180))
    d.text((40,170), "Source: capsules/SIEVE_DAY2.json (if present)", fill=(180,180,180))
    img.save(OUT_PNG)

    meta = {
        "schema_version": "1.0.0",
        "title": "Infographic (smoke)",
        "subtitle": "CI placeholder; full render runs locally/Colab",
        "metrics": {"np_wall_pct": None, "thresholds": {"np": 0.09, "p": 0.045}},
        "source_capsule": str(CAP_JSON) if CAP_JSON.exists() else None,
        "timestamp": utc_now_z(),
        "ci": True,
    }
    try:
        OUT_JSON.write_text(json.dumps(meta, indent=2))
    except Exception:
        pass

    import sys
    print("SMOKE=1 → wrote placeholder PNG/JSON; exiting before heavy cells.")
    sys.exit(0)
"""

def main(path: str):
    p = pathlib.Path(path)
    nb = json.loads(p.read_text())
    cells = nb.get("cells", [])
    if cells and isinstance(cells[0], dict):
        src0 = "".join(cells[0].get("source", []))
        if MARK in src0:
            print("Smoke cell already present; nothing to do.")
            return
    # Insert new code cell at index 0
    cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + ("\n" if not line.endswith("\n") else "") for line in SMOKE_CELL.splitlines()],
    }
    nb.setdefault("cells", [])
    nb["cells"] = [cell] + nb["cells"]
    p.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
    print(f"Injected smoke cell into {p}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: inject_smoke_cell.py <notebook.ipynb>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
