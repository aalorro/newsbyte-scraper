#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True
import re
import HTMLParser


def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def strip_code(text):
    return re.sub(r'\_|\(\w*.*\);\s*', '', text)


def strip_backslash(text):
    return re.sub(r'\\', '', text)


# strips the link with text included
def strip_links(text):
    return re.sub(r'<a\s.*?>.*?</a>', '', text, flags=re.M | re.I)


# strips the link with text not included
def strip_links2(text):
    return re.sub(r'<a.*?>|</a>', '', text, flags=re.M | re.I)


def strip_p(text):
    return re.sub(r'<p.*?>|</p>', '', text, flags=re.M | re.I)


def strip_div(text):
    return re.sub(r'<div.*?>|</div>', '', text, flags=re.M | re.I)


def strip_newline(text):
    return re.sub(r'\n', '', text, flags=re.M | re.I)


def strip_span(text):
    return re.sub(r'<span.*?>|</span>', '', text, flags=re.M | re.I)


def strip_img(text):
    return re.sub(r'<img.*?>|</img>', '', text, flags=re.M | re.I)


def strip_javascript(text):
    return re.sub(r'<script.*?>.*?</script>', '', text, flags=re.M | re.I)


def strip_iframe(text):
    return re.sub(r'<iframe.*?>|</iframe>', '', text, flags=re.M | re.I)


def strip_cdata(text):
    return re.sub(r'//<.*?\]\]>', '', text, flags=re.M | re.I)


def has_links(text):
    return bool(re.search(r'<a\s.*?>.*?</a>', text, re.M | re.I))


def convert_br(text, repl='\n'):
    return re.sub(r'<br\s*\\?\/?>', repl, text, flags=re.I)


def html_unescape(text):
    h = HTMLParser.HTMLParser()
    return h.unescape(text)


def gma_convert_br(text, repl='\n\n'):
    return re.sub(r'&nbsp;', repl, text, flags=re.I)


def strip_extra_newlines(text):
    return re.sub(r'\n\n\n\n', '', text, flags=re.I)


def strip_brackets(text):
    return re.sub(r'\[.+\]', '', text)


def convert_div(text):
    return re.sub(r'<div.*?>|</div>', '\n', text, flags=re.M | re.I)


def convert_p(text):
    return re.sub(r'<p.*?>|</p>', '\n', text, flags=re.M | re.I)

def get_src_attr(text):
    return re.sub(r'<img.*?src="|">|"/>|</img>', '', text)
