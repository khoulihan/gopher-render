from . import _textwrap as textwrap
import inspect

from ._namedict import namedict

# TODO: Add additional formatting helper functions
# TODO: Add the formatting classes/functions here

def _noop(text, *args, **kwargs):
    return text


def full_justify(text, width, *args, **kwargs):
    lines = textwrap.wrap(text, width, *args, **kwargs)
    out_lines = []
    for line in lines[:-1]:
        orig_len = len(line)
        ls = line.lstrip()
        indent = ' ' * (orig_len - len(ls))
        padding_spaces = width - orig_len
        rs = ls.rstrip()
        #padding_spaces = len(ls) - len(rs)
        if padding_spaces == 0:
            out_lines.append(line)
            continue
        words = rs.split(' ')
        gaps = (len(words) - 1)
        if gaps == 0:
            out_lines.append(line)
            continue
        n, r = divmod(padding_spaces, gaps)
        narrow = ' ' * (n + 1)
        if r == 0:
            # No remainder
            out_lines.append(indent + narrow.join(words))
        else:
            wide = ' ' * (n + 2)
            out_lines.append(indent + wide.join(words[:r]) + wide + narrow.join(words[r:]))
    if len(lines) > 0:
        out_lines.append(lines[-1])
    return '\n'.join(out_lines)


def left_justify(text, width, *args, **kwargs):
    lines = textwrap.wrap(text, width, *args, **kwargs)
    return '\n'.join(lines)


def right_justify(text, width, *args, **kwargs):
    lines = textwrap.wrap(text, width, *args, **kwargs)
    righted = [right(line, width) for line in lines]
    return '\n'.join(righted)


def center_justify(text, width, *args, **kwargs):
    lines = textwrap.wrap(text, width, *args, **kwargs)
    centered = [center(line, width) for line in lines]
    return '\n'.join(centered)


def center(text, width, *args, **kwargs):
    if not width:
        return _noop(text)
    return text.center(width, *args, **kwargs)


def right(text, width, *args, **kwargs):
    if not width:
        return _noop(text)
    return text.rjust(width, *args, **kwargs)


justifications = {
    'none': _noop,
    'full': full_justify,
    'center': center_justify,
    'left': left_justify,
    'right': right_justify,
}

# TODO: The string method capitalize() only capitalizes the first character
# while the actual method to uppercase everything is upper(). This function
# should probably match the method name
# TODO: Should may deal with casing the same way as the justifications...
def capitalize(text):
    return text.upper()


def spread(text, spread_char, count):
    s = spread_char * count
    return s.join(text)


class BoxSide:
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def _get_template_width(template):
    # TODO: This needs to be more sophisticated
    return len(template) - 2


