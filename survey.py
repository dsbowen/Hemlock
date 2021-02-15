from hemlock import Branch, Page, Label, Input, route, settings

@route('/survey')
def start():
    return Branch(
        Page(
            Input(type='month', validate=check_datetime)
        ),
        Page(
            Label('hello, world'),
            terminal=True, back=True
        )
    )

def check_datetime(inpt):
    print(inpt.response)