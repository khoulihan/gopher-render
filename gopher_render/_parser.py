import re
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import namedtuple
import cssselect

from ._selectors import tag_matches, Specificity

from .rendering import full_justify

from .rendering import Box, BoxSide
from .rendering import Renderer, InlineRenderer, BlockRenderer
from .rendering import HeaderRenderer, MarkdownHeaderRenderer
from .rendering import ParagraphRenderer, BlockQuoteRenderer
from .rendering import CodeRenderer, PreRenderer
from .rendering import EmRenderer, StrongRenderer
from .rendering import UnderlineRenderer, StrikethroughRenderer
from .rendering import BreakRenderer
from .rendering import LinkRenderer, ExtractedLinkRenderer
from .rendering import ImageRenderer, ExtractedImageLinkRenderer
from .rendering import ListRenderer, ListItemRenderer, OrderedListItemRenderer
from .rendering import DefinitionListRenderer, DefinitionListTermHeaderRenderer, DefinitionListItemRenderer
from .rendering import AnsiEscapeCodeRenderer


# TODO: Maybe this class should do more actual parsing? Or just rename to Tag
class TagParser(object):

    def __init__(self, tag, parent, attrs, **context):
        self.tag = tag
        self.parent = parent
        self.children = []
        self.closed = tag in ('br', 'img')
        self.attrs = {}
        self.classes = []
        self.id = None
        if attrs is not None:
            self.attrs = dict(attrs)
            self.classes = self.__extract_classes()
            self.id = self.attrs.get('id', None)
        self.renderer = None
        self.renderer_settings = None
        self._context = context
        self._pending_links = []

    def tag_children(self):
        """
        Return only the children that represent tags (i.e. exclude any DataParsers)
        """
        return [t for t in self.children if t.tag is not None]

    def __extract_classes(self):
        if 'class' in self.attrs:
            self.attrs['class'] = self.attrs['class'].split()
            return self.attrs['class']
        return []

    def add_pending_link(self, link):
        self._pending_links.append(link)

    def assign_renderer(self, renderer):
        try:
            self.renderer = renderer[0]
            self.renderer_settings = renderer[1]
        except TypeError:
            self.renderer = renderer

    def render(self, box):
        render_context = dict(
            parent_box=box,
        )
        render_context.update(self._context)

        if self.renderer_settings is not None:
            render_context['settings'] = self.renderer_settings

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

        if len(self._pending_links):
            rendered_children.append('\n')
        for l in self._pending_links:
            rendered_children.append(
                l.link_render(box)
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
        if tag == 'a':
            # If set, this will be used as the link description
            self.title = self.attrs.get('title', None)
            self.href = self.attrs.get('href', None)
            self.gopher_link = self._parse_href()
        elif tag == 'img':
            # If set, this will be used as the link description
            self.title = self.attrs.get('alt', None)
            self.href = self.attrs.get('src', None)
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
        try:
            self.renderer = renderer[0][0]
            self.renderer_settings = renderer[0][1]
        except TypeError:
            self.renderer = renderer[0]

        try:
            self.link_renderer = renderer[1][0]
            self.link_renderer_settings = renderer[1][1]
        except TypeError:
            self.link_renderer = renderer[1]

    # For links, this generally renders the contents of the tag in its
    # original location, unless 'link_placement' is 'inline', in which case
    # link rendering occurs in the original location.
    def render(self, box):
        placement = self._context['image_placement'] if self.tag == 'img' else self._context['link_placement']
        if placement != 'inline':
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

        placement = render_context['image_placement'] if self.tag == 'img' else render_context['link_placement']
        if placement == "inline":
            renderer = self.renderer
            renderer_settings = self.renderer_settings
        else:
            renderer = self.link_renderer
            renderer_settings = self.link_renderer_settings

        render_inst = renderer(self, **render_context)
        if renderer_settings is not None:
            render_context['settings'] = renderer_settings

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
        if not context['in_pre']:
            # This attempts to remove extraneous formatting internal to the data
            # but does not remove whitespace from the start or end of the data
            # because it may be followed or preceeded by a tag that depends on
            # that whitespace for separation.
            # This produces different results than how browsers handle whitespace.
            # However, the paragraph renderer will also strip whitespace from the
            # start and end of its content, minimising the impact of this.
            data_split = data.split('\n')
            if len(data_split) > 1:
                data_stripped = []
                data_stripped.append(data_split[0].rstrip())
                if len(data_split) > 2:
                    data_stripped.extend([l.strip() for l in data_split[1:-1]])
                data_stripped.append(data_split[-1].lstrip())
                data_split = data_stripped
            data = ' '.join(data_split)
            data = re.sub('[ \t]+', ' ', data)
        self.data = data
        self.closed = True

    def render(self, box):
        return self.data


class DocumentParser(object):
    """
    Implicit root for the document, even if the html being parsed is only a
    fragment.

    For html tags that are otherwise parentless, an instance of this class will
    be the parent.
    """
    def __init__(self):
        self.children = []

    def tag_children(self):
        """
        Return only the children that represent tags (i.e. exclude any DataParsers)
        """
        return [t for t in self.children if t.tag is not None]

    def append(self, tag):
        self.children.append(tag)

    def reset(self):
        self.children = []


RendererMapping = namedtuple('RendererMapping', 'selector, renderer')


class RendererMap(object):
    """
    Provides a mapping of CSS selectors to Renderer specifications.
    """

    def __init__(self, renderer_dict):
        self._map = []
        for key in renderer_dict:
            selector = cssselect.parse(key)
            self._map.append(RendererMapping(selector, renderer_dict[key]))

    def get_for_tag(self, tag):
        all_matches = []
        for mapping in self._map:
            match, specificity = tag_matches(tag, mapping.selector)
            if match:
                all_matches.append(
                    (
                        Specificity(specificity),
                        mapping
                    )
                )
        all_matches.sort(key=lambda m: m[0])
        renderer = None
        renderer_settings = {}
        for s, mapping in all_matches:
            try:
                r = mapping.renderer[0]
                s = mapping.renderer[1]
            except TypeError:
                r = mapping.renderer
                s = None
            if r is not None:
                renderer = r
            if s is not None:
                renderer_settings.update(s)
        if not renderer:
            return None
        return (renderer, renderer_settings)


class GopherHTMLParser(HTMLParser):
    def __init__(
        self,
        width=67,
        box=None,
        renderers={},
        extracted_link_renderers={},
        output_format='text',
        link_placement='footer',
        image_placement='inline',
        gopher_host="",
        gopher_port=70,
        optimise=True,
    ):
        if output_format == 'gophermap' and link_placement == 'inline':
            raise ValueError("Links cannot be inlined in gophermap output")
        if output_format == 'gophermap' and gopher_host == '':
            raise ValueError("gopher_host is required for gophermap output")
        super().__init__(convert_charrefs=True)
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        self.tree = DocumentParser()
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
        self._image_placement = image_placement
        self._gopher_host = gopher_host
        self._gopher_port = gopher_port
        self.renderers = {
            # Default renderer. A * could also be used to match any element.
            '': Renderer,

            # Block elements
            'h1': MarkdownHeaderRenderer,
            'h2': MarkdownHeaderRenderer,
            'h3': MarkdownHeaderRenderer,
            'h4': MarkdownHeaderRenderer,
            'h5': MarkdownHeaderRenderer,
            'h6': MarkdownHeaderRenderer,
            'p': ParagraphRenderer,
            'br': BreakRenderer,
            'blockquote': BlockQuoteRenderer,
            'blockquote > p:first-child': (None, dict(
                margin=[0,0,1,0]
            )),
            'blockquote > p:last-child': (None, dict(
                margin=[1,0,0,0]
            )),
            # TODO: I think there is an :only-child selector for this
            'blockquote > p:last-child:first-child': (None, dict(
                margin=[0,0,0,0]
            )),
            'pre': PreRenderer,
            'div': BlockRenderer,
            'ul': ListRenderer,
            'ol': ListRenderer,
            'li': ListItemRenderer,
            'ol > li': OrderedListItemRenderer,
            'li:first-child': (None, dict(
                margin=[0,0,0,0]
            )),
            # TODO: The need for this is unfortunate...
            'li > ol > li:first-child, li > ul > li:first-child': (None, dict(
                margin=[1,0,0,0]
            )),

            # Definition list
            'dl': DefinitionListRenderer,
            'dt': DefinitionListTermHeaderRenderer,
            'dd': DefinitionListItemRenderer,
            'dt:first-child': (None, dict(
                margin=[0,0,0,0]
            )),

            # Inline elements
            'code': CodeRenderer,
            'a': LinkRenderer,
            'img': ImageRenderer,
            'em': EmRenderer,
            'strong': StrongRenderer,
            'i': EmRenderer,
            'b': StrongRenderer,
            'u': UnderlineRenderer,
            'ins': UnderlineRenderer,
            's': StrikethroughRenderer,
            'del': StrikethroughRenderer,
            'span': InlineRenderer,
        }
        self.renderers.update(renderers)
        self.extracted_link_renderers = {
            'a': ExtractedLinkRenderer,
            'img': ExtractedImageLinkRenderer,
        }
        self.extracted_link_renderers.update(extracted_link_renderers)
        self._default_renderer = self.renderers['']
        del self.renderers['']
        self._renderer_map = RendererMap(self.renderers)
        self._extracted_link_renderer_map = RendererMap(self.extracted_link_renderers)
        self._next_link_number = 1
        self._footer_pending_links = []
        self._in_pre = False
        self._optimise = optimise

    def _get_top(self):
        t = None
        if len(self._tag_stack) > 0:
            t = self._tag_stack[-1]
            if t.closed:
                t = None
        return t

    def _get_renderer(self, tag):
        renderer = self._renderer_map.get_for_tag(tag)
        if not renderer:
            renderer = self._default_renderer
        return renderer

    def _get_extracted_link_renderer(self, tag):
        try:
            renderer = self._extracted_link_renderer_map.get_for_tag(tag)
        except KeyError:
            renderer = None
        if not renderer:
            # This should have been matched in the map anyway
            renderer = self.extracted_link_renderers['a']
        return renderer

    def handle_starttag(self, tag, attrs):
        parent = self._get_top() or self.tree
        t = None
        if tag == 'pre':
            self._in_pre = True
        if tag in ('a', 'img'):
            t = LinkParser(
                tag,
                parent,
                attrs,
                output_format=self._output_format,
                link_placement=self._link_placement,
                image_placement=self._image_placement,
                link_reference=self._next_link_number,
                gopher_host=self._gopher_host,
                gopher_port=self._gopher_port,
            )
            placement = self._image_placement if tag == 'img' else self._link_placement
            if placement == 'footer':
                self._footer_pending_links.append(t)
            elif placement == 'after_block':
                parent.add_pending_link(t)
            if placement != 'inline':
                self._next_link_number += 1
        else:
            t = TagParser(
                tag,
                parent,
                attrs,
            )
        if not t.closed:
            self._tag_stack.append(t)
        if parent:
            parent.children.append(t)
        else:
            self.tree.append(t)

    def handle_endtag(self, tag):
        if tag in ('br', 'img'):
            # br and img tags are inherently self-closing, so if we encounter an end tag
            # we can just ignore it. I believe <br/> produces endtag calls.
            return
        top = self._get_top()
        if tag == 'pre':
            self._in_pre = False
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
        # Ignore any whitespace data on its own, unless in a pre tag
        # Pretty printed html includes a lot of this.
        # Removing ths because it removes significant whitespace between
        # adjacent tags... But I'm not convinced that pretty printing whitespace
        # won't be an issue.
        # if not self._in_pre:
        #     if len(data) == 0 or data.isspace():
        #         return
        parent = self._get_top()
        d = DataParser(parent, data, in_pre=self._in_pre)
        if parent:
            parent.children.append(d)
        else:
            # No containing tags, so add directly to the root of the tree
            # This probably indicates badly formed HTML.
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
            renderer = self._get_renderer(tag)
            if tag.tag in ('a', 'img'):
                tag.assign_renderer((
                        renderer,
                        self._get_extracted_link_renderer(tag)
                    )
                )
            else:
                tag.assign_renderer(renderer)

            self._assign_renderers(tag.children)

    def _optimise_parsed(self):
        """
        Remove extraeous whitespace to the right of the text.
        """
        parsed = self.parsed
        split = parsed.split('\n')
        optimised = [l.rstrip() for l in split]
        return '\n'.join(optimised)

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
        self._assign_renderers(self.tree.children)

        for t in self.tree.children:
            self._parsed.append(t.render(self._box))

        if self._link_placement == 'footer' and len(self._footer_pending_links) > 0:
            self._parsed.append("\n")
            for l in self._footer_pending_links:
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
        if self._optimise:
            self.parsed = self._optimise_parsed()

    def reset(self):
        super().reset()
        self._parsed = []
        self.parsed = ""
        self._tag_stack = []
        self.tree = DocumentParser()
        self._next_link_number = 1
        self._footer_pending_links = []
