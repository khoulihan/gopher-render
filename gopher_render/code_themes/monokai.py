"""
Monokai Pygments theme, adapted for ANSI escape code rendering.
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
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "#49483e" }),
    ".c": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Comment
    ".err": (AnsiEscapeCodeRenderer, { "foreground_colour": "#960050", "background_colour": "#1e0010" }), # Error
    ".k": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword
    ".l": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal
    ".n": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f92672" }), # Operator
    ".p": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Punctuation
    ".cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Comment.Multiline
    ".cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Comment.Preproc
    ".c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Comment.Single
    ".cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Comment.Special
    ".ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword.Constant
    ".kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword.Declaration
    ".kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f92672" }), # Keyword.Namespace
    ".kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword.Pseudo
    ".kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword.Reserved
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Keyword.Type
    ".ld": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.Date
    ".m": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number
    ".s": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String
    ".na": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Attribute
    ".nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Builtin
    ".nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Class
    ".no": (AnsiEscapeCodeRenderer, { "foreground_colour": "#66d9ef" }), # Name.Constant
    ".nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Decorator
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Entity
    ".ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Exception
    ".nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Function
    ".nl": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Label
    ".nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Namespace
    ".nx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Name.Other
    ".py": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Property
    ".nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f92672" }), # Name.Tag
    ".nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Variable
    ".ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f92672" }), # Operator.Word
    ".w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Text.Whitespace
    ".mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number.Float
    ".mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number.Hex
    ".mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number.Integer
    ".mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number.Oct
    ".sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Backtick
    ".sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Char
    ".sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Doc
    ".s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Double
    ".se": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.String.Escape
    ".sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Heredoc
    ".si": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Interpol
    ".sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Other
    ".sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Regex
    ".s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Single
    ".ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "#e6db74" }), # Literal.String.Symbol
    ".bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Builtin.Pseudo
    ".vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Variable.Class
    ".vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Variable.Global
    ".vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f8f8f2" }), # Name.Variable.Instance
    ".il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#ae81ff" }), # Literal.Number.Integer.Long
    ".gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#75715e" }), # Generic.Subheading & Diff Unified/Comment?
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f92672" }), # Generic.Deleted & Diff Deleted
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#a6e22e" }), # Generic.Inserted & Diff Inserted
}

#.gh { } # Generic Heading & Diff Header
