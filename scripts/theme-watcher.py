#!/usr/bin/env python3
"""Automatically apply the selected theme's Xfce GTK3 panel CSS.

Xfce 4.20 uses application-priority CSS for buttons. Reproduce ONLY the
selected Ambiant variant's own rules in GTK user CSS (priority 800); remove
them immediately when any other theme is selected.
"""
from pathlib import Path
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

VARIANTS = ("Ambiant-MATE", "Ambiant-MATE-Dark", "Radiant-MATE")
START = "/* BEGIN AMBIANT-XFCE PANEL */"
END = "/* END AMBIANT-XFCE PANEL */"
LEGACY = "/* Ambiant Xfce final */"
CSS = Path.home() / ".config/gtk-3.0/gtk.css"
CACHE = Path.home() / ".local/share/ambiant-xfce"
THEMES = Path.home() / ".local/share/themes"

def selected_theme():
    p = subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName"],
                       capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None

def theme_css(variant):
    root = THEMES / variant / "gtk-3.0"
    main = (root / "gtk-main.css").read_text()
    panel = (root / "apps/xfce-panel.css").read_text()
    colors = {}
    for key in ("fg_color", "dark_bg_color", "dark_fg_color"):
        match = re.search(r"^@define-color\s+" + key + r"\s+([^;]+);", main, re.M)
        if not match:
            raise ValueError(f"Missing {key} in {variant}")
        colors[key] = match.group(1).strip()
    fg = colors["dark_fg_color"]
    if fg.startswith("@"):
        alias = fg[1:]
        if alias not in colors:
            raise ValueError(f"Unresolved theme color {fg} in {variant}")
        fg = colors[alias]
    definitions = f"@define-color dark_bg_color {colors['dark_bg_color']};\n"
    definitions += f"@define-color dark_fg_color {fg};\n"
    return definitions + panel

def remove_managed(existing):
    if (START in existing) != (END in existing):
        raise ValueError("Unbalanced managed CSS; refusing to alter user file")
    if START in existing:
        existing = existing[:existing.index(START)] + existing[existing.index(END) + len(END):]
    return existing

def apply(variant, clean_legacy=False):
    CSS.parent.mkdir(parents=True, exist_ok=True)
    before = CSS.read_text() if CSS.exists() else ""
    base = remove_managed(before)
    if clean_legacy and LEGACY in base:
        # Earlier provided setup script appended this block at the end.
        base = base[:base.index(LEGACY)].rstrip()
    if variant in VARIANTS:
        payload = theme_css(variant)
        result = base.rstrip() + "\n\n" + START + "\n" + payload + "\n" + END + "\n"
    else:
        result = base.rstrip() + ("\n" if base.strip() else "")
    if result != before:
        tmp = CSS.with_name(CSS.name + ".ambiant-xfce.tmp")
        tmp.write_text(result)
        os.replace(tmp, CSS)
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Synchronize once")
    parser.add_argument("--clean-legacy", action="store_true",
                        help="Remove the known legacy Ambiant Xfce final block")
    args = parser.parse_args()
    previous = object()
    while True:
        variant = selected_theme()
        if variant is not None and (variant != previous or args.once):
            try:
                changed = apply(variant, args.clean_legacy)
            except (OSError, ValueError) as exc:
                print(f"Ambiant-XFCE: {exc}", file=sys.stderr)
                if args.once:
                    return 1
            else:
                previous = variant
                if changed:
                    subprocess.run(["xfce4-panel", "--restart"], check=False,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Theme:", variant, "Panel CSS:", "updated" if changed else "unchanged",
                      flush=True)
            args.clean_legacy = False
        if args.once:
            return 0
        time.sleep(2)

if __name__ == "__main__":
    sys.exit(main())
