"""Light/dark theming for the whole application.

ttk widgets are themed application-wide through a single ``ttk.Style`` (so every
ttk widget in every window updates at once), while plain ``tkinter`` widgets,
menus and window backgrounds are recolored by walking the widget tree.
"""

from tkinter import TclError
from tkinter import ttk

# Palettes for each theme. "light" mirrors the system defaults closely enough
# that the original look is preserved when dark mode is off.
PALETTES = {
    "light": {
        "bg": "#f0f0f0",
        "surface": "#ffffff",
        "fg": "#000000",
        "select_bg": "#0078d7",
        "select_fg": "#ffffff",
        "entry_bg": "#ffffff",
        "disabled_fg": "#a3a3a3",
        "trough": "#e6e6e6",
    },
    "dark": {
        "bg": "#1e1e1e",
        "surface": "#2d2d2d",
        "fg": "#e6e6e6",
        "select_bg": "#094771",
        "select_fg": "#ffffff",
        "entry_bg": "#3c3c3c",
        "disabled_fg": "#6d6d6d",
        "trough": "#3c3c3c",
    },
}

# The ttk theme to use for dark mode. "clam" honors color options reliably,
# unlike the native Windows themes.
_DARK_TTK_THEME = "clam"

# Remembered so light mode can restore the original native ttk theme.
_original_ttk_theme = None

# Color options we try to set on plain tk widgets. Each is applied only if the
# widget actually supports it (checked against ``widget.keys()``).
_PLAIN_OPTIONS = {
    "background": "bg",
    "foreground": "fg",
    "activebackground": "select_bg",
    "activeforeground": "select_fg",
    "disabledforeground": "disabled_fg",
    "insertbackground": "fg",
    "selectcolor": "entry_bg",
    "highlightbackground": "bg",
    "highlightcolor": "bg",
    "troughcolor": "trough",
    "readonlybackground": "entry_bg",
}

# Widgets that hold editable text look better with the dedicated entry color.
_ENTRY_CLASSES = {"Entry", "Spinbox", "TCombobox", "Text", "Listbox"}


def get_palette(dark):
    return PALETTES["dark"] if dark else PALETTES["light"]


def _configure_ttk_style(dark, palette):
    """Configure the application-wide ttk style for the given theme."""
    global _original_ttk_theme
    style = ttk.Style()

    if _original_ttk_theme is None:
        _original_ttk_theme = style.theme_use()

    if not dark:
        # Restore the native look untouched.
        style.theme_use(_original_ttk_theme)
        return

    style.theme_use(_DARK_TTK_THEME)
    bg, surface, fg = palette["bg"], palette["surface"], palette["fg"]
    select_bg, select_fg = palette["select_bg"], palette["select_fg"]
    entry_bg, disabled_fg = palette["entry_bg"], palette["disabled_fg"]

    style.configure(".", background=bg, foreground=fg, fieldbackground=entry_bg,
                    bordercolor=surface, troughcolor=palette["trough"])
    style.map(".", foreground=[("disabled", disabled_fg)])

    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TLabelframe", background=bg, foreground=fg)
    style.configure("TLabelframe.Label", background=bg, foreground=fg)

    style.configure("TButton", background=surface, foreground=fg)
    style.map("TButton",
              background=[("active", select_bg), ("pressed", select_bg)],
              foreground=[("active", select_fg), ("disabled", disabled_fg)])

    style.configure("TMenubutton", background=surface, foreground=fg)
    style.map("TMenubutton", background=[("active", select_bg)],
              foreground=[("active", select_fg)])

    style.configure("TCheckbutton", background=bg, foreground=fg)
    style.map("TCheckbutton", background=[("active", bg)],
              foreground=[("disabled", disabled_fg)])

    for widget in ("TEntry", "TSpinbox", "TCombobox"):
        style.configure(widget, fieldbackground=entry_bg, foreground=fg,
                        background=surface, insertcolor=fg, arrowcolor=fg)


def _restore_or_store(widget, dark):
    """Apply palette colors to a single plain tk widget, remembering originals
    so light mode can restore the widget's native appearance."""
    palette = get_palette(dark)
    available = set(widget.keys())
    cls = widget.winfo_class()

    if not dark:
        original = getattr(widget, "_theme_orig", None)
        if original:
            for option, value in original.items():
                try:
                    widget.configure(**{option: value})
                except TclError:
                    pass
        return

    if not hasattr(widget, "_theme_orig"):
        widget._theme_orig = {}
        for option in _PLAIN_OPTIONS:
            if option in available:
                try:
                    widget._theme_orig[option] = widget.cget(option)
                except TclError:
                    pass

    for option, palette_key in _PLAIN_OPTIONS.items():
        if option not in available:
            continue
        if option == "background" and cls in _ENTRY_CLASSES:
            value = palette["entry_bg"]
        else:
            value = palette[palette_key]
        try:
            widget.configure(**{option: value})
        except TclError:
            pass


def _recolor_tree(widget, dark):
    """Recolor a widget and all of its descendants.

    ttk widgets are skipped (they are handled by the global style); only plain
    tk widgets, menus and toplevels are touched here.
    """
    if not isinstance(widget, ttk.Widget):
        _restore_or_store(widget, dark)
    for child in widget.winfo_children():
        _recolor_tree(child, dark)


def apply_theme(window, dark):
    """Apply the light or dark theme to ``window`` and everything inside it.

    Safe to call repeatedly and on any Tk/Toplevel window.
    """
    palette = get_palette(dark)
    _configure_ttk_style(dark, palette)

    # Recolors the window itself (its background, behind the ttk frames) and
    # every plain tk descendant.
    _recolor_tree(window, dark)

    # The menu bar is attached via ``config(menu=...)`` and is reachable through
    # the widget tree, but make sure the menubar set on this window is covered.
    try:
        menu_name = window["menu"]
        if menu_name:
            _recolor_tree(window.nametowidget(menu_name), dark)
    except (TclError, KeyError):
        pass
