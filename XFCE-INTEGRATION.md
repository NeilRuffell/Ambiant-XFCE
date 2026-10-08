# Xfce 4.20 theme-controlled panel gradients

This branch adds Xfce panel CSS to the three themes: Ambiant-MATE,
Ambiant-MATE-Dark and Radiant-MATE. The files reside within each theme at
`gtk-3.0/apps/xfce-panel.css` and use that variant's colour definitions.

## Install and enable automatic theme switching

From a clone of **this branch**:

```bash
python3 scripts/install-xfce.py
```

The installer copies all three themes into `~/.local/share/themes`,
backs up any same-named installed themes, and saves a backup of
`~/.config/gtk-3.0/gtk.css` before changing it. It installs an Xfce
session autostart entry and starts the automatic theme watcher immediately.

Select themes normally in **Settings → Appearance → Style**. No manual
CSS command is required after switching themes.

- On Ambiant-MATE, Ambiant-MATE-Dark or Radiant-MATE, the watcher
  copies **that selected theme's own** panel styles and palette definitions
  into a managed section of the GTK3 user stylesheet.
- On **any other theme**, it removes that managed section, leaving the
  rest of the user's stylesheet intact. No Ambiant gradients remain.
- The currently selected Xfce theme controls the appearance. The watcher
  checks for a change every two seconds and restarts the Xfce panel
  only when the managed CSS actually changes.
- On Xfce panel preferences, choose **None (use system style)** for
  panel background to let the GTK theme show through.
- XFWM4 window-decoration theme is independent and is not changed.

## Why a watcher is necessary

GTK3's theme CSS is loaded at priority 200, while Xfce 4.20 injects
button background CSS at application priority 600. GTK's user CSS is
priority 800. This means a stock Xfce panel will not always honor
theme-provided gradient rules for its buttons. The watcher handles the
priority mismatch while dynamically selecting the matching theme rules.

The themes themselves carry all variant-specific styling. The user-level
CSS is a **temporary mirror of the active theme**, not a permanent
Ambiant override. Unrelated GTK3 themes are left without that mirror.
No desktop-wide theme-setting changes are made by the installer.

## Previous global Ambiant override

The installer removes the **known**, previously supplied
`/* Ambiant Xfce final */` block from the end of the GTK3 user stylesheet,
following a backup. Older, unrecognized overrides are **not**
automatically removed; inspect them if you see lingering effects.

## Rollback

Remove `~/.config/autostart/ambiant-xfce-panel.desktop`, stop the running
`theme-watcher.py` process, and restore your
`gtk.css.pre-ambiant-xfce-<timestamp>` backup, or remove only the section
between `/* BEGIN AMBIANT-XFCE PANEL */` and
`/* END AMBIANT-XFCE PANEL */`. Your earlier theme directories are
preserved with a `.before-ambiant-xfce-<timestamp>` suffix.

## Testing status

GitHub source changes are committed. Full GTK3 rendered visual regression
testing on Xubuntu 26.04 has **not** been performed.
