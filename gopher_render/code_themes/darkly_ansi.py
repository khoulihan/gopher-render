"""
A pygmnts theme roughly based on Darkly, but only using basic ANSI colours.
"""
from ..rendering import AnsiEscapeCodeRenderer

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "bright_yellow" }),
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "cyan", "background_colour": "black" }),
    ".gr": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white", "background_colour": "bright_red" }),
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "white", "background_colour": "black" }),
    # The foreground and background were both the same for this one...
    ".go": (AnsiEscapeCodeRenderer, { "foreground_colour": "white", "background_colour": "cyan" }),
    #".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e3e7df", }), # White - default colour
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow", }),
    ".c,.cm,.c1,.cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow", }),
    # White - default colour
    #".err,.g,.l,.n,.x,.p,.ge,.gp,.gs,.gt,.ld,.s,.nc,.nd,.ne,.nl,.nn,.nx,.py,.ow,.w,.sb,.sc,.sd,.s2,.se,.sh,.si,.sx,.sr,.s1,.ss,.bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan", }),
    ".k,.kc,.kd,.kn,.kp,.kr,.nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "blue", }),
    ".cp,.gh,.gu,.na,.nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_red", }),
    ".m,.nb,.no,.mf,.mh,.mi,.mo,.il": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green", }),
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black", }),
    #".nv,.vc,.vg,.vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#fff", }), # White - default colour
}
