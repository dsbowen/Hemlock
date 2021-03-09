from hemlock import Branch, Page, Label, route, Input

@route('/survey')
def start():
    return Branch(
        Page(
            Input(prepend='**$**', append='**.00**'),
            terminal=True
        )
    )