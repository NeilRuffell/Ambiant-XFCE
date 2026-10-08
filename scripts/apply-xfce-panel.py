#!/usr/bin/env python3
"""Activate existing Ambiant GTK3 panel styling at user priority for Xfce 4.20."""
from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

VARIANTS = ("Ambiant-MATE", "Ambiant-MATE-Dark", "Radiant-MATE")
START = "/* BEGIN AMBIANT-XFCE PANEL */"
END = "/* END AMBIANT-XFCE PANEL */"

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in VARIANTS:
        raise SystemExit("Usage: python3 scripts/apply-xfce-panel.py " + " | ".join(VARIANTS))
    variant = sys.argv[1]
    source = Path(__file__).resolve().parents[1] / "usr/share/themes" / variant / "gtk-3.0"
    theme_css = (source / "gtk-main.css").read_text()
    panel_css = (source / "apps/xfce-panel.css").read_text()
    colors = {}
    for key in ("fg_color", "dark_bg_color", "dark_fg_color"):
        match = re.search(r"^@define-color\s+" + key + r"\s+([^;]+);", theme_css, re.M)
        if not match:
            raise SystemExit(f"Missing {key} in {variant}; no changes made")
        colors[key] = match.group(1).strip()
    if colors["dark_fg_color"].startswith("@"):
        colors["dark_fg_color"] = colors[colors["dark_fg_color"][1:]]
    definitions = "".join(f"@define-color {key} {colors[key]};\n"
                          for key in ("dark_bg_color", "dark_fg_color"))
    destination = Path.home() / ".config/gtk-3.0/gtk.css"
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = destination.read_text() if destination.exists() else ""
    if (START in existing) != (END in existing):
        raise SystemExit("Unbalanced managed section; no changes made")
    if START in existing:
        existing = existing[:existing.index(START)] + existing[existing.index(END) + len(END):]
    if destination.exists():
        backup = destination.with_name("gtk.css.backup-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        shutil.copy2(destination, backup)
        print("Backup:", backup)
    block = START + "\n" + definitions + panel_css + "\n" + END
    destination.write_text(existing.rstrip() + "\n\n" + block + "\n")
    print("Applied", variant, "Xfce rules to", destination)
    print("Restart the Xfce panel after selecting the matching appearance theme.")
    print("Previously added, unmarked GTK panel overrides are not removed.")

if __name__ == "__main__":
    main()
