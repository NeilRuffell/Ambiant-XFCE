# Xfce 4.20 panel compatibility

This branch adds native GTK3 Xfce panel selectors to all three existing themes:

- Ambiant-MATE
- Ambiant-MATE-Dark
- Radiant-MATE

The new `gtk-3.0/apps/xfce-panel.css` file in each theme is imported from
`gtk-main.css`. Each file uses the current theme's own `@dark_bg_color`,
`@dark_fg_color`, shade factors, borders, and menu states. No external
theme design is used.

## Why there is a second activation step

Xfce 4.20 injects `.xfce4-panel.background button { background: transparent; }`
at GTK's application priority (600), which can override declarations from
a GTK theme (priority 200). GTK's user CSS has priority 800.

After cloning this repository on Xubuntu, copy the desired theme directory
from `usr/share/themes/` into `~/.local/share/themes/`. Then run:

```sh
python3 scripts/apply-xfce-panel.py Ambiant-MATE
xfconf-query -c xsettings -p /Net/ThemeName -s Ambiant-MATE
xfce4-panel --restart
```

Instead of `Ambiant-MATE`, choose `Ambiant-MATE-Dark` or `Radiant-MATE`
in **both** the helper command and the Appearance theme setting.

The helper preserves other GTK user CSS, backs it up, and replaces only its
own marked block on subsequent runs. **It does not remove earlier unrelated
panel overrides.** An older override in `~/.config/gtk-3.0/gtk.css` can
still conflict and must be reviewed separately.

To undo the helper's changes, remove only the block between
`/* BEGIN AMBIANT-XFCE PANEL */` and `/* END AMBIANT-XFCE PANEL */`
from the GTK user stylesheet, or restore the timestamped backup.

For a theme-provided panel background, set Xfce Panel Preferences →
Appearance → Background to **None (use system style)**.

The helper must be re-run when changing themes because GTK's user-level
override does not automatically switch palettes.

## Validation

The source adaptations are committed, but rendered visual fidelity on an
actual Xubuntu 26.04/Xfce 4.20 desktop has not been verified. Keep the
changes on this working branch until testing confirms panel, applet and
tasklist states.