class Box(object):
    """
    A rudimentary nesting box model where left and right margins are inherited.
    """
    def __init__(
        self,
        width=67,
        margin=[0,0,0,0],
        padding=[0,0,0,0],
        border=[0,0,0,0],
        line_template=None,
        parent=None
    ):
        if margin == None:
            margin = [0,0,0,0]
        if padding == None:
            padding = [0,0,0,0]
        if border == None:
            border = [0,0,0,0]
        self.width = width
        self.margin = margin[:]
        # TOP and BOTTOM are ignored in these totals
        self.total_margin = margin[:]
        self.padding = padding[:]
        self.total_padding = padding[:]
        self.border = border[:]
        self.total_border = border[:]
        self.line_template = line_template
        self.line_template_padding = 0
        self.total_line_template_padding = 0
        if self.line_template:
            self.line_template_padding = _get_template_width(self.line_template)
        self.parent = parent
        # If a parent was provided, its width overrides the provided width
        # and its margins are added to the provided margins to give total margins
        if parent:
            self.parent = parent
            self.width = parent.width
            self.total_margin[BoxSide.LEFT] = self.margin[BoxSide.LEFT] + parent.total_margin[BoxSide.LEFT]
            self.total_margin[BoxSide.RIGHT] = self.margin[BoxSide.RIGHT] + parent.total_margin[BoxSide.RIGHT]
            self.total_padding[BoxSide.LEFT] = self.padding[BoxSide.LEFT] + parent.total_padding[BoxSide.LEFT]
            self.total_padding[BoxSide.RIGHT] = self.padding[BoxSide.RIGHT] + parent.total_padding[BoxSide.RIGHT]
            self.total_border[BoxSide.LEFT] = self.border[BoxSide.LEFT] + parent.total_border[BoxSide.LEFT]
            self.total_border[BoxSide.RIGHT] = self.border[BoxSide.RIGHT] + parent.total_border[BoxSide.RIGHT]
            self.total_line_template_padding = self.line_template_padding + parent.total_line_template_padding

    def inner_width_excluding_line_template():
        doc = """
        The width actually available to the element's inner content,
        excluding the extra padding created by the line_template.

        Block content should be wrapped to this width.
        """
        def fget(self):
            return self.width - (
                self.total_margin[BoxSide.LEFT] + self.total_margin[BoxSide.RIGHT] +
                self.total_padding[BoxSide.LEFT] + self.total_padding[BoxSide.RIGHT] +
                self.total_border[BoxSide.LEFT] + self.total_border[BoxSide.RIGHT] +
                self.total_line_template_padding
            )
        return locals()
    inner_width_excluding_line_template = property(**inner_width_excluding_line_template())

    def inner_width():
        doc = "The width actually available to the element's inner content."
        def fget(self):
            return self.width - (
                self.total_margin[BoxSide.LEFT] + self.total_margin[BoxSide.RIGHT] +
                self.total_padding[BoxSide.LEFT] + self.total_padding[BoxSide.RIGHT] +
                self.total_border[BoxSide.LEFT] + self.total_border[BoxSide.RIGHT]
            )
        return locals()
    inner_width = property(**inner_width())

    def padded_width():
        doc = "The width of the element including the padding."
        def fget(self):
            # This has to include the width of the local line template
            # but exclude any added by further up the hierarchy.
            return self.width - (
                self.total_margin[BoxSide.LEFT] + self.total_margin[BoxSide.RIGHT] +
                self.total_border[BoxSide.LEFT] + self.total_border[BoxSide.RIGHT] +
                (self.total_line_template_padding - self.line_template_padding)
            )
        return locals()
    padded_width = property(**padded_width())

    def bordered_width():
        doc = "The width of the element including the padding."
        def fget(self):
            return self.width - (
                self.total_margin[BoxSide.LEFT] + self.total_margin[BoxSide.RIGHT]
            )
        return locals()
    bordered_width = property(**bordered_width())

    def __repr__(self):
        return "Box [ m: {}, p: {}, b: {}, w: {}, iw: {} ]".format(
            self.margin,
            self.padding,
            self.border,
            self.width,
            self.inner_width
        )


class Formatter(object):
    """
    Base formatter.
    """

    def __init__(self, *args, **kwargs):
        self.defaults = {}
        self.defaults.update(kwargs)

    def __extract_classes(self, attrs):
        classes = ""
        for attr in attrs:
            if attr[0] == 'class':
                classes = attr[1]
        return classes.split()

    def _get_format(self, tag, **kwargs):
        """
        Retrieve a copy of the formatting settings, updated as necessary
        to reflect the context.

        Base implementation just returns the defaults. Inheriting classes can
        override this to change formatting behaviour based on tag, classes,
        or other attributes.
        """
        return self.defaults.copy()

    def __call__(self, tag, content, **kwargs):
        kwargs['classes'] = self.__extract_classes(
            kwargs.get('attrs', {})
        )
        kwargs['settings'] = self._get_format(tag, **kwargs)
        kwargs['box'] = self.get_box(tag, kwargs)
        return self.format(tag, content, **kwargs)

    def get_box(self, tag, context):
        """
        Get a box adjusted for the context.

        Base implementation just wraps the parent box without modifying it.
        Inheriting classes can override this to set margins for an element.
        """
        parent = context.get('parent_box', None)
        if parent:
            return Box(parent=parent)
        return None

    def format(self, tag, content, **kwargs):
        return content


class _RendererMeta(type):
    """
    This metaclass ensures that every Renderer derived class has its own
    settings dictionary, thus avoiding accidentally overriding settings in a
    base class.
    """

    def __new__(cls, name, bases, namespace, **kwds):
        # namespace only contains the names defined in the class that is being
        # created - super().__new__ will combine it with the base classes
        # Therefore, add the settings before that if necessary!
        if not 'settings' in namespace:
            namespace['settings'] = namedict()
        else:
            s = namespace['settings']
            if not isinstance(s, namedict):
                namespace['settings'] = namedict(s)

        r = super().__new__(cls, name, bases, namespace, **kwds)
        return r


