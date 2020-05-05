import textwrap

# TODO: Add additional formatting helper functions
# TODO: Add the formatting classes/functions here

def _noop(text, *args, **kwargs):
    return text

# TODO: Implement line_template in justification funcs
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


def capitalize(text):
    return text.capitalize()


class Box(object):
    """
    A rudimentary nesting box model where left and right margins are inherited.
    """
    def __init__(
        self,
        width=67,
        left=0,
        right=0,
        top=0,
        bottom=0,
        parent=None
    ):
        self.width = width
        self.left = left
        self.total_left = left
        self.right = right
        self.total_right = right
        self.top = top
        self.bottom = bottom
        self.parent = parent
        # If a parent was provided, its width overrides the provided width
        # and its margins are added to the provided margins to give total margins
        if parent:
            self.parent = parent
            self.width = parent.width
            self.total_left = self.left + parent.total_left
            self.total_right = self.right + parent.total_right

    def effective_width():
        doc = "The width actually available to the element."
        def fget(self):
            return self.width - (self.total_left + self.total_right)
        return locals()
    effective_width = property(**effective_width())

    def __repr__(self):
        return "Box [ t: {}, b: {}, l: {}, r: {}, w: {}, ew: {} ]".format(
            self.top,
            self.bottom,
            self.left,
            self.right,
            self.width,
            self.effective_width
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
        return self.defaults

    def __call__(self, tag, content, **kwargs):
        kwargs['classes'] = self.__extract_classes(
            kwargs.get('attrs', {})
        )
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


class BoxFormatter(Formatter):
    def get_box(self, tag, context):
        """
        Get a box adjusted for the context.

        This class adds a left and right margin if set for the formatter.
        """
        parent = context.get('parent_box', None)
        if parent:
            left = self.defaults.get('margin_left', 0)
            right = self.defaults.get('margin_right', 0)
            top = self.defaults.get('margin_top', 0)
            bottom = self.defaults.get('margin_bottom', 0)
            return Box(
                top=top,
                bottom=bottom,
                left=left,
                right=right,
                parent=parent
            )
        return None

    def format(self, tag, content, **kwargs):
        box = self.get_box(tag, kwargs)
        # Not sure if splitlines of split('\n') is best here
        lines = content.splitlines(keepends=True)
        indented = "".join([
            "{}{}".format(' ' * box.left, l)
            for l in lines
        ])
        return "{}{}{}".format(
            '\n' * box.top,
            indented,
            '\n' * box.bottom,
        )


class HeaderFormatter(BoxFormatter):
    """
    template="{}",
    centered=True,
    capitalized=False,
    underlined=False,
    underline_char="=",
    underline_full=False,
    margin_top=2,
    margin_bottom=1
    """

    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            template="{}",
            centered=True,
            capitalized=False,
            underlined=False,
            underline_char="=",
            underline_full=False,
            margin_top=1,
            margin_bottom=2
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)
        center_func = center if settings['centered'] else _noop
        capitalize_func = capitalize if settings['capitalized'] else _noop
        box = self.get_box(tag, kwargs)
        print(box)
        width = box.effective_width
        inner = capitalize_func(
            settings['template'].format(
                content
            )
        )
        underline = ""
        if settings['underlined']:
            underline_len = width if settings['underline_full'] else len(inner)
            underline = "{}".format(settings['underline_char'] * underline_len, width)
            return super().format(
                tag,
                "{}\n{}".format(
                    center_func(inner, width),
                    center_func(underline, width),
                ),
                **kwargs
            )
        else:
            return super().format(
                tag,
                center_func(inner, width),
                **kwargs
            )
        # return "{}{}\n{}{}".format(
        #     "\n"*settings['margin_top'],
        #     center_func(inner, width),
        #     center_func(underline, width),
        #     "\n"*settings['margin_bottom']
        # )


class ParagraphFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            template="{}",
            line_template="{}",
            indent=0,
            padding_right=0,
            initial_indent=8,
            justification='full',
            capitalized=False,
            fix_sentence_endings=True,
            lines_above=1,
            lines_below=1,
            skip_for_code_or_pre=True
        )
        self.defaults.update(kwargs)

    def _skip(self, children):
        return len(children) == 1 and children[0].tag in ['code', 'pre']

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)

        if settings['skip_for_code_or_pre'] and self._skip(kwargs['children']):
            return "{}{}{}".format(
                "\n"*settings['lines_above'],
                super().format(tag, content, **settings),
                "\n"*settings['lines_below']
            )

        justify_func = justifications[settings['justification']]
        capitalize_func = capitalize if settings['capitalized'] else _noop

        justify_args = dict(
            initial_indent=' '*settings['initial_indent'],
            subsequent_indent=' '*settings['indent'],
            #line_template=settings['line_template'],
        )
        for textwrap_arg in [
            'fix_sentence_endings',
            'break_long_words',
            'break_on_hyphens',
            'break_on_hyphens',
            'placeholder',
            'drop_whitespace',
            'replace_whitespace',
            'expand_tabs',
            'tabsize',
        ]:
            if textwrap_arg in settings:
                justify_args[textwrap_arg] = settings[textwrap_arg]

        width = kwargs.get('width', None)
        # TODO: How best to use the template here?
        inner = capitalize_func(super().format(tag, content, **settings))
        template = settings['template']
        return "{}{}{}".format(
            "\n"*settings['lines_above'],
            template.format(justify_func(inner, width, **justify_args)),
            "\n"*settings['lines_below']
        )


