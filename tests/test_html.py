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
    lines = output.splitlines()
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
    lines = output.splitlines()
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
    lines = output.splitlines()
    assert len(lines) == 6

    # Check the centering
    assert lines[2].startswith(' ' * 30)
    assert lines[2].endswith(' ' * 30)
    assert lines[2].strip() == "Seventh"

    # Check the underline
    assert lines[3] == "=" * 67
