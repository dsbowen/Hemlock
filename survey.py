from hemlock import Branch, Page, Label, Input, Slider, binary, route

# update selenium-tools

@route('/survey')
def start():
    return Branch(
        Page(
            Slider(min=0, max=100, reversed=True)
        ),
        Page(
            Label('hello, world'),
            terminal=True, back=True
        )
    )

def print_value(q):
    print(q.response, q.data)