class Renderer(metaclass=_RendererMeta):
    """
    Base Renderer.
    """

    """
    The renderer settings. Settings from all bases classes will be aggregated
    into a single new dictionary when Renderer instances are created.
    """
    settings = namedict()

    def __new__(cls, *args, **kwargs):
        """
        Combine the base_settings of all base classes into a single settings
        dictionary on the newly created class instance.
        """
        s = namedict()
        all_classes = inspect.getmro(cls)
        all_bases = []
        for klass in all_classes[::-1]:
            if hasattr(klass, 'settings'):
                if klass.settings not in all_bases:
                    all_bases.append(klass.settings)
        for base in all_bases:
            s.update(base)

        instance = super().__new__(cls)
        instance.settings = s

        return instance

    def __init__(self, tag, **kwargs):
        # This will be a TagParser instance
        self.tag = tag
        self.context = kwargs
        self._adjust_settings()

    def __getattribute__(self, name):
        """
        Have to make sure that the settings map is always a namedict.
        """
        if name == "settings":
            s = super().__getattribute__(name)
            if not isinstance(s, namedict):
                s = namedict(s)
            return s
        return super().__getattribute__(name)

    def _adjust_settings(self):
        """
        Adjust the formatting settings.
        """
        # If there is a settings dictionary in the context, update the
        # settings with that.
        local_settings = self.context.get('settings', None)
        if local_settings is not None:
            self.settings.update(local_settings)

    def render(self, content):
        """
        Render the provided content.
        """
        return content


class NonRenderer(Renderer):
    """
    This Renderer... does not render! The render() method will always return an
    empty string.
    """
    def render(self, content):
        """
        Return an empty string to remove all contents from the output.
        """
        return ""


class InlineRenderer(Renderer):

    settings = namedict(
        template="{}",
        capitalized=False,
    )

    def render(self, content):
        settings = self.settings
        capitalize_func = capitalize if settings['capitalized'] else _noop
        return settings.template.format(
            capitalize_func(super().render(content))
        )


class BlockRenderer(Renderer):

    settings = namedict(
        border=['','','',''],
        margin=[0,0,0,0],
        padding=[0,0,0,0],
    )

    def __init__(self, tag, **kwargs):
        super().__init__(tag, **kwargs)
        # TODO: What if None, or wrong length?
        border = self.settings.border
        self._border_width = [ len(b) for b in border ]
        self.box = self._generate_box()

    def _generate_box(self):
        """
        Create a box adjusted for the context.

        This class adds a left and right margin if set for the formatter.
        """
        context = self.context
        parent = context.get('parent_box', None)
        settings = self.settings

        if parent:
            # TODO: What if None?
            margin = settings.get('margin', None)
            padding = settings.get('padding', None)
            border = self._border_width
            return Box(
                margin=margin,
                padding=padding,
                border=border,
                parent=parent
            )
        return None

    def _outer_render(self, content):
        box = self.box
        # Not sure if splitlines of split('\n') is best here
        lines = content.splitlines(keepends=True)
        indented = "".join([
            "{}{}".format(' ' * box.margin[BoxSide.LEFT], l)
            for l in lines
        ])
        return "{}{}{}".format(
            '\n' * box.margin[BoxSide.TOP],
            indented,
            '\n' * box.margin[BoxSide.BOTTOM],
        )

    def _inner_render(self, content):
        # TODO: This should really be wrapped, since the boxing depends on
        # the width of the content being correct. Do a naive wrapping here
        # and allow derived classes to do more sophisticated things.
        return content

    def _border_render(self, content):
        box = self.box
        settings = self.settings
        borders = settings.border
        # Not sure if splitlines of split('\n') is best here
        lines = content.split('\n')
        padded = [
            "{}{}{}{}{}".format(
                borders[BoxSide.LEFT],
                ' ' * box.padding[BoxSide.LEFT],
                l,
                ' ' * (box.padded_width - (box.padding[BoxSide.LEFT] + len(l))),
                borders[BoxSide.RIGHT]
            ) for l in lines
        ]

        vertical_pad = "{}{}{}".format(
            borders[BoxSide.LEFT],
            ' ' * box.padded_width,
            borders[BoxSide.RIGHT]
        )
        if box.padding[BoxSide.TOP] > 0:
            padded[0:0] = [vertical_pad] * box.padding[BoxSide.TOP]
        if box.padding[BoxSide.BOTTOM] > 0:
            padded.extend([vertical_pad] * box.padding[BoxSide.BOTTOM])

        if box.border[BoxSide.TOP] > 0:
            for c in borders[BoxSide.TOP][::-1]:
                padded.insert(0, c * box.bordered_width)
        if box.border[BoxSide.BOTTOM] > 0:
            for c in borders[BoxSide.BOTTOM]:
                padded.append(c * box.bordered_width)

        return "\n".join(padded)

    def render(self, content):
        return self._outer_render(
            self._border_render(
                self._inner_render(
                    super().render(content)
                )
            )
        )


