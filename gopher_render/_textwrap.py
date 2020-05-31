"""
Code in this file is adapted from the Python Standard Library, specifically
the `textwrap` module. The changes are to ignore the length contributed by ANSI
escape codes when wrapping text, as they are invisible when displayed.

Copyright (C) 1999-2001 Gregory P. Ward.
Copyright (C) 2002, 2003 Python Software Foundation.
Written by Greg Ward <gward@python.net>
"""

from textwrap import TextWrapper
import re

_escape_regex = regex = re.compile(
    r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    m        # a literal m
    """, re.VERBOSE
)

def _len(obj):
    if not isinstance(obj, str):
        return len(obj)
    actual = _escape_regex.sub("", obj)
    return len(actual)


class AnsiAwareTextWrapper(TextWrapper):
    """
    This TextWrapper subclass ignores ANSI escape sequences when determining
    the length of wrapped lines.
    """

    def _wrap_chunks(self, chunks):
        """
        An exact reimplementation of the method from the base class, but using
        a custom length function to take ANSI escape sequences into account,
        since they are invisible in the output on target platforms.
        """
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")

        # Arrange in reverse order so items can be efficiently popped
        # from a stack of chucks.
        chunks.reverse()

        while chunks:

            # Start the list of chunks that will make up the current line.
            # cur_len is just the length of all the chunks in cur_line.
            cur_line = []
            cur_len = 0

            # Figure out which static string will prefix this line.
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            # Maximum width for this line.
            width = self.width - len(indent)

            # First chunk on line is whitespace -- drop it, unless this
            # is the very beginning of the text (ie. no lines started yet).
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]

            while chunks:
                l = _len(chunks[-1])

                # Can at least squeeze this chunk onto the current line.
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l

                # Nope, this line is full.
                else:
                    break

            # The current line is full, and the next chunk is too big to
            # fit on *any* line (not just this one).
            if chunks and _len(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
                cur_len = sum(map(_len, cur_line))

            # If the last chunk on this line is all whitespace, drop it.
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                cur_len -= _len(cur_line[-1])
                del cur_line[-1]

            if cur_line:
                if (self.max_lines is None or
                    len(lines) + 1 < self.max_lines or
                    (not chunks or
                     self.drop_whitespace and
                     len(chunks) == 1 and
                     not chunks[0].strip()) and cur_len <= width):
                    # Convert current line back to a string and store it in
                    # list of all lines (return value).
                    lines.append(indent + ''.join(cur_line))
                else:
                    while cur_line:
                        if (cur_line[-1].strip() and
                            cur_len + len(self.placeholder) <= width):
                            cur_line.append(self.placeholder)
                            lines.append(indent + ''.join(cur_line))
                            break
                        cur_len -= _len(cur_line[-1])
                        del cur_line[-1]
                    else:
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if (_len(prev_line) + len(self.placeholder) <=
                                    self.width):
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                    break

        return lines


def wrap(text, width=70, **kwargs):
    """A reimplementation of the textwrap.wrap function to use the custom
    TextWrapper type.
    """
    w = AnsiAwareTextWrapper(width=width, **kwargs)
    return w.wrap(text)
