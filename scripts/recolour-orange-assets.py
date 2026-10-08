#!/usr/bin/env python3
"""Audit and convert Mint-green UI assets in Ambiant/Radiant orange variants.

Edits only files under usr/share/themes; skips semantic success/status assets.
Use --check to audit without modifying assets.
"""
from pathlib import Path
import colorsys
import re
import sys
from collections import Counter
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "usr/share/themes"
THEMES = ("Ambiant-MATE", "Ambiant-MATE-Dark", "Radiant-MATE")
# Names denote theme UI accent surfaces, not pictograms or semantic status.
UI = ("check", "radio", "button", "focused", "focus", "slider", "scale",
      "switch", "progress", "selected", "active", "notebook", "tab",
      "entry", "combobox", "spin", "scrollbar", "menu", "arrow")
# Hue range covers desaturated grey-green Mint highlights through vivid green.
# Keep neutral greys and dark borders untouched.
ORANGE_HUE = 19 / 360

def convert(rgb):
    r, g, b = (x / 255 for x in rgb)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # Mint green: yellow-green to blue-green, excluding orange/neutral.
    if 47/360 <= h <= 167/360 and s >= .11 and v >= .18 and g > r * 1.045:
        # Keep the original value/saturation and hence all gradients/shadows.
        x = colorsys.hsv_to_rgb(ORANGE_HUE, s, v)
        return tuple(round(z * 255) for z in x)
    return rgb

def process_png(path, check):
    with Image.open(path) as original:
        img = original.convert("RGBA")
    pixels = img.load()
    count = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if not a:
                continue
            repl = convert((r, g, b))
            if repl != (r, g, b):
                count += 1
                if not check:
                    pixels[x, y] = (*repl, a)
    if count and not check:
        img.save(path)
    return count

RGBHEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
def process_svg(path, check):
    source = path.read_text()
    changed = 0
    def repl(match):
        nonlocal changed
        txt = match.group()
        digits = txt[1:]
        if len(digits) == 3:
            rgb = tuple(int(v*2, 16) for v in digits)
        else:
            rgb = tuple(int(digits[i:i+2], 16) for i in (0, 2, 4))
        new = convert(rgb)
        if new != rgb:
            changed += 1
            return "#" + "".join(f"{v:02x}" for v in new)
        return txt
    result = RGBHEX.sub(repl, source)
    if changed and not check:
        path.write_text(result)
    return changed

def main():
    check = "--check" in sys.argv
    totals = Counter()
    for theme in THEMES:
        root = ROOT / theme
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in (".png", ".svg"):
                continue
            lower = path.name.lower()
            if not any(word in lower for word in UI):
                # Report other green images for manual classification, but do not recolour.
                continue
            try:
                count = process_png(path, check) if path.suffix.lower() == ".png" else process_svg(path, check)
            except (OSError, ValueError) as exc:
                raise SystemExit(f"Cannot inspect {path}: {exc}")
            if count:
                print(f"{theme}: {path.relative_to(root)} ({count} recoloured pixels/values)")
                totals[theme] += count
    for theme in THEMES:
        print(f"{theme} modified green pixel/value count: {totals[theme]}")
    print("Mode:", "audit only" if check else "updated theme image files")

if __name__ == "__main__":
    main()
