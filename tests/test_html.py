"""
Test that various HTML tags are rendered correctly.
"""

from gopher_render import GopherHTMLParser


class TestDefaults:
    """
    Test the default output formatting for all tags.

    The default output should match markdown formatting
    """
    def test_p_tag_default_short(self):
        """
        Default p tag render has a line below and is left justified.
        """
        html = "<p>Paragraph Text</p>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Blank line after.
        assert output.endswith("\n")

        # No wrapping should occur (line count includes blanks)
        lines = output.split('\n')
        assert len(lines) == 3

        # Initial line indent
        #assert lines[1].startswith(' ' * 8)

        assert lines[1].strip() == "Paragraph Text"
        assert len(lines[1]) == len(lines[1].strip())
        assert lines[2] == ''


    def test_p_tag_default_long(self):
        """
        Default p tag render has a line below
        Long lines are wrapped to 67 characters and full justified.
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
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Blank line before.
        assert output.endswith("\n")

        # Wrapping (line count includes blank lines)
        lines = output.split('\n')
        assert len(lines) == 10

        # Initial line indent
        #assert lines[1].startswith(' ' * 8)

        # Check that lines are padded to the correct width
        for li in range(1, len(lines) - 1):
            assert len(lines[li]) == 67


    def test_br_tag_default(self):
        """
        Default br tag renderer just adds a newline. It should not be removed
        by p tag formatting.
        """
        html = "<p>Paragraph<br>Text</p>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Blank line after.
        assert output.endswith("\n")

        # One extra wrap for the br
        lines = output.split('\n')
        assert len(lines) == 4

        assert lines[1].strip() == "Paragraph"
        assert len(lines[1]) == len(lines[1].strip())
        assert lines[2].strip() == 'Text'
        assert len(lines[2]) == len(lines[2].strip())


    def test_closed_br_tag_default(self):
        """
        Default br tag renderer just adds a newline. It should not be removed
        by p tag formatting.
        """
        html = "<p>Paragraph<br/>Text</p>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Blank line after.
        assert output.endswith("\n")

        # One extra wrap for the br
        lines = output.split('\n')
        assert len(lines) == 4

        assert lines[1].strip() == "Paragraph"
        assert len(lines[1]) == len(lines[1].strip())
        assert lines[2].strip() == 'Text'
        assert len(lines[2]) == len(lines[2].strip())


    def _header(self, html, result):
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.strip() == result
        assert output.startswith('\n')
        assert output.endswith('\n')
        assert len(output) == 69


    def test_h1_tag_default(self):
        """
        Default h1 tag render has a line below, and has a # on either side
        """
        self._header(
            "<h1>Seventh</h1>",
            "# Seventh #"
        )


    def test_h2_tag_default(self):
        """
        Default h2 tag render has a line below, and has a ## on either side
        """
        self._header(
            "<h2>Seventh</h2>",
            "## Seventh ##"
        )


    def test_h3_tag_default(self):
        """
        Default h3 tag render has a line below, and has a ### on either side
        """
        self._header(
            "<h3>Seventh</h3>",
            "### Seventh ###"
        )


    def test_h4_tag_default(self):
        """
        Default h4 tag render has a line below, and has a #### on either side
        """
        self._header(
            "<h4>Seventh</h4>",
            "#### Seventh ####"
        )


    def test_h5_tag_default(self):
        """
        Default h5 tag render has a line below, and has a ##### on either side
        """
        self._header(
            "<h5>Seventh</h5>",
            "##### Seventh #####"
        )


    def test_h6_tag_default(self):
        """
        Default h6 tag render has a line below, and has a ###### on either side
        """
        self._header(
            "<h6>Seventh</h6>",
            "###### Seventh ######"
        )


    def test_code_span_default(self):
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


    def test_code_span_in_p_default(self):
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
        assert output.strip() == "This paragrah includes a `ClassName` in a code tag."


    def test_code_block_default(self):
        """
        Where a code tags parent is a pre tag, its content should NOT be surrounded by backticks.

        The pre tag content will be indented, and also have a line after
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

        for li in range(1, 3):
            assert lines[li].rstrip() == "    {}".format(codelines[li - 1])


    def test_blockquote_default(self):
        """
        Blockquotes have a line before and after, and '> ' at the start of each
        line. Paragraphs within the quote will have one blank line between them,
        but the first and last paragraphs will not have top and bottom margins
        respectively.
        """
        html = "<blockquote><p>One</p><p>Two</p></blockquote>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Blank lines before and after.
        assert output.startswith("\n")
        assert output.endswith("\n")

        # No wrapping should occur (line count includes blanks)
        lines = output.split('\n')
        assert len(lines) == 5

        for line in lines[1:-1]:
            assert line.startswith("> ")
            assert len(line) == 67
        assert lines[2].strip() == '>'


    def test_em_default(self):
        """
        Default em tag render should just surround the content in underscores.
        """
        html = "<em>ClassName</em>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by underscores
        assert output.startswith("_")
        assert output.endswith("_")

        # Only one set of underscores, and the content.
        assert len(output) == 11

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_strong_default(self):
        """
        Default strong tag render should just surround the content in **s.
        """
        html = "<strong>ClassName</strong>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by asterisks
        assert output.startswith("**")
        assert output.endswith("**")

        # Double asterisks, and the content.
        assert len(output) == 13

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_u_default(self):
        """
        Default u tag render should just surround the content in underscores.
        """
        html = "<u>ClassName</u>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by underscores
        assert output.startswith("_")
        assert output.endswith("_")

        # Only one set of underscores, and the content.
        assert len(output) == 11

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_s_default(self):
        """
        Default s tag (strikethrough) render should just surround the content in ~~s.
        """
        html = "<s>ClassName</s>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by tildes
        assert output.startswith("~~")
        assert output.endswith("~~")

        # Double tildes, and the content.
        assert len(output) == 13

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_ins_default(self):
        """
        Default ins tag render should just surround the content in underscores.
        """
        html = "<ins>ClassName</ins>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by underscores
        assert output.startswith("_")
        assert output.endswith("_")

        # Only one set of underscores, and the content.
        assert len(output) == 11

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_del_default(self):
        """
        Default del tag render should just surround the content in ~~s.
        """
        html = "<del>ClassName</del>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        # Surrounded by tildes
        assert output.startswith("~~")
        assert output.endswith("~~")

        # Double tildes, and the content.
        assert len(output) == 13

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_span_default(self):
        """
        Default span tag render should do... nothing!
        """
        html = "<span>ClassName</span>"
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("C")
        assert output.endswith("e")

        # Just the content.
        assert len(output) == 9

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_div_default(self):
        """
        Default div tag render should do nothing except pad to the width of
        the block.
        """
        html = "<div>ClassName</div>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("C")
        assert output.strip().endswith("e")

        # Just the padded content.
        assert len(output) == 67

        # Just one line
        lines = output.split('\n')
        assert len(lines) == 1


    def test_ul_default(self):
        """
        Default ul tag render. It prepends list items with '* ' and has a margin
        above and below.
        """
        html = "<ul><li>One</li><li>Two</li><li>Three</li></ul>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("\n")
        assert output.endswith("\n")

        lines = output.split('\n')
        assert len(lines) == 5
        for i in range(1, 4):
            assert lines[i].startswith("* ")
            assert len(lines[i]) == 67


    def test_ol_default(self):
        """
        Default ol tag render. It prepends list items with a number and has a margin
        above and below.
        """
        html = "<ol><li>One</li><li>Two</li><li>Three</li></ol>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("\n")
        assert output.endswith("\n")

        lines = output.split('\n')
        assert len(lines) == 5
        for i in range(1, 4):
            assert lines[i].startswith("{}. ".format(i))
            assert len(lines[i]) == 67


    def test_nested_lists_default(self):
        """
        Nested lists.
        """
        html = "<ol><li>One</li><li>Two<ul><li>Two Point One</li><li>Two Point Two</li></ul></li><li>Three</li></ol>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("\n")
        assert output.endswith("\n")

        lines = output.split('\n')
        assert len(lines) == 7
        for i in range(1, 3):
            assert lines[i].startswith("{}. ".format(i))
            assert len(lines[i]) == 67
        for i in range(3, 5):
            assert lines[i].startswith("   * ")
            assert len(lines[i]) == 67
        assert lines[5].startswith("3. ".format(i))
        assert len(lines[5]) == 67


    def test_whitespace(self):
        """
        Test that whitespace is removed or preserved as expected.
        """
        html = "\n".join([
            "<p>  This \t\t\tparagraph  ",
            "     has a \tbunch of",
            "whitespace   in between    ",
            "the lines  </p>",
        ])
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        lines = output.split('\n')
        assert len(lines) == 3

        result = "This paragraph has a bunch of whitespace in between the lines"
        assert lines[1] == result


    def test_whitespace_around_tags(self):
        """
        Test that whitespace is preserved around inline tags within a paragraph.
        """
        html = "\n".join([
            "<p>A first line,",
            "an <em>emphasised</em> second.",
            "<strong>Strong start </strong>to a third.",
            "</p>"
        ])
        parser = GopherHTMLParser()
        parser.feed(html)
        parser.close()
        output = parser.parsed

        lines = output.split('\n')
        assert len(lines) == 3

        # This is the formatted paragraph, but it then gets padded by the box model
        # Note that the paragraph justification adds an extra space after the
        # full stop here.
        result = "A first line, an _emphasised_ second.  **Strong start **to a third."
        result = result + (' ' * (67 - len(result)))
        assert lines[1] == result


    def test_dl_default(self):
        """
        Default dl tag render. It prepends definitions with ': ' and has a margin
        above and below, and a margin between terms.
        """
        html = "<dl><dt>One</dt><dd>Definition One</dd><dt>Two</dt><dd>Definition Two One</dd><dd>Definition Two Two</dd></dl>"
        parser = GopherHTMLParser(optimise=False)
        parser.feed(html)
        parser.close()
        output = parser.parsed

        assert output.startswith("\n")
        assert output.endswith("\n")

        lines = output.split('\n')
        assert len(lines) == 8
        assert lines[2].startswith(": ")
        for i in range(5, 7):
            assert lines[i].startswith(": ")
            assert len(lines[i]) == 67
        for i in range(1, 7):
            assert len(lines[i]) == 67
