from hemlock import Branch, Page, Label, Input, Slider, likert, route, settings
from hemlock import Debug as D

@route('/survey')
def start():
    return Branch(
        Page(
            Slider(
                ticks=[0, 10],
                ticks_labels=['min', 'max'],
                formatter={0: 'Min', 5: 'Mid', 10: 'Max'},
                step=2,
                var='var',
                submit=print_value,
                # debug=D.click_slider_range(26)
            )
        ),
        Page(
            Label('hello, world'),
            terminal=True, back=True
        )
    )

def print_value(q):
    print(q.response, q.data)