class HeaderRenderer(BlockRenderer):

    settings = dict(
        template="{}",
        capitalized=False,
        spread=0,
        spread_char=" ",
        centered=False,
        underlined=False,
        underline_char="=",
        underline_full=False,
        margin=[1,0,1,0]
    )

    def _inner_render(self, content):
        # TODO: This should really be wrapped, since the boxing depends on
        # the width of the content being correct.
        settings = self.settings
        center_func = center if settings.centered else _noop
        capitalize_func = capitalize if settings.capitalized else _noop
        spread_func = spread if settings.spread > 0 else _noop
        box = self.box
        width = box.inner_width
        inner = settings.template.format(
            spread_func(
                capitalize_func(
                    super()._inner_render(content)
                ),
                settings.spread_char,
                settings.spread
            )
        )
        underline = ""
        if settings['underlined']:
            underline_len = width if settings.underline_full else len(inner)
            underline = "{}".format(settings.underline_char * underline_len, width)
            return "{}\n{}".format(
                center_func(inner, width),
                center_func(underline, width),
            )
        else:
            return center_func(inner, width)


class MarkdownHeaderRenderer(HeaderRenderer):
    """
    Renderer for markdown style headers.

    This renderer will automatically use the correct format for the header type.
    """

    def _adjust_settings(self):
        """
        Adjust the formatting settings.
        """
        super()._adjust_settings()
        # TODO: Check that the tag is actually a header!
        h_type = int(self.tag.tag[1])
        hashes = "#" * h_type
        self.settings.template = "{} {} {}".format(hashes, "{}", hashes)


class ParagraphRenderer(BlockRenderer):
    """
    Default Renderer for paragraphs and paragraph-like blocks. Content is generally
    wrapped and justified, but can be manipulated in several other ways.
    """

    settings = dict(
        initial_indent=0,
        subsequent_indent=0,
        justification='left',
        capitalized=False,
        fix_sentence_endings=True,
        break_long_words=True,
        skip_for_code_or_pre=True,
        margin=[1,0,1,0],
        line_template="{}",
    )

    # TODO: Very repetitive
    def _generate_box(self):
        """
        Create a box adjusted for the context.

        This class adds a left and right margin if set for the formatter.
        """
        context = self.context
        parent = context.get('parent_box', None)
        settings = self.settings

        if parent:
            # TODO: What if None?
            margin = settings.get('margin', None)
            padding = settings.get('padding', None)
            line_template = settings.get('line_template', None)
            border = self._border_width
            return Box(
                margin=margin,
                padding=padding,
                border=border,
                parent=parent,
                line_template=line_template,
            )
        return None

    def _skip(self, children):
        return len(children) == 1 and children[0].tag in ['code', 'pre']

    def _inner_render(self, content):
        settings = self.settings

        # TODO: There may be other circumstances where we need to skip
        # However, every instance I've encountered so far has been resolvable
        # by correcting markdown or the markdown parser settings, so...
        if settings.skip_for_code_or_pre and self._skip(self.tag.children):
            return content

        justify_func = justifications[settings.justification]
        capitalize_func = capitalize if settings.capitalized else _noop

        justify_args = dict(
            initial_indent=' '*settings.initial_indent,
            subsequent_indent=' '*settings.subsequent_indent,
        )
        for textwrap_arg in [
            'fix_sentence_endings',
            'break_long_words',
            'break_on_hyphens',
            'placeholder',
            'drop_whitespace',
            'replace_whitespace',
            'expand_tabs',
            'tabsize',
        ]:
            if textwrap_arg in settings:
                justify_args[textwrap_arg] = settings[textwrap_arg]

        width = self.box.inner_width_excluding_line_template
        # TODO: Is a block or line template useful here?
        inner = capitalize_func(content)
        #template = settings['template']
        inner_split = inner.split('\n')
        justified = []
        for chunk in inner_split:
            # I think we can safely strip here because the paragraph renderer
            # is expected to reformat its contents...
            j = justify_func(chunk.strip(), width, **justify_args)
            justified.append(j)
        justified = '\n'.join(justified)
        just_split = justified.split("\n")
        template = self.settings.line_template
        return "\n".join(
            [template.format(line) for line in just_split]
        )


# TODO: Need to differentiate between code spans and code blocks, somehow!
# 1) This formatter could check if it has siblings by checking the parent's children
#    (can't just check the parent because block could be just a code inside a p)
# 2) The parser could keep an eye out for code blocks and update the assigned formatter
# 3) Could check the children - if any child data has a newline in it, then it's a block, innit?
# 4) Could have the paragraph formatter skip the wrapping, but not the before and after
#    padding if it has only a code child

