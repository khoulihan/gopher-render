"""
A pygments theme roughly based on Monokai, but only using basic ANSI colours.
"""
from ..rendering import AnsiEscapeCodeRenderer

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "#49483e" }),
    ".c": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment
    ".err": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white", "background_colour": "red" }), # Error
    ".k": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword
    ".l": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal
    # These bright_white elements are white in monokai, but I think it will be safer to leave them
    # as the default text colour.
    #".n": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name
    #".bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Builtin.Pseudo
    #".vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Variable.Class
    #".vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Variable.Global
    #".vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Variable.Instance
    #".w": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Text.Whitespace
    #".nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Variable
    #".py": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Property
    #".nl": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Label
    #".nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Namespace
    #".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Entity
    #".nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Name.Builtin
    #".p": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white" }), # Punctuation
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Operator
    ".cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Multiline
    ".cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Preproc
    ".c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Single
    ".cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Special
    ".ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword.Constant
    ".kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword.Declaration
    ".kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Keyword.Namespace
    ".kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword.Pseudo
    ".kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword.Reserved
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Keyword.Type
    ".ld": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.Date
    ".m": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number
    ".s": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String
    ".na": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Attribute
    ".nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Class
    ".no": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Name.Constant
    ".nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Decorator
    ".ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Exception
    ".nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Function
    ".nx": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Name.Other
    ".nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Name.Tag
    ".ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Operator.Word
    ".mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number.Float
    ".mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number.Hex
    ".mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number.Integer
    ".mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number.Oct
    ".sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Backtick
    ".sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Char
    ".sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Doc
    ".s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Double
    ".se": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.String.Escape
    ".sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Heredoc
    ".si": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Interpol
    ".sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Other
    ".sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Regex
    ".s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Single
    ".ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "yellow" }), # Literal.String.Symbol
    ".il": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Literal.Number.Integer.Long
    ".gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Generic.Subheading & Diff Unified/Comment?
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Generic.Deleted & Diff Deleted
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_green" }), # Generic.Inserted & Diff Inserted
}

#.gh { } # Generic Heading & Diff Header
