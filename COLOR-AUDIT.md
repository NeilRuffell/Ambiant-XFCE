# Xfce-compatible Ubuntu orange and Mint green variants

## Ready in GitHub

- **Orange:** branch `xfce-panel-integration` has `Ambiant-MATE`,
  `Ambiant-MATE-Dark` and `Radiant-MATE` with their existing Xfce panel
  styles and the authentic Ubuntu Ambiance orange accent palette
  (`#f07746`).
- **Green:** branch `xfce-green` has all three themes with the original
  Mint-green palette (`#87A556`) and the corresponding Xfce panel styling.
  The green branch retains original artwork.

These are alternative **branches**, not yet six separately named themes
that can be installed side-by-side. They have no automatic switching
scripts, installer watchers, or global GTK CSS dependencies for the colour
scheme.

## Orange artwork provenance

The orange branch contains **unmodified binary PNG artwork** imported
from `ubports/ubuntu-themes`, branch `xenial`, directory
`Ambiance/gtk-3.0/assets/`. Original Ubuntu files were copied as-is into
all three GTK3 theme directories.

This includes original selected/mixed checkbox and radio artwork,
normal/high-DPI versions, hover/disabled/backdrop variants, focus
button/entry borders, toolbar-focused states, slider focus
indicators and menu checkmarks. Verified exact source byte matches
for samples from Ambiant, Ambiant-Dark and Radiant.

This replaces the earlier failed approach of recolouring images via a
user-run script. No such script or workflow remains in the orange branch.

## Palette values

The orange branch changes the primary GTK2/GTK3 selected background,
link colours, notebook accent and progress fill to follow the original
Ubuntu orange theme definitions. Semantic green success indicators
are deliberately left green.

## Remaining verification limitation

Not every image file or style rule has been pixel-audited. The orange
branch has source-verified original Ubuntu assets for the main control
states, but exhaustive visual verification on an installed Xfce
desktop remains outstanding. No claim of perfect pixel fidelity is made.