# TODO: I was under the impression that this could be sometimes a block and
# sometimes inline, but now I'm not so sure. If a code block is a child of a pre,
# then the pre will be allowed to do the formatting, and this renderer will only
# handle inline rendering.
class CodeRenderer(InlineRenderer):

    settings = dict(
        block_template="```\n{}\n```\n",
        inline_template="`{}`"
    )

    def render(self, content):
        settings = self.settings

        parent = self.tag.parent
        if parent and hasattr(parent, 'tag') and parent.tag == 'pre':
            # The pre will handle the formatting
            return content
        if '\n' in content:
            return settings['block_template'].format(content)
        return settings['inline_template'].format(content)


class PreRenderer(BlockRenderer):

    settings = dict(
        line_template="{}",
        indent=4,
        margin=[1,0,1,0],
    )

    def _inner_render(self, content):
        settings = self.settings

        lines = content.splitlines()
        formatted = []
        for line in lines:
            formatted.append(
                "{}{}".format(
                    " "*settings.indent,
                    settings.line_template.format(line)
                )
            )
        return "\n".join(formatted)


class LinkRenderer(InlineRenderer):

    settings = dict(
        templates={
            "reference": "[{content}][{link_reference}]",
            "inline": ["[{content}]({href})", '[{content}]({href} "{title}")']
        },
        capitalized=False,
    )

    # TODO: Seems like this could be improved. Something like the extracted renderer below
    def render(self, content):
        settings = self.settings
        capitalize_func = capitalize if settings.capitalized else _noop
        if self.context["link_placement"] == "inline":
            if "title" in self.context and self.context["title"]:
                return settings.templates["inline"][1].format(
                    content=capitalize_func(super().render(content)),
                    href=self.context["href"],
                    title=self.context["title"],
                )
            else:
                return settings.templates["inline"][0].format(
                    content=capitalize_func(super().render(content)),
                    href=self.context["href"],
                )
        else:
            return settings.templates["reference"].format(
                content=capitalize_func(super().render(content)),
                link_reference=self.context["link_reference"]
            )


class ExtractedLinkRenderer(BlockRenderer):

    # TODO: The block rendering is adding an entire line's worth of whitespace at
    # the end of the line for extracted text links.
    settings = dict(
        templates=["\n[{link_reference}] {description}: {href}", '\n[{link_reference}] {description}: {href} "{title}"'],
        gophermap_template="{type}[{link_reference}] {description}\t{selector}\t{host}\t{port}\n",
        max_link_description=10,
    )

    def _inner_render(self, content):
        settings = self.settings
        output_format = self.context['output_format']
        href = self.context['href']
        title = self.context['title']

        # TODO: Surely this truncation should be optional?
        max_link_description = settings.max_link_description
        trimming = len(content) > max_link_description
        content = content.strip()[:max_link_description]
        if trimming:
            content = "{}...".format(content)

        if output_format == 'gophermap':
            description = title if title is not None else content
            gopher_link = self.context['gopher_link']
            link_ref = self.context["link_reference"]
            return settings.gophermap_template.format(
                description=super()._inner_render(description),
                link_reference=link_ref,
                selector=gopher_link['selector'],
                type=gopher_link['type'],
                host=gopher_link['host'],
                port=gopher_link['port'],
            )
        else:
            template = settings.templates[0]
            keywords = dict(
                description=super()._inner_render(content),
                link_reference=self.context["link_reference"],
                href=href,
            )
            if title:
                template = settings.templates[1]
                keywords["title"] = title
            return template.format(
                **keywords
            )

    def _outer_render(self, content):
        output_format = self.context['output_format']
        if output_format == "gophermap":
            # A left margin would not be acceptable for gophermap links, so only
            # apply the top and bottom margins, if any.
            box = self.box
            return "{}{}{}".format(
                '\n' * box.margin[BoxSide.TOP],
                content,
                '\n' * box.margin[BoxSide.BOTTOM],
            )
        return super()._outer_render(content)

    def render(self, content):
        output_format = self.context['output_format']
        if output_format == "gophermap":
            # A border would not be acceptable for gophermap links, so skip
            # that render step.
            return self._outer_render(
                self._inner_render(
                    content
                )
            )
        return super().render(content)


