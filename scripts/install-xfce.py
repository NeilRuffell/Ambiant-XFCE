#!/usr/bin/env python3
"""Install three Ambiant themes and automatic Xfce panel theme switching."""
from pathlib import Path
from datetime import datetime
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
DEST = HOME / ".local/share/themes"
RUNTIME = HOME / ".local/share/ambiant-xfce"
AUTOSTART = HOME / ".config/autostart/ambiant-xfce-panel.desktop"
VARIANTS = ("Ambiant-MATE", "Ambiant-MATE-Dark", "Radiant-MATE")

def main():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    DEST.mkdir(parents=True, exist_ok=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    for name in VARIANTS:
        src = ROOT / "usr/share/themes" / name
        dst = DEST / name
        if not (src / "gtk-3.0/apps/xfce-panel.css").is_file():
            raise SystemExit("Missing Xfce theme CSS for " + name)
        if dst.exists() or dst.is_symlink():
            back = DEST / (name + ".before-ambiant-xfce-" + stamp)
            dst.rename(back)
            print("Saved old theme:", back)
        shutil.copytree(src, dst, symlinks=True)
        print("Installed:", dst)
    script = RUNTIME / "theme-watcher.py"
    shutil.copy2(ROOT / "scripts/theme-watcher.py", script)
    AUTOSTART.parent.mkdir(parents=True, exist_ok=True)
    AUTOSTART.write_text(
        "[Desktop Entry]\nType=Application\nName=Ambiant XFCE theme sync\n"
        "Comment=Use panel styling from the active GTK theme\n"
        f"Exec=/usr/bin/python3 {script}\n"
        "Terminal=false\nX-GNOME-Autostart-enabled=true\n"
    )
    user_css = HOME / ".config/gtk-3.0/gtk.css"
    if user_css.exists():
        backup = user_css.with_name("gtk.css.pre-ambiant-xfce-" + stamp)
        shutil.copy2(user_css, backup)
        print("GTK CSS backup:", backup)
    subprocess.run([sys.executable, str(script), "--once", "--clean-legacy"], check=True)
    subprocess.Popen([sys.executable, str(script)], start_new_session=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    print("Installed autostart and started automatic theme synchronizer.")
    print("Switch themes using Xfce Appearance; other themes remove Ambiant's managed CSS.")

if __name__ == "__main__":
    main()
