# Accent palette audit (Xfce integration branch)

## Colour scheme

The three installed appearance variants share Ubuntu orange selection, focus,
hyperlink and progress accents through their GTK2/GTK3 theme files:

- `Ambiant-MATE`: light applications, dark Ambiant panel, orange accent
- `Ambiant-MATE-Dark`: dark applications, dark Ambiant panel, orange accent
- `Radiant-MATE`: light Radiance applications/panel, orange accent

The theme's existing `selected_fg_color` is retained per variant so
foreground contrast follows its established dark/light palette.

Orange selection is `#f07746`, the colour applied in the user's prior
local GTK palette edit. `#dd4814` is a legacy Ubuntu orange reference;
this work does not claim pixel-for-pixel recreation of a specific release.

## Confirmed replacement of Mint-specific styling

In **each** theme:

- `gtk-3.0/gtk-main.css`: `selected_bg_color` from Mint
  `#87A556` to orange `#f07746`.
- `gtk-3.0/gtk-main.css`: notebook strip `core_color_a` from
  hard-coded muted green `#B9C0A9` to a tint derived from
  `@selected_bg_color` and existing `@core_color_b`.
- `gtk-3.0/gtk-main.css`: progress bar no longer mixes in a literal
  CSS `green` colour. The selected accent determines its hue.
- `gtk-3.0/gtk-widgets.css`: hard-coded Mint-green hyperlinks
  `#a7bb85` replaced with `#f07746`.
- `gtk-2.0/gtkrc`: selection and hyperlink palette values updated to orange.
- Radiant's existing `link_color #A7BB85` has been switched to
  `@selected_bg_color`.

GTK3 `focus_color`, `focus_bg_color`, `focus_color_dialog`,
selected borders, tabs, scrollbars and other components already derive
from `@selected_bg_color`, and therefore follow orange automatically.

## Green is not always Mint styling

`success_color #4e9a06` is kept as a semantic success indication:
success states should not be mistaken for orange-accent controls.
Other fixed warning/error and neutral interface colours remain unchanged.

## Green variant

The original, unmodified green palette remains in the fork's **master**
branch, separate from this orange integration branch. It is not offered
as an additional installed GTK theme variant with a distinct theme name.

## Audit limitations

The source-level audit examined the GTK2 `gtkrc`, GTK3 `gtk-main.css`,
`gtk-widgets.css`, the GTK3 widget asset mapping stylesheet and the
GTK3 MATE application stylesheet for all three variants. The complete
repository's image assets (PNG/SVG), additional application stylesheets,
window-manager (XFWM4) assets and GTK2 pixmaps have **not** all been
exhaustively enumerated or visually inspected. Claims that *all* green
pixels were removed or that this reproduces original Ubuntu Ambiance
exactly would be unsupported. Visual regression testing is needed.

No global GTK settings, panel settings, watcher or installer is needed
for these colour edits; they live within theme files.
