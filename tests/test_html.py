"""
Test that various HTML tags are rendered correctly.
"""

from gopher_render import GopherHTMLParser


def test_p_tag_default_short():
    """
    Default p tag render has a line above and below, and an 8 space indent for
    the first line.
    """
    html = "<p>Paragraph Text</p>"
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Blank lines before and after.
    assert output.startswith("\n")
    assert output.endswith("\n")

    # No wrapping should occur (line count includes blanks)
    lines = output.split('\n')
    assert len(lines) == 3

    # Initial line indent
    assert lines[1].startswith(' ' * 8)

    # As it is the only line, it should not be padded on the right.
    assert lines[1].lstrip() == "Paragraph Text"


def test_p_tag_default_long():
    """
    Default p tag render has a line above and below, and an 8 space indent for
    the first line. Long lines are wrapped to 67 characters and full justified.
    """
    html = ''.join([
        "<p>Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Paragraph Text Paragraph Text Paragraph Text Paragraph Text Paragraph ",
        "Text Paragraph Text Paragraph Text Paragraph Text</p>"
    ])
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Blank lines before and after.
    assert output.startswith("\n")
    assert output.endswith("\n")

    # Wrapping (line count includes blank lines)
    lines = output.split('\n')
    assert len(lines) == 10

    # Initial line indent
    assert lines[1].startswith(' ' * 8)

    # Check that lines are fully justified.
    for li in range(1, len(lines) - 2):
        assert len(lines[li]) == 67

    # The final line should not be padded on the right.
    assert len(lines[-1]) < 67


def test_h1_tag_default():
    """
    Default h1 tag render has 2 lines above and 2 below, is centred, and has a
    full width underline of '=' characters.
    """
    html = "<h1>Seventh</h1>"
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Blank lines before and after
    assert output.startswith("\n\n")
    assert output.endswith("\n\n")

    # Blank lines, header, and underline
    lines = output.split('\n')
    assert len(lines) == 6

    # Check the centering
    assert lines[2].startswith(' ' * 30)
    assert lines[2].endswith(' ' * 30)
    assert lines[2].strip() == "Seventh"

    # Check the underline
    assert lines[3] == "=" * 67


def test_code_span_default():
    """
    Default code tag render should just surround the content in backticks.
    """
    html = "<code>ClassName</code>"
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Surrounded by backticks
    assert output.startswith("`")
    assert output.endswith("`")

    # Only one set of backticks, and the content.
    assert len(output) == 11

    # Just one line
    lines = output.split('\n')
    assert len(lines) == 1


def test_code_span_in_p_default():
    """
    Default code tag render should just surround the content in backticks.

    This test checks that this works correctly within a p tag.
    """
    html = "<p>This paragrah includes a <code>ClassName</code> in a code tag.</p>"
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Surrounded by backticks
    assert output == "\n        This paragrah includes a `ClassName` in a code tag.\n"


def test_code_block_default():
    """
    Where a code tags parent is a pre tag, its content should NOT be surrounded by backticks.

    The pre tag content will be indented, and also have a line before and after
    """
    code = "\n".join([
        "def func():",
        "    print('Some nonsense')",
        "    return True",
    ])
    html = "<pre><code>{}</code></pre>".format(code)
    parser = GopherHTMLParser()
    parser.feed(html)
    parser.close()
    output = parser.parsed

    # Blank lines before and after.
    assert output.startswith("\n")
    assert output.endswith("\n")

    # No wrapping should occur (line count includes blanks)
    lines = output.split('\n')
    assert len(lines) == 5

    codelines = code.split('\n')

    for li in range(1, 4):
        assert lines[li] == "    {}".format(codelines[li - 1])