class ImageRenderer(InlineRenderer):

    settings = dict(
        templates={
            "reference": "[{title}][{link_reference}]",
            "inline": "![{title}]({href})"
        },
        capitalized=False,
    )

    def render(self, content):
        settings = self.settings
        capitalize_func = capitalize if settings.capitalized else _noop
        if self.context["image_placement"] == "inline":
            if "title" in self.context and self.context["title"]:
                return settings.templates["inline"].format(
                    href=self.context["href"],
                    title=self.context["title"],
                )
            else:
                return settings.templates["inline"].format(
                    href=self.context["href"],
                    title="Image",
                )
        else:
            if "title" in self.context and self.context["title"]:
                title = self.context["title"]
            else:
                title = "Image"
            return settings.templates["reference"].format(
                title=title,
                link_reference=self.context["link_reference"]
            )


class ExtractedImageLinkRenderer(BlockRenderer):

    settings = dict(
        templates=["\n[{link_reference}] {description}: {href}", '\n[{link_reference}] {description}: {href} "{title}"'],
        gophermap_template="{type}[{link_reference}] {description}\t{selector}\t{host}\t{port}\n",
        max_link_description=10,
    )

    def _inner_render(self, content):
        settings = self.settings
        output_format = self.context['output_format']
        href = self.context['href']
        if 'title' in self.context and self.context['title']:
            title = self.context['title']
        else:
            title = "Image"

        # TODO: Surely this truncation should be optional?
        max_link_description = settings.max_link_description
        trimming = len(title) > max_link_description
        trimmed_title = title.strip()[:max_link_description]
        if trimming:
            trimmed_title = "{}...".format(trimmed_title)

        if output_format == 'gophermap':
            description = trimmed_title
            gopher_link = self.context['gopher_link']
            link_ref = self.context["link_reference"]
            return settings.gophermap_template.format(
                description=super()._inner_render(description),
                link_reference=link_ref,
                selector=gopher_link['selector'],
                type=gopher_link['type'],
                host=gopher_link['host'],
                port=gopher_link['port'],
            )
        else:
            template = settings.templates[0]
            keywords = dict(
                description=super()._inner_render(trimmed_title),
                link_reference=self.context["link_reference"],
                href=href,
            )
            if trimming:
                template = settings.templates[1]
                keywords["title"] = title
            return template.format(
                **keywords
            )


# TODO: i tags should also have a renderer for icons
class EmRenderer(InlineRenderer):
    """
    Renderer for <em> tags. Usually also for <i> tags.
    """

    settings = dict(
        template="_{}_"
    )


class StrongRenderer(InlineRenderer):
    """
    Renderer for <strong> tags. Usually also for <b> tags.
    """

    settings = dict(
        template="**{}**"
    )


class UnderlineRenderer(InlineRenderer):
    """
    Renderer for <u> tags.
    """

    settings = dict(
        template="_{}_"
    )


class StrikethroughRenderer(InlineRenderer):
    """
    Renderer for <s> tags.
    """

    settings = dict(
        template="~~{}~~"
    )


class BreakRenderer(InlineRenderer):
    """
    Renderer for <br> tags.

    Note that these must be closed (<br/>) or they will break the parser.
    """

    settings = dict(
        template="{}",
    )

    def render(self, content):
        settings = self.settings
        # These tags should not have content, so it is ignored.
        return settings.template.format(
            super().render('\n')
        )


class BlockQuoteRenderer(BlockRenderer):
    settings = dict(
        line_template="> {}",
        margin=[1,0,1,0],
    )

    # TODO: Very repetitive
    def _generate_box(self):
        """
        Create a box adjusted for the context.

        This class adds a left and right margin if set for the formatter.
        """
        context = self.context
        parent = context.get('parent_box', None)
        settings = self.settings

        if parent:
            # TODO: What if None?
            margin = settings.get('margin', None)
            padding = settings.get('padding', None)
            line_template = settings.get('line_template', None)
            border = self._border_width
            return Box(
                margin=margin,
                padding=padding,
                border=border,
                parent=parent,
                line_template=line_template,
            )
        return None

    def _inner_render(self, content):
        settings = self.settings

        width = self.box.inner_width

        content_split = content.splitlines()
        template = self.settings.line_template

        return "\n".join(
            [template.format(line) for line in content_split]
        )


class ListRenderer(BlockRenderer):
    settings = dict(
        margin=[1,0,1,0],
        padding=[0,0,0,0]
    )


