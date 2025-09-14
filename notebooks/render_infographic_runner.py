#!/usr/bin/env python3
"""
Lightweight Day-3 infographic renderer used by CI.
Behavior:
 - If docs/day3_infographic.json exists, render docs/day3_infographic.png.
 - If JSON is missing (typical on PRs), create a SMOKE placeholder PNG.
 - Always write a PNG so the artifact step can upload something.
Exit code:
 - 0 on success/SMOKE success; non-zero only if a real render attempt failed.
"""
from __future__ import annotations
import os, json, sys, datetime as dt
ROOT = os.getcwd()
JSON_PATH = os.environ.get("INFO_JSON", os.path.join(ROOT, "docs", "day3_infographic.json"))
PNG_PATH  = os.environ.get("INFO_PNG",  os.path.join(ROOT, "docs", "day3_infographic.png"))
os.makedirs(os.path.dirname(PNG_PATH), exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False
try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

def smoke_png(path: str, title="SMOKE: Missing JSON", subtitle=""):
    W,H = 1280,720
    if HAVE_PIL:
        img = Image.new("RGB",(W,H),(18,18,18))
        d = ImageDraw.Draw(img)
        try:
            big = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            small= ImageFont.truetype("DejaVuSans.ttf", 18)
        except Exception:
            big = small = ImageFont.load_default()
        d.text((40,40), title, fill=(235,235,235), font=big)
        if subtitle:
            d.text((40,110), subtitle, fill=(180,180,180), font=small)
        img.save(path); print(f"[runner] SMOKE PNG -> {path}"); return
    if HAVE_MPL:
        fig = plt.figure(figsize=(10,6), dpi=160); ax=plt.gca(); ax.axis("off")
        fig.patch.set_facecolor((0.07,0.07,0.07)); ax.set_facecolor((0.07,0.07,0.07))
        ax.text(0.05,0.85,title,fontsize=24,color="white",fontweight="bold")
        if subtitle: ax.text(0.05,0.70,subtitle,fontsize=12,color=(0.8,0.8,0.8))
        plt.savefig(path,bbox_inches="tight"); plt.close(fig)
        print(f"[runner] SMOKE PNG (mpl) -> {path}"); return
    open(path,"wb").close(); print(f"[runner] Empty file -> {path}")

def render(json_path: str, png_path: str):
    meta = json.load(open(json_path,"r",encoding="utf-8"))
    if meta.get("timestamp") == "{{AUTO}}":
        meta["timestamp"] = dt.datetime.utcnow().isoformat(timespec="seconds")+"Z"
    title = meta.get("title","Entropy Sieve — Day 3 Snapshot")
    subtitle = meta.get("subtitle","")
    m = meta.get("metrics",{}) or {}
    notes = meta.get("notes",[]) or []
    palette = (meta.get("visuals",{}) or {}).get("palette",[]) or []
    accent = palette[0] if palette else "#cddc39"
    bg     = palette[1] if len(palette)>1 else "#111418"
    lines = [
        f"NP-wall rate: {m.get('np_wall_pct',0):.2f}%",
        f"ΔΦ thresholds: NP={m.get('np_threshold','?')}  P={m.get('p_threshold','?')}",
        f"Samples × length: {m.get('samples','?')} × {m.get('trace_len','?')}",
        f"Traces: {m.get('traces','?')}",
    ]
    if HAVE_MPL:
        fig = plt.figure(figsize=(10,6), dpi=160); ax=plt.gca(); ax.axis("off")
        fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
        ax.text(0.05,0.90,title,fontsize=20,color=accent,fontweight="bold")
        ax.text(0.05,0.85,subtitle,fontsize=12,color=(0.8,0.85,0.9))
        y=0.75
        for s in lines: ax.text(0.05,y,s,fontsize=14,color="white"); y-=0.06
        ax.text(0.05,y-0.02,"Notes:",fontsize=14,color=accent,fontweight="bold"); y-=0.10
        for n in notes: ax.text(0.05,y,"• "+str(n),fontsize=12,color="white"); y-=0.05
        ax.text(0.05,0.06,f"Created: {meta.get('timestamp')}",fontsize=9,color=(0.7,0.72,0.8))
        plt.savefig(png_path,bbox_inches="tight"); plt.close(fig)
        print(f"[runner] Rendered PNG -> {png_path}")
        return
    # Fallback: smoke with packed text
    smoke_png(png_path, title=title, subtitle=subtitle)

def main():
    if not os.path.exists(JSON_PATH):
        info = f"Expected JSON: {JSON_PATH}"
        smoke_png(PNG_PATH, subtitle=info)
        return 0
    try:
        render(JSON_PATH, PNG_PATH)
        return 0
    except Exception as e:
        print(f"[runner] ERROR: {e}", file=sys.stderr)
        smoke_png(PNG_PATH, title="SMOKE: Render failed", subtitle=str(e))
        return 1

if __name__ == "__main__":
    sys.exit(main())
