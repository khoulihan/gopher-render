"""
Github Pygments theme, adapted for ANSI escape code rendering.
"""
from ..rendering import AnsiEscapeCodeRenderer

# TODO: This theme is intended for a light background, and needs to be adapted
# to work ok on any background

# The base colours for the theme. These are not used by default.
# To use them, an ANSI aware block renderer would be required that restores
# these colour settings after every syntax span.
background_colour = "#f8f8f8"
# There is actually no foreground colour specified by this theme.
foreground_colour: "#C1C2C3"

# GitHub style for Pygments syntax highlighter, for use with Jekyll
# Courtesy of GitHub.com

# HTML Colours
_TEAL = "#008080"
_PURPLE = "#800080"
_NAVY = "#000080"

renderers = {
    ".highlight .c": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999988", "italic": True }),
    ".highlight .err": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a61717", "background-colour": "#e3d2d2", }),
    ".highlight .k": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .o": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999988", "italic": True }),
    ".highlight .cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999999", "bold": True }),
    ".highlight .c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999988", "italic": True }),
    ".highlight .cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999999", "bold": True, "italic": True }),
    ".highlight .gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#000000", "background-colour": "#ffdddd", }),
    ".highlight .gd .x": (AnsiEscapeCodeRenderer, { "foreground_colour": "#000000", "background-colour": "#ffaaaa", }),
    ".highlight .ge": (AnsiEscapeCodeRenderer, { "italic": True }),
    ".highlight .gr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000", }),
    ".highlight .gh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999999", }),
    ".highlight .gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#000000", "background-colour": "#ddffdd", }),
    ".highlight .gi .x": (AnsiEscapeCodeRenderer, { "foreground_colour": "#000000", "background-colour": "#aaffaa", }),
    ".highlight .go": (AnsiEscapeCodeRenderer, { "foreground_colour": "#888888", }),
    ".highlight .gp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#555555", }),
    ".highlight .gs": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#800080", "bold": True }),
    ".highlight .gt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000", }),
    ".highlight .kc": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .kd": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .kn": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .kp": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .kr": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#445588", "bold": True }),
    ".highlight .m": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .s": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .n": (AnsiEscapeCodeRenderer, { "foreground_colour": "#333333", }),
    ".highlight .na": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0086b3", }),
    ".highlight .nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#445588", "bold": True }),
    ".highlight .no": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .ni": (AnsiEscapeCodeRenderer, { "foreground_colour": _PURPLE }),
    ".highlight .ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "#990000", "bold": True }),
    ".highlight .nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#990000", "bold": True }),
    ".highlight .nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#555555", }),
    ".highlight .nt": (AnsiEscapeCodeRenderer, { "foreground_colour": _NAVY }),
    ".highlight .nv": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .ow": (AnsiEscapeCodeRenderer, { "bold": True }),
    ".highlight .w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#bbbbbb", }),
    ".highlight .mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .se": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .si": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009926", }),
    ".highlight .s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#dd1144", }),
    ".highlight .ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "#990073", }),
    ".highlight .bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999999", }),
    ".highlight .vc": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .vg": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .vi": (AnsiEscapeCodeRenderer, { "foreground_colour": _TEAL }),
    ".highlight .il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999", }),
    ".highlight .gc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#999", "background-colour": "#EAF2F5", }),
}
