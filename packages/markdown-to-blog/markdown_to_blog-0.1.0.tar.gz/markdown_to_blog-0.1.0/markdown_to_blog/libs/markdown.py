import codecs

from markdown2 import Markdown
from .md_converter.base import MarkdownConverter

def convert_markdown(converter: MarkdownConverter, text: str):
    return converter.convert(text)


def convert(input_fn, output_fn, is_temp=False):
    with codecs.open(input_fn, "r", "utf_8") as fp:
        markdowner = Markdown(extras=["highlightjs-lang", "fenced-code-blocks"])
        html = markdowner.convert(fp.read())

        with codecs.open(output_fn, "w", "utf_8") as fwp:
            fwp.write(html)
