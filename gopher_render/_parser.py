from html.parser import HTMLParser
import textwrap

from .formatting import full_justify
from .formatting import null_formatter, default_h1_formatter, default_h2_formatter
from .formatting import default_h3_formatter, default_p_formatter
from .formatting import default_pre_formatter, default_code_formatter


class TagParser(object):

    def __init__(self, tag, parent, attrs, formatter, **context):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.closed = False
        self.attrs = attrs
        self.formatter = formatter
        self._context = context

    def render(self):
        rendered = []
        for c in self.children:
            rendered.append(c.render())
        format_context = dict(
            parent=self.parent,
            children=self.children,
            attrs=self.attrs,
        )
        format_context.update(self._context)
        return self.formatter(
            self.tag,
            "".join(rendered),
            **format_context
        )


class DataParser(TagParser):
    def __init__(self, parent, data, **context):
        super().__init__(None, parent, None, None, **context)
        self.data = data
        self.closed = True

    def render(self):
        return self.data


# TODO: This needs a mechanism to select formatters based on tag and attrs,
# though the base implementation will probably ignore most attrs.
class GopherHTMLParser(HTMLParser):
    # TODO: Dependency injection so that custom tag rendering classes can be supplied
    def __init__(self, width=67, formatters={}):
        super().__init__(convert_charrefs=True)
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        self._width = width
        self.formatters = {
            '': null_formatter,
            'h1': default_h1_formatter,
            'h2': default_h2_formatter,
            'h3': default_h3_formatter,
            'p': default_p_formatter,
            'pre': default_pre_formatter,
            'code': default_code_formatter,
        }
        self.formatters.update(formatters)

    def _get_top(self):
        t = None
        if len(self._tag_stack) > 0:
            t = self._tag_stack[-1]
            if t.closed:
                t = None
        return t

    def _get_formatter(self, tag, attrs):
        formatter = self.formatters.get(tag, None)
        if not formatter:
            formatter = self.formatters['']
        return formatter

    def handle_starttag(self, tag, attrs):
        parent = self._get_top()
        formatter = self._get_formatter(tag, attrs)
        t = TagParser(
            tag,
            parent,
            attrs,
            formatter,
            width=self._width
        )
        if t:
            self._tag_stack.append(t)
            if parent:
                parent.children.append(t)
        else:
            print("Unsupported start tag, ignoring: " + tag)

    def handle_endtag(self, tag):
        top = self._get_top()
        if not top:
            print("Unsupported or mismatched end tag, ignoring: " + tag)
            return
        if top.tag == tag:
            top.closed = True
        else:
            # TODO: Consider instead just accepting mismatched tags and closing the top tag?
            print("Unsupported or mismatched end tag, ignoring: " + tag)
        if top.closed:
            self._tag_stack.pop()
            if top.parent is None and len(self._tag_stack) == 0:
                self._parsed.append(top.render())

    def handle_data(self, data):
        parent = self._get_top()
        d = DataParser(parent, data)
        if parent:
            parent.children.append(d)
        else:
            # No containing tags, so just dump directly to the output
            # Not an ideal scenario
            self._parsed.append(d.render())

    def close(self):
        super().close()
        # Compile the parsed string
        for t in self._tag_stack:
            self._parsed.append(t.render())
        self.parsed = "".join(self._parsed)

    def reset(self):
        super().reset()
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
