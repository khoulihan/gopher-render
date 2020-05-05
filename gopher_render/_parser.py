from html.parser import HTMLParser
import textwrap
from urllib.parse import urlparse

from .formatting import full_justify
from .formatting import null_formatter, default_h1_formatter, default_h2_formatter
from .formatting import default_h3_formatter, default_p_formatter
from .formatting import default_pre_formatter, default_code_formatter
from .formatting import default_link_formatter, default_extracted_link_formatter
from .formatting import default_em_formatter, default_strong_formatter
from .formatting import Box


class TagParser(object):

    def __init__(self, tag, parent, attrs, formatter, **context):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.closed = False
        self.attrs = attrs
        self.formatter = formatter
        self._context = context

    def render(self, box):
        format_context = dict(
            parent=self.parent,
            children=self.children,
            attrs=self.attrs,
            parent_box=box,
        )
        format_context.update(self._context)
        box = self.formatter.get_box(
            self.tag,
            format_context
        )

        rendered = []
        for c in self.children:
            rendered.append(
                c.render(box)
            )

        return self.formatter(
            self.tag,
            "".join(rendered),
            **format_context
        )


class LinkParser(TagParser):

    def __init__(
        self,
        tag,
        parent,
        attrs,
        formatter,
        link_formatter,
        **context
    ):
        super().__init__(
            tag,
            parent,
            attrs,
            formatter,
            **context
        )
        self.link_formatter = link_formatter
        self.href = None
        # If set, this will be used as the link description
        self.title = None
        for attr in attrs:
            if attr[0] == 'href':
                self.href = attr[1]
            if attr[0] == 'title':
                self.title = attr[1]
        self.gopher_link = self._parse_href()

    # TODO: This needs a lot more work to be comprehensive
    def _guess_type(self, path):
        p = path.rpartition('.')
        if p[0] == "":
            # No file extension, so gopher menu?
            return 1
        elif p[2] in ("html", "htm"):
            return 'h'
        elif p[2] == 'gif':
            return 'g'
        elif p[2] in ('jpg', 'jpeg', 'png', 'bmp', 'tiff'):
            return 'I'
        elif p[2] in ('txt', 'csv', 'tsv', 'md'):
            return 0
        else:
            # Default to binary for all other files
            return 9


    def _parse_href(self):
        """
        Parse the href of the link and return a dictionary containing the
        elements of a gophermap link
        """
        parsed = urlparse(self.href)
        if parsed.scheme in ("http", "https"):
            return dict(
                type='h',
                selector="URL:{}".format(self.href),
                host=self._context['gopher_host'],
                port=self._context['gopher_port'],
            )
        elif parsed.scheme == 'gopher':
            # Absolute gopher url
            return dict(
                type=self._guess_type(parsed.path),
                selector=parsed.path,
                host=parsed.hostname,
                port=parsed.port,
            )
        elif parsed.scheme == '':
            # Relative URL - interpret as a relative gopher link
            return dict(
                type=self._guess_type(parsed.path),
                selector=parsed.path,
                host=self._context['gopher_host'],
                port=self._context['gopher_port'],
            )
        else:
            # Unknown protocol: try it as a web link
            return dict(
                type='h',
                selector="URL:{}".format(self.href),
                host=self._context['gopher_host'],
                port=self._context['gopher_port'],
            )

    # For links, this generally renders the contents of the tag in its
    # original location, unless 'link_placement' is 'inline', in which case
    # link rendering occurs in the original location.
    def render(self, box):
        if self._context['link_placement'] != 'inline':
            return super().render(box)
        return self.link_render(box)

    def link_render(self, box):
        """
        Render an extracted link.
        """
        format_context = dict(
            parent=self.parent,
            children=self.children,
            attrs=self.attrs,
            href=self.href,
            title=self.title,
            gopher_link=self.gopher_link,
            parent_box=box
        )
        format_context.update(self._context)

        # Not sure that adjusting the box for links is going to work too well
        # Certainly for gopher links the box should be ignored entirely.
        box = self.formatter.get_box(
            self.tag,
            format_context
        )

        rendered = []
        for c in self.children:
            rendered.append(
                c.render(box)
            )
        rendered_text = "".join(rendered)

        return self.link_formatter(
            self.tag,
            rendered_text,
            **format_context
        )


