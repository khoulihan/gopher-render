"""
Tomorrow Night Pygments theme, adapted for ANSI escape code rendering.
"""
from ..rendering import AnsiEscapeCodeRenderer

# TODO: This theme is intended for a dark background, and needs to be adapted
# to work ok on any background

# The base colours for the theme. These are not used by default.
# To use them, an ANSI aware block renderer would be required that restores
# these colour settings after every syntax span.
background_colour = "#1d1f21"
foreground_colour: "#c5c8c6"

renderers = {
    ".hll": (AnsiEscapeCodeRenderer, { "background_colour": "#373b41" }),
    ".c": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Comment
    ".err": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Error
    ".k": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b294bb" }), # Keyword
    ".l": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal
    ".n": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name
    ".o": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7" }), # Operator
    ".p": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Punctuation
    ".cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Comment.Multiline
    ".cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Comment.Preproc
    ".c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Comment.Single
    ".cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Comment.Special
    ".gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Generic.Deleted
    ".ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".gh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6", "bold": True }), # Generic.Heading
    ".gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Generic.Inserted
    ".gp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896", "bold": True }), # Generic.Prompt
    ".gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7", "bold": True }), # Generic.Subheading
    ".kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b294bb" }), # Keyword.Constant
    ".kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b294bb" }), # Keyword.Declaration
    ".kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7" }), # Keyword.Namespace
    ".kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b294bb" }), # Keyword.Pseudo
    ".kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b294bb" }), # Keyword.Reserved
    ".kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f0c674" }), # Keyword.Type
    ".ld": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.Date
    ".m": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number
    ".s": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String
    ".na": (AnsiEscapeCodeRenderer, { "foreground_colour": "#81a2be" }), # Name.Attribute
    ".nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name.Builtin
    ".nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f0c674" }), # Name.Class
    ".no": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Constant
    ".nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7" }), # Name.Decorator
    ".ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name.Entity
    ".ne": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Exception
    ".nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#81a2be" }), # Name.Function
    ".nl": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name.Label
    ".nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#f0c674" }), # Name.Namespace
    ".nx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#81a2be" }), # Name.Other
    ".py": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name.Property
    ".nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7" }), # Name.Tag
    ".nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Variable
    ".ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "#8abeb7" }), # Operator.Word
    ".w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Text.Whitespace
    ".mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number.Float
    ".mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number.Hex
    ".mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number.Integer
    ".mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number.Oct
    ".sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Backtick
    ".sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Literal.String.Char
    ".sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#969896" }), # Literal.String.Doc
    ".s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Double
    ".se": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.String.Escape
    ".sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Heredoc
    ".si": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.String.Interpol
    ".sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Other
    ".sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Regex
    ".s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Single
    ".ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "#b5bd68" }), # Literal.String.Symbol
    ".bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#c5c8c6" }), # Name.Builtin.Pseudo
    ".vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Variable.Class
    ".vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Variable.Global
    ".vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#cc6666" }), # Name.Variable.Instance
    ".il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#de935f" }), # Literal.Number.Integer.Long
}
