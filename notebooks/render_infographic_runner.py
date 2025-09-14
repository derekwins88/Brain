#!/usr/bin/env python3
# Lightweight runner: render infographic if JSON exists, otherwise create a smoke PNG so CI artifacts exist.
import os, json, datetime as dt
import matplotlib.pyplot as plt

# Determine root: if current working directory is notebooks, move one level up
ROOT = (
    os.path.abspath(os.path.join(os.getcwd(), ".."))
    if os.path.basename(os.getcwd()) == "notebooks"
    else os.getcwd()
)
JSON_PATH = os.environ.get(
    "INFO_JSON", os.path.join(ROOT, "docs", "day3_infographic.json")
)
PNG_PATH = os.environ.get(
    "INFO_PNG", os.path.join(ROOT, "docs", "day3_infographic.png")
)

os.makedirs(os.path.dirname(PNG_PATH), exist_ok=True)

if not os.path.exists(JSON_PATH):
    # Create a small smoke PNG so CI artifacts still exist
    fig = plt.figure(figsize=(6, 3), dpi=160)
    ax = fig.add_subplot(111)
    ax.axis("off")
    ax.text(
        0.5,
        0.6,
        "SMOKE: Missing JSON",
        ha="center",
        va="center",
        fontsize=14,
        color="red",
    )
    ax.text(0.5, 0.4, f"Expected: {JSON_PATH}", ha="center", va="center", fontsize=10)
    fig.patch.set_facecolor("black")
    plt.savefig(PNG_PATH, bbox_inches="tight")
    print(f"JSON not found at {JSON_PATH}; wrote smoke PNG to {PNG_PATH}")
    raise SystemExit(0)

# Otherwise load JSON and render
with open(JSON_PATH) as f:
    meta = json.load(f)

if meta.get("timestamp") == "{{AUTO}}":
    meta["timestamp"] = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"

title = meta.get("title", "Infographic (auto)")
notes = meta.get("notes", [])
palette = meta.get("visuals", {}).get("palette", [])
accent = palette[0] if palette else "white"
bg = palette[1] if len(palette) > 1 else "#000000"

fig = plt.figure(figsize=(10, 6), dpi=160)
ax = plt.gca()
ax.axis("off")
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)
ax.text(0.05, 0.92, title, fontsize=20, fontweight="bold", color=accent)
ax.text(
    0.05, 0.06, f"Created: {meta.get('timestamp')}", fontsize=9, color=(0.7, 0.72, 0.8)
)
plt.savefig(PNG_PATH, bbox_inches="tight")
print(f"Rendered infographic → {PNG_PATH}")
