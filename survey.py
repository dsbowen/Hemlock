from hemlock import Branch, Page, Label, route, settings

@route('/survey')
def start():
    return Branch(
        Page(
            Label(
                'page 1'
            )
        ),
        Page(
            Label('hello, world'),
            terminal=True
        )
    )