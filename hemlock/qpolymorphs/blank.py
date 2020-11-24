"""# Blank"""

from .bases import InputBase
from ..app import db, settings
from ..functions.debug import send_keys
from ..models import Question
from ..tools import key

from flask import render_template

settings['Blank'] = {
    'class': ['form-control'], 'type': 'text', 'blank_empty': '', 'debug': send_keys
}


class Blank(InputBase, Question):
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
            val = '<span name={}></span>'.format(self.blank_id).join(val)
        super().__setattr__(key, val)