# TODO: Need to differentiate between code spans and code blocks, somehow!
# 1) This formatter could check if it has siblings by checking the parent's children
#    (can't just check the parent because block could be just a code inside a p)
# 2) The parser could keep an eye out for code blocks and update the assigned formatter
# 3) Could check the children - if any child data has a newline in it, then it's a block, innit?
# 4) Could have the paragraph formatter skip the wrapping, but not the before and after
#    padding if it has only a code child
class CodeFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            inline_template="{}",
            block_template="{}"
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)

        parent = kwargs.get('parent', None)
        if parent and parent.tag == 'pre':
            # The pre will handle the formatting
            return content
        if '\n' in content:
            return settings['block_template'].format(content)
        return settings['inline_template'].format(content)


class PreFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            line_template="{}",
            indent=0,
            before="",
            after="",
            lines_above=1,
            lines_below=1,
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)

        lines = content.split('\n')
        formatted = []
        for line in lines:
            formatted.append(
                "{}{}".format(
                    " "*settings['indent'],
                    settings['line_template'].format(line)
                )
            )

        return "{}{}{}".format(
            "\n"*settings['lines_above'],
            "\n".join(formatted),
            "\n"*settings['lines_below'],
        )


class LinkFormatter(Formatter):

    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            template="{content}[{link_number}]",
            capitalized=False,
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)
        capitalize_func = capitalize if settings['capitalized'] else _noop
        return settings['template'].format(
            content=capitalize_func(super().format(tag, content, **kwargs)),
            link_number=kwargs["link_number"]
        )


class ExtractedLinkFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            template="[{link_number}] {description}: {url}\n",
            gophermap_template="{type}[{link_number}] {description}\t{selector}\t{host}\t{port}\n",
            max_link_description=10,
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)

        href = kwargs['href']
        title = kwargs['title']

        max_link_description = settings['max_link_description']
        trimming = len(content) > max_link_description
        content = content.strip()[:max_link_description]
        if trimming:
            content = "{}...".format(content)

        description = title if title is not None else content

        output_format = kwargs['output_format']
        if output_format == 'gophermap':
            gopher_link = kwargs['gopher_link']
            return settings['gophermap_template'].format(
                description=super().format(tag, description, **kwargs),
                link_number=kwargs["link_number"],
                selector=gopher_link['selector'],
                type=gopher_link['type'],
                host=gopher_link['host'],
                port=gopher_link['port'],
            )
        else:
            return settings['template'].format(
                description=super().format(tag, description, **kwargs),
                link_number=kwargs["link_number"],
                url=href
            )


class SpanFormatter(Formatter):
    def __init__(self, *args, **kwargs):
        self.defaults = dict(
            template="{}",
            capitalized=False,
        )
        self.defaults.update(kwargs)

    def format(self, tag, content, **kwargs):
        settings = self._get_format(tag, **kwargs)
        capitalize_func = capitalize if settings['capitalized'] else _noop
        return settings['template'].format(
            capitalize_func(super().format(tag, content, **kwargs))
        )


null_formatter = Formatter()

default_h1_formatter = HeaderFormatter(
    centered=True,
    underlined=True,
    underline_full=True,
    margin_top=3,
)

default_h2_formatter = HeaderFormatter(
    centered=True,
    underlined=True,
    underline_full=False,
)

default_h3_formatter = HeaderFormatter(
    centered=True,
    underlined=True,
    underline_full=False,
    underline_char='-',
)

default_p_formatter = ParagraphFormatter()

default_code_formatter = CodeFormatter(inline_template="`{}`")

default_pre_formatter = PreFormatter(indent=4)

default_link_formatter = LinkFormatter()

default_extracted_link_formatter = ExtractedLinkFormatter()

default_em_formatter = SpanFormatter(template="/{}/")

default_strong_formatter = SpanFormatter(template="*{}*")
