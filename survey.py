from hemlock import (
    Branch, Page, Embedded, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)

@route('/survey')
def start():
    return Branch(
        Page(
            Label('page 0')
        ),
        Page(
            Label('page 1.5')
        ),
        Page(
            Label('page 1'),
            terminal=True
        )
    )