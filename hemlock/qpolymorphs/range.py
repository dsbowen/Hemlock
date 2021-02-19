"""# Range slider"""

from ..app import db, settings
from ..functions.debug import click_slider_range, drag_range, send_keys
from ..models import Question
from .bases import InputBase

from flask import render_template

choices_5 = [
    'Strongly disagree',
    'Disagree',
    'Neutral',
    'Agree',
    'Strongly agree'
]

choices_7 = [
    'Strongly disagree',
    'Disagree',
    'Slightly disagree',
    'Neutral',
    'Slightly agree',
    'Agree',
    'Strongly agree'
]

choices_9 = [
    'Very strongly disagree',
    'Strongly disagree',
    'Disagree',
    'Slightly disagree',
    'Neutral',
    'Slightly agree',
    'Agree',
    'Strongly agree',
    'Very strongly agree'
]

def likert(label=None, choices=5, default=0, **kwargs):
    def get_choices(choices):
        assert isinstance(choices, list) or choices in (5, 7, 9)
        if choices == 5:
            return choices_5
        elif choices == 7:
            return choices_7
        elif choices == 9:
            return choices_9
        return choices

    choices = get_choices(choices)
    tick_labels = [choices[i] for i in (0, int((len(choices)-1)/2), -1)]
    tick_labels = [label.replace(' ', '<br/>') for label in tick_labels]
    max_ = int((len(choices)-1)/2)
    min_ = -max_
    return Slider(
        label,
        ticks=[min_, 0, max_],
        ticks_labels=tick_labels,
        ticks_positions=[0, 50, 100],
        formatter=choices,
        default=default,
        **kwargs
    )

settings['Range'] = {
    'debug': drag_range,
    'type': 'range', 
    'class': ['custom-range'], 
    'min': 0, 'max': 100, 'step': 1
}


class Range(InputBase, Question):
    """
    Range sliders can be dragged between minimum and maximum values in step 
    increments.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Range label.

    template : str, default='hemlock/range.html'
        Template for the range body.

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

    Examples
    --------
    ```python
    from hemlock import Range, Page, push_app_context

    app = push_app_context()

    Page(Range('<p>This is a range slider.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'range'}

    def __init__(self, label=None, template='hemlock/range.html', **kwargs):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/range.js', q=self))


settings['RangeInput'] = {
    'debug': send_keys,
    'width': '5em',
    'class': ['form-control'],
    'type': 'number', 'min': 0, 'max': 100, 'step': 1
}


class RangeInput(InputBase, Question):
    """
    Range slider with an input field.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Range label.

    template : str, default='hemlock/rangeinput.html'
        Template for the range body.

    width : str, default='5em'
        Width of the input field.

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

    Examples
    --------
    ```python
    from hemlock import RangeInput, Page, push_app_context

    app = push_app_context()

    Page(RangeInput('<p>This is a range slider.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'rangeinput'}

    width = db.Column(db.String)

    def __init__(
            self, label=None, template='hemlock/rangeinput.html', **kwargs
        ):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/rangeinput.js', q=self))


settings['Slider'] = {
    'min': 0, 'max': 10, 'step': 1, 'debug': click_slider_range
}

class Slider(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'slider'}

    formatter = db.Column(db.PickleType)

    _input_attr_names = [
        'min', 'max', 'step',
        'precision',
        'orientation',
        'range',
        'selection',
        'tooltip',
        'tooltip_split',
        'tooltip_position',
        'handle',
        'reversed',
        'rtl',
        'enabled',
        'natural_arrow_keys',
        'ticks',
        'ticks_positions',
        'ticks_labels',
        'ticks_snap_bounds',
        'ticks_tooltip',
        'scale',
        'focus',
        'labelledby',
        'rangeHighlights',
        'lock_to_tips'
    ]

    def __init__(self, label=None, template='hemlock/slider.html', **kwargs):
        self.input_attrs = {}
        super().__init__(label=label, template=template, **kwargs)

    def get_values(self):
        if self.ticks:
            return range(self.ticks[0], self.ticks[-1]+self.step, self.step)
        return range(self.min, self.max, self.step)

    def __getattribute__(self, key):
        if key == '_input_attr_names' or key not in self._input_attr_names:
            return super().__getattribute__(key)
        return self.input_attrs.get('data-slider-'+key.replace('_', '-'))

    def __setattr__(self, key, val):
        if key in self._input_attr_names:
            self.input_attrs['data-slider-'+key.replace('_', '-')] = val
        else:
            super().__setattr__(key, val)

    def _render_js(self):
        def gen_formatter():
            if isinstance(self.formatter, str):
                return self.formatter
            elif isinstance(self.formatter, dict):
                mapping = {
                    str(key): str(val) for key, val in self.formatter.items()
                }
                return '''
                    var mapping={};
                    if (mapping[value]){{
                        return mapping[value];
                    }}
                    return value;
                '''.format(mapping)
            elif isinstance(self.formatter, list):
                mapping = {
                    str(key): str(val) 
                    for key, val in zip(self.get_values(), self.formatter)
                }
                return 'return {}[value];'.format(mapping)

        js = super()._render_js()
        if self.formatter is not None:
            formatter = gen_formatter()
            js += render_template(
                'hemlock/slider.js', q=self, formatter=formatter
            )
        return js

    def _render_input_attrs(self):
        ticks_labels = self.input_attrs.pop('data-slider-ticks-labels', None)
        if ticks_labels is None:
            return self.input_attrs.to_html()
        labels = ['"{}"'.format(i) for i in ticks_labels]
        labels = '[{}]'.format(', '.join(labels))
        labels = " data-slider-ticks-labels='{}'".format(labels)
        attrs = self.input_attrs.to_html()
        return_val = attrs + ' ' + labels
        self.input_attrs['data-slider-ticks-labels'] = ticks_labels
        return return_val

    def _record_data(self):
        self.data = float(self.response)
        if self.reversed:
            values = list(self.get_values())
            min_, max_ = values[0], values[-1]
            self.data = (
                (max_-min_)*(1 - (self.data-min_) / (max_-min_)) + min_
            )
        return self