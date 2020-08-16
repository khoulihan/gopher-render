import argparse
from pathlib import Path
# TODO: Optional modules should be optional!
import markdown
from markdown.extensions import codehilite
import pygments
from . import GopherHTMLParser
from .rendering import Box
from .code_themes.monokai import renderers as monokai
from .code_themes.iced_gopher import renderers as ansi
from .code_themes.autumn import renderers as autumn

def _parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Markdown or HTML to plain text or gophermaps")
    parser.add_argument("source", type=str, action="store", help="source file")
    parser.add_argument("destination", type=str, action="store", help="destination file")
    parser.add_argument("-d", "--dump", action="store_true", dest="dump", help="Dump the html to the console before parsing it")
    args = parser.parse_args()
    return args

def main():
    args = _parse_arguments()
    source_text = None
    source_path = Path(args.source)
    with open(source_path, 'r') as in_file:
        source_text = in_file.read()

    if source_path.suffix == '.md':
        md = markdown.Markdown(extensions=['markdown.extensions.codehilite', 'markdown.extensions.extra', 'markdown.extensions.meta'], **{
            'extension_configs': {
                'markdown.extensions.codehilite': {'css_class': 'highlight'},
                'markdown.extensions.extra': {},
                'markdown.extensions.meta': {},
            },
            'output_format': 'html5',
        })

        # This version is for checking that default code blocks work ok
        # md = markdown.Markdown(extensions=['markdown.extensions.meta'], **{
        #     'extension_configs': {
        #         'markdown.extensions.meta': {},
        #     },
        #     'output_format': 'html5',
        # })

        #md = markdown.Markdown()
        source_text = md.convert(source_text)

    if args.dump:
        print(source_text)

    parser = GopherHTMLParser(
        output_format="text",
        gopher_host="my.gopher.com",
        box=Box(
            width=67,
            margin=[1,0,1,0]
        ),
        link_placement='footer',
        image_placement='inline',
        renderers=ansi
    )
    parser.feed(source_text)
    parser.close()

    #with open(args.destination, 'w') as out_file:
    #    out_file.write(parser.parsed)

    print(parser.parsed)


if __name__ == "__main__":
    main()
