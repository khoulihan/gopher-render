"""
Tomorrow Pygments theme, adapted for ANSI escape code rendering.
"""
from ..rendering import AnsiEscapeCodeRenderer

# TODO: This theme is intended for a light background, and needs to be adapted
# to work ok on any background

# The base colours for the theme. These are not used by default.
# To use them, an ANSI aware block renderer would be required that restores
# these colour settings after every syntax span.
background_colour = "#ffffff"
foreground_colour: "#4d4d4c"

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "#d6d6d6" }),
    ".c": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Comment
    ".err": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Error
    ".k": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8959a8" }), # Keyword
    ".l": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal
    ".n": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f" }), # Operator
    ".p": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Punctuation
    ".cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Comment.Multiline
    ".cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Comment.Preproc
    ".c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Comment.Single
    ".cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Comment.Special
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Generic.Deleted
    ".ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".gh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c", "bold": True }), # Generic.Heading
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Generic.Inserted
    ".gp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c", "bold": True }), # Generic.Prompt
    ".gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f", "bold": True }), # Generic.Subheading
    ".kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8959a8" }), # Keyword.Constant
    ".kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8959a8" }), # Keyword.Declaration
    ".kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f" }), # Keyword.Namespace
    ".kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8959a8" }), # Keyword.Pseudo
    ".kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8959a8" }), # Keyword.Reserved
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#eab700" }), # Keyword.Type
    ".ld": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.Date
    ".m": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number
    ".s": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String
    ".na": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4271ae" }), # Name.Attribute
    ".nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name.Builtin
    ".nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#eab700" }), # Name.Class
    ".no": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Constant
    ".nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f" }), # Name.Decorator
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name.Entity
    ".ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Exception
    ".nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4271ae" }), # Name.Function
    ".nl": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name.Label
    ".nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#eab700" }), # Name.Namespace
    ".nx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4271ae" }), # Name.Other
    ".py": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name.Property
    ".nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f" }), # Name.Tag
    ".nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Variable
    ".ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "#3e999f" }), # Operator.Word
    ".w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Text.Whitespace
    ".mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number.Float
    ".mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number.Hex
    ".mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number.Integer
    ".mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number.Oct
    ".sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Backtick
    ".sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Literal.String.Char
    ".sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8e908c" }), # Literal.String.Doc
    ".s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Double
    ".se": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.String.Escape
    ".sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Heredoc
    ".si": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.String.Interpol
    ".sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Other
    ".sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Regex
    ".s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Single
    ".ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "#718c00" }), # Literal.String.Symbol
    ".bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4d4d4c" }), # Name.Builtin.Pseudo
    ".vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Variable.Class
    ".vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Variable.Global
    ".vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c82829" }), # Name.Variable.Instance
    ".il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f5871f" }), # Literal.Number.Integer.Long
}
