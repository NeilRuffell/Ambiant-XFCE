#!/usr/bin/env python3
"""Build Xfce theme directories from Canonical's original light-themes .deb.

Usage:
  apt download light-themes
  python3 tools/import-original-light-themes.py ./light-themes_*.deb

No theme artwork is generated, altered, or recoloured. The extracted Ubuntu
PNG/SVG assets and CSS are copied byte-for-byte, then only the Xfce panel
integration stylesheet is added to the resulting theme.
"""
from pathlib import Path
import glob
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "usr/share/themes"
MAPPING = {
    "Ambiance": ("Ambiance-XFCE", "Ambiant-MATE"),
    "Radiance": ("Radiance-XFCE", "Radiant-MATE"),
}

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 tools/import-original-light-themes.py light-themes_VERSION_all.deb")
    matches = glob.glob(sys.argv[1])
    if len(matches) != 1 or not Path(matches[0]).is_file():
        raise SystemExit("Expected exactly one local light-themes .deb file")
    archive = Path(matches[0]).resolve()
    with tempfile.TemporaryDirectory(prefix="light-themes-") as tmp:
        tmp = Path(tmp)
        subprocess.run(["dpkg-deb", "-x", str(archive), str(tmp)], check=True)
        srcroot = tmp / "usr/share/themes"
        # Validate both source themes before modifying any output.
        for source in MAPPING:
            src = srcroot / source
            if not (src / "gtk-3.0/gtk-main.css").is_file():
                raise SystemExit(f"Original {source} GTK3 source not found in package")
        for source, (target, panel_source) in MAPPING.items():
            src = srcroot / source
            panel = OUTPUT / panel_source / "gtk-3.0/apps/xfce-panel.css"
            if not panel.is_file():
                raise SystemExit(f"Missing Xfce panel integration: {panel}")
            dst = OUTPUT / target
            if dst.exists():
                raise SystemExit(f"Refusing to overwrite existing {dst}; move it first")
            shutil.copytree(src, dst, symlinks=True)
            # GTK 3.24 uses gtk-3.20 when the theme supplies it.
            for gtk_dir in ("gtk-3.0", "gtk-3.20"):
                maincss = dst / gtk_dir / "gtk-main.css"
                if not maincss.is_file():
                    continue
                apps = dst / gtk_dir / "apps"
                apps.mkdir(exist_ok=True)
                shutil.copy2(panel, apps / "xfce-panel.css")
                original = maincss.read_text()
                if 'apps/xfce-panel.css' not in original:
                    maincss.write_text(original.rstrip() + '\n@import url("apps/xfce-panel.css");\n')
            # Always carry the original package's theme identity but use a unique name.
            idx = dst / "index.theme"
            if idx.is_file():
                original_index = idx.read_text()
                idx.write_text(original_index.replace("Name=" + source, "Name=" + target))
            print(f"Built {dst} from the original Canonical {source} theme")
    print("Only repository theme directories were created; no installed themes or user CSS changed.")

if __name__ == "__main__":
    main()