class DataParser(TagParser):
    def __init__(self, parent, data, **context):
        super().__init__(None, parent, None, None, **context)
        self.data = data
        self.closed = True

    def render(self, box):
        return self.data


class GopherHTMLParser(HTMLParser):
    # TODO: Dependency injection so that custom tag rendering classes can be supplied
    def __init__(
        self,
        width=67,
        box=None,
        formatters={},
        output_format='text',
        link_placement='footer',
        gopher_host="",
        gopher_port=70,
    ):
        if output_format == 'gophermap' and link_placement == 'inline':
            raise ValueError("Links cannot be inlined in gophermap output")
        if output_format == 'gophermap' and gopher_host == '':
            raise ValueError("gopher_host is required for gophermap output")
        super().__init__(convert_charrefs=True)
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        #self._width = width
        if box:
            self._box = box
        else:
            # TODO: Maybe a default top margin as well?
            self._box = Box(
                width=67
            )
        self._output_format = output_format
        self._link_placement = link_placement
        self._gopher_host = gopher_host
        self._gopher_port = gopher_port
        self.formatters = {
            '': null_formatter,
            'h1': default_h1_formatter,
            'h2': default_h2_formatter,
            'h3': default_h3_formatter,
            'p': default_p_formatter,
            'pre': default_pre_formatter,
            'code': default_code_formatter,
            'a': (default_link_formatter, default_extracted_link_formatter),
            'em': default_em_formatter,
            'strong': default_strong_formatter,
        }
        self.formatters.update(formatters)
        self._next_link_number = 1
        self._pending_links = []

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
        t = None
        if tag == 'a':
            t = LinkParser(
                tag,
                parent,
                attrs,
                formatter[0],
                formatter[1],
                output_format=self._output_format,
                link_placement=self._link_placement,
                link_number=self._next_link_number,
                gopher_host=self._gopher_host,
                gopher_port=self._gopher_port,
            )
            self._next_link_number += 1
            if self._link_placement != 'inline':
                self._pending_links.append(t)
        else:
            t = TagParser(
                tag,
                parent,
                attrs,
                formatter,
            )
        self._tag_stack.append(t)
        if parent:
            parent.children.append(t)

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
            # TODO: This will have to determine if links should be rendered
            # after the closed tag if link_placement is 'after_block'
            self._tag_stack.pop()
            if top.parent is None and len(self._tag_stack) == 0:
                self._parsed.append(top.render(self._box))

    def handle_data(self, data):
        parent = self._get_top()
        d = DataParser(parent, data)
        if parent:
            parent.children.append(d)
        else:
            # No containing tags, so just dump directly to the output
            # Not an ideal scenario
            self._parsed.append(d.render(None))

    def _indent_body(self):
        box = self._box
        parsed = "".join(self._parsed)
        lines = parsed.splitlines(keepends=True)
        return "".join([
            "{}{}".format(' ' * self._box.left, l)
            for l in lines
        ])

    def close(self):
        super().close()
        # Compile the parsed string
        for t in self._tag_stack:
            self._parsed.append(t.render(self._box))
        if self._link_placement == 'footer' and len(self._pending_links) > 0:
            self._parsed.append("\n")
            for l in self._pending_links:
                self._parsed.append(l.link_render(self._box))

        # TODO: Some variation here within our box model:
        # Gophermap links should definitely not be indented, but this naively
        # indents everything. If link placement is footer this should be easy
        # enough to avoid, but for inter-block links it will be troublesome.
        # Could perhaps identify the points where links need to be inserted
        # and indent everything around them separately.
        indented = self._indent_body()
        self.parsed = "{}{}{}".format(
            "\n" * self._box.top,
            indented,
            "\n" * self._box.bottom
        )

    def reset(self):
        super().reset()
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        self._next_link_number = 1
        self._pending_links = []
