"""
Autumn Pygments theme.
"""
from ..rendering import AnsiEscapeCodeRenderer

# I think this has a slightly more complete set of class definitions than
# the other themes, so good to use as a base.
renderers = {
    ".highlight .hll": (AnsiEscapeCodeRenderer, { "background_colour": "#ffffcc" }),
    ".highlight":  (AnsiEscapeCodeRenderer, { "background_colour": "#ffffff" }),
    ".highlight .c": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aaaaaa", "italic": True }), # Comment
    ".highlight .err": (AnsiEscapeCodeRenderer, { "foreground_colour": "#FF0000", "background_colour": "#FFAAAA" }), # Error
    ".highlight .k": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword
    ".highlight .ch": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aaaaaa", "italic": True }), # Comment.Hashbang
    ".highlight .cm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aaaaaa", "italic": True }), # Comment.Multiline
    ".highlight .cp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#4c8317" }), # Comment.Preproc
    ".highlight .cpf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aaaaaa", "italic": True }), # Comment.PreprocFile
    ".highlight .c1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aaaaaa", "italic": True }), # Comment.Single
    ".highlight .cs": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa", "italic": True }), # Comment.Special
    ".highlight .gd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Generic.Deleted
    ".highlight .ge": (AnsiEscapeCodeRenderer, { "italic": True }), # Generic.Emph
    ".highlight .gr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Generic.Error
    ".highlight .gh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#000080", "bold": True }), # Generic.Heading
    ".highlight .gi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aa00" }), # Generic.Inserted
    ".highlight .go": (AnsiEscapeCodeRenderer, { "foreground_colour": "#888888" }), # Generic.Output
    ".highlight .gp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#555555" }), # Generic.Prompt
    ".highlight .gs": (AnsiEscapeCodeRenderer, { "bold": True }), # Generic.Strong
    ".highlight .gu": (AnsiEscapeCodeRenderer, { "foreground_colour": "#800080", "bold": True }), # Generic.Subheading
    ".highlight .gt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Generic.Traceback
    ".highlight .kc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword.Constant
    ".highlight .kd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword.Declaration
    ".highlight .kn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword.Namespace
    ".highlight .kp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword.Pseudo
    ".highlight .kr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Keyword.Reserved
    ".highlight .kt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aaaa" }), # Keyword.Type
    ".highlight .m": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number
    ".highlight .s": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String
    ".highlight .na": (AnsiEscapeCodeRenderer, { "foreground_colour": "#1e90ff" }), # Name.Attribute
    ".highlight .nb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aaaa" }), # Name.Builtin
    ".highlight .nc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aa00" }), # Name.Class
    ".highlight .no": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Constant
    ".highlight .nd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#888888" }), # Name.Decorator
    ".highlight .ni": (AnsiEscapeCodeRenderer, { "foreground_colour": "#880000", "bold": True }), # Name.Entity
    ".highlight .nf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aa00" }), # Name.Function
    ".highlight .nn": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aaaa" }), # Name.Namespace
    ".highlight .nt": (AnsiEscapeCodeRenderer, { "foreground_colour": "#1e90ff", "bold": True }), # Name.Tag
    ".highlight .nv": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Variable
    ".highlight .ow": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Operator.Word
    ".highlight .w": (AnsiEscapeCodeRenderer, { "foreground_colour": "#bbbbbb" }), # Text.Whitespace
    ".highlight .mb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Bin
    ".highlight .mf": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Float
    ".highlight .mh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Hex
    ".highlight .mi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Integer
    ".highlight .mo": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Oct
    ".highlight .sa": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Affix
    ".highlight .sb": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Backtick
    ".highlight .sc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Char
    ".highlight .dl": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Delimiter
    ".highlight .sd": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Doc
    ".highlight .s2": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Double
    ".highlight .se": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Escape
    ".highlight .sh": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Heredoc
    ".highlight .si": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Interpol
    ".highlight .sx": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Other
    ".highlight .sr": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.String.Regex
    ".highlight .s1": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa5500" }), # Literal.String.Single
    ".highlight .ss": (AnsiEscapeCodeRenderer, { "foreground_colour": "#0000aa" }), # Literal.String.Symbol
    ".highlight .bp": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aaaa" }), # Name.Builtin.Pseudo
    ".highlight .fm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#00aa00" }), # Name.Function.Magic
    ".highlight .vc": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Variable.Class
    ".highlight .vg": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Variable.Global
    ".highlight .vi": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Variable.Instance
    ".highlight .vm": (AnsiEscapeCodeRenderer, { "foreground_colour": "#aa0000" }), # Name.Variable.Magic
    ".highlight .il": (AnsiEscapeCodeRenderer, { "foreground_colour": "#009999" }), # Literal.Number.Integer.Long
}
