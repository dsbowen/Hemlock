from sqlalchemy.types import JSON
from sqlalchemy_mutable import MutableList


class CSSListType(JSON):
    pass


class CSSList(MutableList):
    """
    Items in a `CSSList` must be one of the following:

    1. Link tag (str) e.g., `'<link rel="stylesheet" href="https://my-css-url">'`
    2. Href (str) e.g., `"https://my-css-url"`
    3. Style dictionary (dict) e.g., `{'body': {'background': 'coral'}}`

    The style dictionary maps a css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.
    """
    def render(self):
        def render_item(item):
            if isinstance(item, str):
                # interpret item as a link tag or href
                return (
                    item if item.startswith('<link')
                    else '<link rel="stylesheet" href="{}">'.format(item)
                )

            # interpret item as style dictionary
            def format_style(selector, attrs):
                attrs = ' '.join(
                    ['{}: {};'.format(*item) for item in attrs.items()]
                )
                return selector+' {'+attrs+'}'

            css = ' '.join(
                [format_style(key, val) for key, val in item.items()]
            )
            return '<style>{}</style>'.format(css)

        return '\n'.join([render_item(item) for item in self])


CSSList.associate_with(CSSListType)


class JSListType(JSON):
    pass


class JSList(MutableList):
    """
    Items in a `JSList` must be one of the following:

    1. Attributes dictionary (dict) e.g., `{'src': 'https://my-js-url'}`
    2. JS code (str)
    3. Tuple of (attributes dictionary, js code)
    """
    def render(self):
        from ...tools import format_attrs

        def render_item(item):
            assert isinstance(item, (tuple, dict, str))
            if isinstance(item, tuple):
                attrs, js = item
            elif isinstance(item, dict):
                attrs, js = item, ''
            elif isinstance(item, str):
                if item.startswith('<script'):
                    # item is already formatted
                    return item
                attrs, js = {}, item
            return '<script {}>{}</script>'.format(format_attrs(**attrs), js)

        return '\n'.join([render_item(item) for item in self])


JSList.associate_with(JSListType)