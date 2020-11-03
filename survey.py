from hemlock import (
    Branch, Page, Embedded, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)
from hemlock.tools import consent_page, completion_page

settings['collect_IP'] = False

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Hello World')
        ),
        Page(
            Label('Goodbye world')
        )
    )