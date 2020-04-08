from html.parser import HTMLParser
import textwrap

from .formatting import full_justify

# TODO: I think it might be better to rework this into a single TagParser class with a tag attribute
# and then provide that with a formatting class or function depending on the tag and other criteria
# controlled by the GopherHTMLParser
class TagParser(object):

    tag = None

    def __init__(self, parent, attrs, width):
        self.parent = parent
        self.children = []
        self.closed = False
        self._width = width

    def render(self):
        rendered = ""
        for c in self.children:
            rendered = rendered + c.render()
        return rendered


class DataParser(TagParser):
    def __init__(self, parent, data, width):
        super().__init__(parent, None, width)
        self.data = data
        self.closed = True

    def render(self):
        return self.data


class ParagraphParser(TagParser):

    tag = 'p'

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        # TODO: Justification and first line indent should be options
        out = full_justify(
            " "*8 + super().render(),
            self._width,
            fix_sentence_endings=True
        )
        # lines = textwrap.wrap(
        #     " "*8 + super().render(),
        #     self._width,
        #     fix_sentence_endings=True
        # )
        # for l in lines:
        #     print(len(l))
        # return "\n".join([l.ljust(self._width) for l in lines]) + "\n\n"
        return out + '\n'


class HeaderParser(TagParser):

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        # TODO: Styling will need to be optional
        return super().render()


class H1Parser(HeaderParser):

    tag = 'h1'

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        # TODO: Styling will need to be optional
        return "\n" + ("=== {{ " + super().render() + " }} ===").center(self._width) + "\n\n"


class H2Parser(HeaderParser):

    tag = 'h2'

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        # TODO: Styling will need to be optional
        return "\n" + ("== { " + super().render() + " } ==").center(self._width) + "\n"


class H3Parser(HeaderParser):

    tag = 'h3'

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        # TODO: Styling will need to be optional
        return "\n" + ("= " + super().render() + " =").center(self._width) + "\n"


# TODO: Problem with this is that Markdown wraps code blocks
# in paragraphs, so the paragraph parser reformats all its content.
# Use of certain extensions avoids this - not sure there is going to be a way
# to avoid it otherwise. The p handler would need to check for code or pre children...
# What I might do is if a p only has one code or pre child then it does not
# do any formatting itself.
class CodeParser(TagParser):

    tag = 'code'

    def __init__(self, parent, attrs, width):
        super().__init__(parent, attrs, width)

    def render(self):
        return super().render()


# TODO: This needs a mechanism to select formatters based on tag and attrs,
# though the base implementation will probably ignore most attrs.
class GopherHTMLParser(HTMLParser):
    # TODO: Dependency injection so that custom tag rendering classes can be supplied
    def __init__(self, width=67):
        super().__init__(convert_charrefs=True)
        self.parsed = ""
        self._tag_stack = []
        self._width = width

    def _get_top(self):
        t = None
        if len(self._tag_stack) > 0:
            t = self._tag_stack[-1]
            if t.closed:
                t = None
        return t

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        parent = self._get_top()
        t = None
        if tag == 'h1':
            t = H1Parser(parent, attrs, self._width)
        elif tag == 'h2':
            t = H2Parser(parent, attrs, self._width)
        elif tag == 'h3':
            t = H3Parser(parent, attrs, self._width)
        elif tag == 'p':
            t = ParagraphParser(parent, attrs, self._width)
        elif tag == 'code':
            t = CodeParser(parent, attrs, self._width)
        if t:
            self._tag_stack.append(t)
            if parent:
                parent.children.append(t)
        else:
            print("Unsupported start tag, ignoring: " + tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        top = self._get_top()
        if not top:
            print("Unsupported or mismatched end tag, ignoring: " + tag)
            return
        if top.tag == tag:
            top.closed = True
        else:
            print("Unsupported or mismatched end tag, ignoring: " + tag)
        if top.closed:
            self._tag_stack.pop()
            if top.parent is None and len(self._tag_stack) == 0:
                self.parsed = self.parsed + top.render()

    def handle_data(self, data):
        print("Encountered some data  :", data)
        parent = self._get_top()
        d = DataParser(parent, data, self._width)
        if parent:
            parent.children.append(d)
        else:
            # No containing tags, so just dump directly to the output
            # Not an ideal scenario
            self.parsed = self.parsed + d.render()

    def close(self):
        super().close()
        # Compile the parsed string
        for t in self._tag_stack:
            self.parsed = self.parsed + t.render()

    def reset(self):
        super().reset()
        self.parsed = ""
        self._tag_stack = []