class ListItemRenderer(BlockRenderer):
    settings = dict(
        line_template="* {}",
        margin=[1,0,0,0],
        initial_indent=0,
        subsequent_indent=0,
        justification='left',
        capitalized=False,
        fix_sentence_endings=True,
        break_long_words=True,
    )

    # TODO: Very repetitive
    def _generate_box(self):
        """
        Create a box adjusted for the context.

        This class adds a line template if set for the formatter.
        """
        context = self.context
        parent = context.get('parent_box', None)
        settings = self.settings

        if parent:
            # TODO: What if None?
            margin = settings.get('margin', None)
            padding = settings.get('padding', None)
            line_template = settings.get('line_template', None)
            border = self._border_width
            return Box(
                margin=margin,
                padding=padding,
                border=border,
                parent=parent,
                line_template=line_template,
            )
        return None

    def _inner_render(self, content):
        settings = self.settings

        justify_func = justifications[settings.justification]
        capitalize_func = capitalize if settings.capitalized else _noop

        justify_args = dict(
            initial_indent=' '*settings.initial_indent,
            subsequent_indent=' '*settings.subsequent_indent,
        )
        for textwrap_arg in [
            'fix_sentence_endings',
            'break_long_words',
            'break_on_hyphens',
            'placeholder',
            'drop_whitespace',
            'replace_whitespace',
            'expand_tabs',
            'tabsize',
        ]:
            if textwrap_arg in settings:
                justify_args[textwrap_arg] = settings[textwrap_arg]

        width = self.box.inner_width_excluding_line_template
        # TODO: Is a block or line template useful here?
        inner = capitalize_func(content)
        justified = justify_func(inner, width, **justify_args)
        just_split = justified.split("\n")
        template = self.settings.line_template
        # The template only applies for the first line in this case, the rest
        # are just padded by its width.
        out = [template.format(just_split[0])]
        template_width = self.box.line_template_padding
        if len(just_split) > 1:
            out.extend(['{}{}'.format(' ' * template_width, line) for line in just_split[1:]])
        return "\n".join(out)


class OrderedListItemRenderer(ListItemRenderer):
    settings = dict(
        line_template="{0}. {1}",
        start_index=1,
        step=1,
    )

    def __init__(self, tag, **kwargs):
        # Determine the ordinal and prepare a template based on it before the
        # box gets generated, otherwise the width will be incorrect.
        self.order = self._get_ordinal(
            tag,
            self.settings.start_index,
            self.settings.step,
        )
        self.settings.line_template = self.settings.line_template.format(
            self.order,
            '{}'
        )
        super().__init__(tag, **kwargs)

    def _get_ordinal(self, tag, start_index, step):
        return (tag.parent.children.index(tag) * step) + start_index


class DefinitionListRenderer(BlockRenderer):
    settings = dict(
        margin=[1,0,1,0],
        padding=[0,0,0,0]
    )


class DefinitionListTermHeaderRenderer(HeaderRenderer):
    settings = dict(
        margin=[2,0,0,0],
        padding=[0,0,0,0]
    )


class DefinitionListItemRenderer(BlockRenderer):
    settings = dict(
        line_template=": {}",
        margin=[1,0,0,0],
        initial_indent=0,
        subsequent_indent=0,
        justification='left',
        capitalized=False,
        fix_sentence_endings=True,
        break_long_words=True,
    )

    # TODO: Very repetitive
    def _generate_box(self):
        """
        Create a box adjusted for the context.

        This class adds a line template if set for the formatter.
        """
        context = self.context
        parent = context.get('parent_box', None)
        settings = self.settings

        if parent:
            # TODO: What if None?
            margin = settings.get('margin', None)
            padding = settings.get('padding', None)
            line_template = settings.get('line_template', None)
            border = self._border_width
            return Box(
                margin=margin,
                padding=padding,
                border=border,
                parent=parent,
                line_template=line_template,
            )
        return None

    def _inner_render(self, content):
        settings = self.settings

        justify_func = justifications[settings.justification]
        capitalize_func = capitalize if settings.capitalized else _noop

        justify_args = dict(
            initial_indent=' '*settings.initial_indent,
            subsequent_indent=' '*settings.subsequent_indent,
        )
        for textwrap_arg in [
            'fix_sentence_endings',
            'break_long_words',
            'break_on_hyphens',
            'placeholder',
            'drop_whitespace',
            'replace_whitespace',
            'expand_tabs',
            'tabsize',
        ]:
            if textwrap_arg in settings:
                justify_args[textwrap_arg] = settings[textwrap_arg]

        width = self.box.inner_width_excluding_line_template
        # TODO: Is a block or line template useful here?
        inner = capitalize_func(content)
        justified = justify_func(inner, width, **justify_args)
        just_split = justified.split("\n")
        template = self.settings.line_template
        # The template only applies for the first line in this case, the rest
        # are just padded by its width.
        out = [template.format(just_split[0])]
        template_width = self.box.line_template_padding
        if len(just_split) > 1:
            out.extend(['{}{}'.format(' ' * template_width, line) for line in just_split[1:]])
        return "\n".join(out)


