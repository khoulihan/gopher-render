import argparse
# TODO: Optional modules should be optional!
import markdown
from markdown.extensions import codehilite
import pygments
from . import GopherHTMLParser

def _parse_arguments():
    parser = argparse.ArgumentParser(description="Convert Markdown or HTML to plain text or gophermaps")
    parser.add_argument("source", type=str, action="store", help="source file")
    parser.add_argument("destination", type=str, action="store", help="destination file")
    args = parser.parse_args()
    return args

def main():
    args = _parse_arguments()
    source_text = None
    with open(args.source, 'r') as in_file:
        source_text = in_file.read()

    md = markdown.Markdown(extensions=['markdown.extensions.codehilite', 'markdown.extensions.extra', 'markdown.extensions.meta'], **{
        'extension_configs': {
            'markdown.extensions.codehilite': {'css_class': 'highlight'},
            'markdown.extensions.extra': {},
            'markdown.extensions.meta': {},
        },
        'output_format': 'html5',
    })
    #md = markdown.Markdown()
    md_parsed = md.convert(source_text)

    parser = GopherHTMLParser(
        output_format="gophermap",
        gopher_host="my.gopher.com"
    )
    parser.feed(md_parsed)
    parser.close()

    #with open(args.destination, 'w') as out_file:
    #    out_file.write(parser.parsed)

    print(parser.parsed)


if __name__ == "__main__":
    main()
