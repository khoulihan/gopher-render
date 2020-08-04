"""
Custom Pygments theme that only uses the basic ANSI palette, and therefore should be
suitable for however the end-user has their terminal emulator configured.
"""
from ..rendering import AnsiEscapeCodeRenderer

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "red" }),
    ".c": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment
    ".err": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_white", "background_colour": "red" }), # Error
    ".k": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword
    ".l": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal
    #".n": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Operator
    #".p": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Punctuation
    ".cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Multiline
    ".cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Preproc
    ".c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Single
    ".cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_black" }), # Comment.Special
    ".ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Constant
    ".kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Declaration
    ".kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Namespace
    ".kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Pseudo
    ".kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Reserved
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Keyword.Type
    ".ld": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Date
    ".m": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number
    ".s": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String
    ".na": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Attribute
    ".nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Builtin
    ".nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan", "bold": True }), # Name.Class
    ".no": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Constant
    ".nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "cyan", "italic": True }), # Name.Decorator
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Entity
    ".ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Exception
    ".nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_cyan" }), # Name.Function
    ".nl": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Label
    ".nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Namespace
    ".nx": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Other
    ".py": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Property
    ".nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Tag
    ".nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Variable
    ".ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Operator.Word
    #".w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Text.Whitespace
    ".mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number.Float
    ".mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number.Hex
    ".mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number.Integer
    ".mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number.Oct
    ".sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Backtick
    ".sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Char
    ".sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Doc
    ".s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Double
    ".se": (AnsiEscapeCodeRenderer, { "foreground_colour": "blue" }), # Literal.String.Escape
    ".sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Heredoc
    ".si": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Interpol
    ".sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Other
    ".sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Regex
    ".s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Single
    ".ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.String.Symbol
    ".bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Builtin.Pseudo
    ".vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Variable.Class
    ".vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Variable.Global
    ".vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_magenta" }), # Name.Variable.Instance
    ".il": (AnsiEscapeCodeRenderer, { "foreground_colour": "bright_blue" }), # Literal.Number.Integer.Long
    #".gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Generic.Subheading & Diff Unified/Comment?
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "red" }), # Generic.Deleted & Diff Deleted
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "green" }), # Generic.Inserted & Diff Inserted
}

#.gh { } # Generic Heading & Diff Header
