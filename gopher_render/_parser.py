from html.parser import HTMLParser
import textwrap
from urllib.parse import urlparse

from .rendering import full_justify

from .rendering import Box, BoxSide
from .rendering import Renderer, InlineRenderer, BlockRenderer
from .rendering import HeaderRenderer, MarkdownHeaderRenderer
from .rendering import ParagraphRenderer, BlockQuoteRenderer
from .rendering import CodeRenderer, PreRenderer
from .rendering import EmRenderer, StrongRenderer
from .rendering import UnderlineRenderer, StrikethroughRenderer
from .rendering import LinkRenderer, ExtractedLinkRenderer


# TODO: Maybe this class should do more actual parsing? Or just rename to Tag
class TagParser(object):

    def __init__(self, tag, parent, attrs, **context):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.closed = False
        self.attrs = {}
        self.classes = []
        self.id = None
        if attrs is not None:
            self.attrs = dict(attrs)
            self.classes = self.__extract_classes()
            self.id = self.attrs.get('id', None)
        self.renderer = None
        self._context = context

    def __extract_classes(self):
        if 'class' in self.attrs:
            self.attrs['class'] = self.attrs['class'].split()
            return self.attrs['class']
        return []

    def assign_renderer(self, renderer):
        self.renderer = renderer

    def render(self, box):
        render_context = dict(
            parent_box=box,
        )
        render_context.update(self._context)

        render_inst = self.renderer(self, **render_context)
        try:
            box = render_inst.box
        except AttributeError:
            # If the renderer doesn't provide a box then the parent's gets
            # passed through.
            pass

        rendered_children = []
        for c in self.children:
            rendered_children.append(
                c.render(box)
            )

        return render_inst.render(
            "".join(rendered_children)
        )


class LinkParser(TagParser):

    def __init__(
        self,
        tag,
        parent,
        attrs,
        **context
    ):
        super().__init__(
            tag,
            parent,
            attrs,
            **context
        )
        self.link_renderer = None
        # If set, this will be used as the link description
        self.title = self.attrs.get('title', None)
        self.href = self.attrs.get('href', None)
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

    def assign_renderer(self, renderer):
        self.renderer = renderer[0]
        self.link_renderer = renderer[1]

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
        render_context = dict(
            href=self.href,
            title=self.title,
            gopher_link=self.gopher_link,
            parent_box=box
        )
        render_context.update(self._context)

        if render_context["link_placement"] == "inline":
            render_inst = self.renderer(self, **render_context)
        else:
            render_inst = self.link_renderer(self, **render_context)
        try:
            box = render_inst.box
        except AttributeError:
            # If the renderer doesn't provide a box then the parent's gets
            # passed through.
            pass

        rendered_children = []
        for c in self.children:
            rendered_children.append(
                c.render(box)
            )

        return render_inst.render(
            "".join(rendered_children)
        )


class DataParser(TagParser):
    def __init__(self, parent, data, **context):
        super().__init__(None, parent, None, **context)
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
        renderers={},
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
        self.tree = []
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
        self.renderers = {
            '': Renderer,
            'h1': MarkdownHeaderRenderer,
            'h2': MarkdownHeaderRenderer,
            'h3': MarkdownHeaderRenderer,
            'p': ParagraphRenderer,
            'blockquote': BlockQuoteRenderer,
            'pre': PreRenderer,
            'code': CodeRenderer,
            'a': (LinkRenderer, ExtractedLinkRenderer),
            'em': EmRenderer,
            'strong': StrongRenderer,
            'i': EmRenderer,
            'b': StrongRenderer,
            'u': UnderlineRenderer,
            's': StrikethroughRenderer,
        }
        self.renderers.update(renderers)
        self._next_link_number = 1
        self._pending_links = []

    def _get_top(self):
        t = None
        if len(self._tag_stack) > 0:
            t = self._tag_stack[-1]
            if t.closed:
                t = None
        return t

    def _get_renderer(self, tag, attrs):
        renderer = self.renderers.get(tag, None)
        if not renderer:
            renderer = self.renderers['']
        return renderer

    def handle_starttag(self, tag, attrs):
        parent = self._get_top()
        renderer = self._get_renderer(tag, attrs)
        t = None
        if tag == 'a':
            t = LinkParser(
                tag,
                parent,
                attrs,
                output_format=self._output_format,
                link_placement=self._link_placement,
                link_reference=self._next_link_number,
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
            )
        self._tag_stack.append(t)
        if parent:
            parent.children.append(t)
        else:
            self.tree.append(t)

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

    def handle_data(self, data):
        parent = self._get_top()
        d = DataParser(parent, data)
        if parent:
            parent.children.append(d)
        else:
            # No containing tags, so add directly to the root of the tree
            self.tree.append(d)

    def _indent_body(self):
        box = self._box
        parsed = "".join(self._parsed)
        lines = parsed.splitlines(keepends=True)
        return "".join([
            "{}{}".format(' ' * self._box.margin[BoxSide.LEFT], l)
            for l in lines
        ])

    def _assign_renderers(self, tags):
        for tag in tags:
            renderer = self._get_renderer(tag.tag, tag.attrs)
            tag.assign_renderer(renderer)
            self._assign_renderers(tag.children)

    def close(self):
        super().close()
        # Compile the parsed string
        # Anything being left in _tag_stack probably indicates an unclosed tag...
        # Pop everything off anyway and add any root tags to the tree.
        while len(self._tag_stack) > 0:
            t = self._tag_stack.pop()
            if t.parent is None:
                self.tree.append(t)

        # Walk the tree and assign renderers.
        self._assign_renderers(self.tree)

        for t in self.tree:
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
        # Addition of padding and border to box model complicate this even further
        indented = self._indent_body()
        self.parsed = "{}{}{}".format(
            "\n" * self._box.margin[BoxSide.TOP],
            indented,
            "\n" * self._box.margin[BoxSide.BOTTOM]
        )

    def reset(self):
        super().reset()
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        self.tree = []
        self._next_link_number = 1
        self._pending_links = []