ansi_colours = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}
ANSI_BACKGROUND_COLOUR_OFFSET = 10
ANSI_FONT_OFFSET = 10

# Codes to activate and deactive effects - except colours and fonts.
ansi_escape_sequences = {
    "bold": (1, 22),
    "faint": (2, 22),
    "italic": (3, 23),
    "fraktur": (20, 23),
    "underline": (4, 24),
    "slow_blink": (5, 25),
    "rapid_blink": (6, 25),
    "invert": (7, 27),
    "conceal": (8, 28),
    "crossed_out": (9, 29),
    "framed": (51, 54),
    "encircled": (52, 54),
    "overlined": (53, 55),
}

ANSI_ESCAPE_SEQUENCE = "\033[{}m"

def _parse_html_colour(colour):
    """
    Return a thruple of the red, green and blue elements of an HTML colour string
    """
    colour = colour.lstrip('#')
    if len(colour) == 3:
        colour = "{}{}{}".format(
            colour[0] * 2,
            colour[1] * 2,
            colour[2] * 2,
        )
    return (
        int(colour[0:2], base=16),
        int(colour[2:4], base=16),
        int(colour[4:6], base=16),
    )

def _get_sequence_for_colour(colour, is_background=False):
    # Colours can be specified in one of four ways
    #    - ANSI 4-bit colour name
    #    - Number of colour in the 8-bit palette
    #    - Tuple containing (r, g, b) values
    #    - HTML #rgb or #rrggbb values
    if colour in ansi_colours:
        offset = 0
        if is_background:
            offset = ANSI_BACKGROUND_COLOUR_OFFSET
        return "{}".format(ansi_colours[colour] + offset)

    control = "48" if is_background else "38"
    if isinstance(colour, int):
        return "{};5;{}".format(control, colour)

    if isinstance(colour, str):
        # Try to parse as an html colour- TODO
        colour = _parse_html_colour(colour)

    # Fall back to a tuple
    return "{};2;{};{};{}".format(
        control,
        colour[0],
        colour[1],
        colour[2],
    )


class AnsiEscapeCodeRenderer(InlineRenderer):
    """
    Inline renderer that can style text using ANSI terminal escape sequences.
    """

    settings = dict(
        foreground_colour=None,
        background_colour=None,
        font=None,
        bold=False,
        underline=False,
        invert=False,
        italic=False, # Apparently not widely supported
        faint=False, # Apparently not widely supported
        slow_blink=False,
        rapid_blink=False, # Apparently not widely supported
        conceal=False, # Apparently not widely supported
        crossed_out=False, # Apparently not widely supported
        fraktur=False, # Apparently hardly ever supported. Don't know what it is!
        framed=False,
        encircled=False,
        overlined=False,
        normalise=False,
    )

    def render(self, content):
        settings = self.settings
        inner = super().render(content)
        normalise = settings.normalise
        enable = []
        disable = []

        for effect in ansi_escape_sequences:
            if settings[effect]:
                enable.append(
                    ANSI_ESCAPE_SEQUENCE.format(
                        ansi_escape_sequences[effect][0]
                    )
                )
                if not normalise:
                    disable.append(
                        ANSI_ESCAPE_SEQUENCE.format(
                            ansi_escape_sequences[effect][1]
                        )
                    )

        # Fonts
        if settings.font is not None:
            enable.append(ANSI_ESCAPE_SEQUENCE.format(setting.font + ANSI_FONT_OFFSET))
            if not normalise:
                disable.append(ANSI_ESCAPE_SEQUENCE.format(0 + ANSI_FONT_OFFSET))

        # Colours
        if settings.foreground_colour:
            enable.append(
                ANSI_ESCAPE_SEQUENCE.format(
                    _get_sequence_for_colour(
                        settings.foreground_colour
                    )
                )
            )
            if not normalise:
                # Default foreground
                disable.append(ANSI_ESCAPE_SEQUENCE.format(39))
        if settings.background_colour:
            enable.append(
                ANSI_ESCAPE_SEQUENCE.format(
                    _get_sequence_for_colour(
                        settings.background_colour,
                        is_background=True
                    )
                )
            )
            if not normalise:
                # Default background
                disable.append(ANSI_ESCAPE_SEQUENCE.format(49))

        if normalise:
            disable.append(ANSI_ESCAPE_SEQUENCE.format(0))

        return "{}{}{}".format(
            "".join(enable),
            inner,
            "".join(disable)
        )
