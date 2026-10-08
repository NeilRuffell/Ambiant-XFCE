# Building authentic orange Ambiance/Radiance themes for Xfce

**Source artwork:** Canonical/Ubuntu `light-themes` Debian package,
which contains the original Ambiance and Radiance CSS and PNG/SVG files.
No artwork is synthesized or colourized by this build.

From the `xfce-panel-integration` branch:

```bash
sudo apt update
apt download light-themes
python3 tools/import-original-light-themes.py ./light-themes_*.deb
```

This generates **only** theme directories, under
`usr/share/themes/Ambiance-XFCE` and
`usr/share/themes/Radiance-XFCE`, within this repository.
It copies Canonical's original theme directories, preserves every
original image asset, and adds the fork's Xfce GTK3 panel stylesheet
as a separate import. It does **not** write `~/.config/gtk-3.0/gtk.css`,
install background services, or touch desktop settings.

Test without overwriting existing themes:

```bash
cp -a usr/share/themes/Ambiance-XFCE ~/.local/share/themes/
cp -a usr/share/themes/Radiance-XFCE ~/.local/share/themes/
```

Choose the themes under Xfce Appearance. Set the panel background
to **use the system style** if previously configured otherwise.

**Important:** This builder is committed, but generated theme
directories and original assets have **not** been committed to GitHub.
Run the builder against the actual Canonical package and inspect the
rendered theme before publishing the generated binary assets. The
existing green originals remain in the `green-original` branch.

This imports a contemporary Ubuntu `light-themes` package, not a
guaranteed pixel-perfect Ubuntu 10.10 theme. GTK3 and Xfce panel
differences may need theme-file adjustments after testing.
