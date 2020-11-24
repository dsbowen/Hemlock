from hemlock import (
    Branch, Page, Embedded, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)
from hemlock.tools import consent_page

@route('/survey')
def start():
    return Branch(
        consent_page('consent', '<p>ID</p>'),
        Page(
            Label('page 1'),
            terminal=True
        )
    )