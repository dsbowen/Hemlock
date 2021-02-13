"""# Blank"""

from .bases import InputBase
from ..app import db, settings
from ..functions.debug import random_input
from ..models import Question
from ..tools import key

from flask import render_template

settings['Blank'] = {
    'class': ['form-control'], 
    'type': 'text', 
    'blank_empty': '', 
    'debug': random_input
}


class Blank(InputBase, Question):
    """
    Fill in the blank question.

    Parameters
    ----------
    label : tuple, list, or None, default=None
        If the label is a `tuple` or `list`, the participant's response will 
        fill in the blanks between items.

    template : str, default='hemlock/input.html'
        File name of the Jinja template.

    blank_empty : str, default=''
        String used to fill in the blank when the participant's response is 
        empty.

    Examples
    --------
    ```python
    from hemlock import Page, Blank

    Page(
    \    Blank(
    \        ('Hello, ', '!'),
    \        blank_empty='_____'
    \    )
    ).preview()
    ```

    Enter 'World' in the input and the label will change to 'Hello, World!'.
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'blank'}

    blank_id = db.String(8)
    blank_empty = db.String()

    def __init__(self, label=None, template='hemlock/input.html', **kwargs):
        self.blank_id = key(8)
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/blank.js', q=self))

    def __setattr__(self, key, val):
        if key == 'label' and isinstance(val, (tuple, list)):
            val = '<span name="{}"></span>'.format(self.blank_id).join(val)
        super().__setattr__(key, val)