#!/usr/bin/env python
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')
args = parser.parse_args()

fi = open(args.input, "r")
fo = open(args.output, "w")

text_input = fi.read()

# two newlines in latex signals a paragraph, if it occurs among text.
# I think the rest of whitespace is insignificant, unless:
# 1. TODO it occurs in a verbatim env,
# 2. there is a % comment that comments until the next newline

# TODO discriminate between paragraphs and e.g.
#
#\usepackage{a}
#
#\usepackage{b}
#

paragraph_split = re.split(r"\n{2,}", text_input)
paragraph_split = [p for p in paragraph_split if len(p) > 0]

def remove_noncomment_newlines(s, new_space=" "):
    newline_split = s.split("\n") # TODO work on other line ending
    o = ""
    for line in newline_split:
        # only add a space if it's needed
        maybe_space = (new_space if (len(o) > 0 and (not o[-1].isspace())) else "")

        # keep newline if this line has a comment
        maybe_newline = "\n" if "%" in line else ""

        o  = o + maybe_space + line + maybe_newline
    return o


def format_paragraph_chunk(s, new_space=" "):
    only_significant_newlinews = remove_noncomment_newlines(s)
    # TODO r"[\s-[\r\n]]", but python doesn't support character class subtraction
    ws_not_line_split = re.split(r"[ \t]", only_significant_newlinews)
    chunk = new_space.join([p for p in ws_not_line_split if len(p) > 0])
    return chunk.strip() # when putting the paragraphs back together, don't need any more newlines.


output = "\n\n".join(map(format_paragraph_chunk, paragraph_split))
fo.write(output)

fi.close()
fo.close()
