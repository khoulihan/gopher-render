"""
Darkly Pygments theme, adapted for ANSI escape code rendering.
"""
from ..rendering import AnsiEscapeCodeRenderer

# TODO: This theme is intended for a dark background, and needs to be adapted
# to work ok on any background

# The base colours for the theme. These are not used by default.
# To use them, an ANSI aware block renderer would be required that restores
# these colour settings after every syntax span.
background_colour = "#343642"
foreground_colour: "#C1C2C3"

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "#ffc" }),
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#2e3436", "background_colour": "#0e1416" }),
    ".gr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#eeeeec", "background_colour": "#c00" }),
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#babdb6", "background_colour": "#1f2b2d" }),
    ".go": (AnsiEscapeCodeRenderer, { "foreground_colour": "#2c3032", "background_colour": "#2c3032" }),
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e3e7df", }),
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "#888a85", }),
    ".c,.cm,.c1,.cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8D9684", }),
    ".err,.g,.l,.n,.x,.p,.ge,.gp,.gs,.gt,.ld,.s,.nc,.nd,.ne,.nl,.nn,.nx,.py,.ow,.w,.sb,.sc,.sd,.s2,.se,.sh,.si,.sx,.sr,.s1,.ss,.bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#C1C2C3", }),
    ".k,.kc,.kd,.kn,.kp,.kr,.nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#729fcf", }),
    ".cp,.gh,.gu,.na,.nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#E9A94B", }),
    ".m,.nb,.no,.mf,.mh,.mi,.mo,.il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8ae234", }),
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "#989DAA", }),
    ".nv,.vc,.vg,.vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#fff", }),
}
