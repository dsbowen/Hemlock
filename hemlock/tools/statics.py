"""Tool for generating statics"""

from hemlock.database.bases import HTMLBase

from bs4 import BeautifulSoup
from flask import render_template

from urllib.parse import parse_qs, urlparse, urlencode

__all__ = [
    'gen_external_css', 
    'gen_internal_css', 
    'gen_external_js',
    'Img',
    'Vid',
]

def gen_soup(template, selector=None, **attrs):
    soup = BeautifulSoup(template, 'html.parser')
    tag = soup.select_one(selector) if selector else list(soup.children)[0]
    [tag.__setitem__(key, val) for key, val in attrs.items()]
    return soup

def gen_external_css(**attrs):
    return gen_soup('<link rel="stylesheet" type="text/css"/>', **attrs)

def gen_internal_css(style):
    """Style maps css selectors to a dictionary of style attributes"""
    html = '<style></style>'
    soup = BeautifulSoup(html, 'html.parser')
    [
        soup.style.append(format_style(selector, attrs)) 
        for selector, attrs in style.items()
    ]
    return soup

def format_style(selector, attrs):
    attrs = ' '.join([attr+': '+val+';' for attr, val in attrs.items()])
    return selector+' {'+attrs+'}'

def gen_external_js(**attrs):
    return gen_soup('<script></script>', **attrs)


class Static(HTMLBase):
    def __init__(self, template, **kwargs):
        self.body = BeautifulSoup(render_template(template), 'html.parser')
        self.src_parms = {}
        [setattr(self, key, val) for key, val in kwargs.items()]

    def render(self, tag=None):
        if tag is not None:
            tag.attrs['src'] = tag['src']+'?'+urlencode(self.parms)
        return str(self.body)

    def _set_src(self, tag, url):
        self.parms = parse_qs(urlparse(url).query)
        tag['src'] = url.split('?')[0]


class Img(Static):
    def __init__(self, **kwargs):
        super().__init__('img.html', **kwargs)

    @property
    def figure(self):
        return self.body.select_one('figure')

    @property
    def img(self):
        return self.body.select_one('img')

    @property
    def src(self):
        return self.img.attrs.get('src')

    @src.setter
    def src(self, val):
        super()._set_src(self.img, val)

    @property
    def caption(self):
        return self.text('figcaption')

    @caption.setter
    def caption(self, val):
        self._set_element(val, 'figcaption')

    @property
    def alignment(self):
        for class_ in self.figure['class']:
            if class_ == 'text-left':
                return 'left'
            if class_ == 'text-center':
                return 'center'
            if class_ == 'text-right':
                return 'right'

    @alignment.setter
    def alignment(self, align):
        align_classes = ['text-'+i for i in ['left','center','right']]
        self.figure['class'] = [
            c for c in self.figure['class'] if c not in align_classes
        ]
        if align:
            align = 'text-' + align
            self.figure['class'].append(align)

    def render(self):
        return super().render(self.img)


YOUTUBE_ATTRS = {
    'frameborder': 0,
    'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
    'allowfullscreen': None
}


class Vid(Static):
    def __init__(self, **kwargs):
        super().__init__('vid.html', **kwargs)

    @property
    def iframe(self):
        return self.body.select_one('iframe')

    @property
    def src(self):
        return self.iframe.attrs.get('src')

    @src.setter
    def src(self, val):
        super()._set_src(self.iframe, val)

    def from_youtube(src):
        vid = Vid()
        parms = parse_qs(urlparse(src).query)
        id = parms.pop('v')[0] # video id
        vid.src = 'https://www.youtube.com/embed/' + id
        vid.iframe.attrs.update(YOUTUBE_ATTRS)
        vid.parms = parms
        return vid
        
    def render(self):
        return super().render(self.iframe)