"""# Questions

`hemlock.Question` and `hemlock.ChoiceQuestion` are 'question skeletons';
most useful when fleshed out. See section on question polymorphs.
"""

from ..app import db
from ..tools import key
from .bases import Data
from .private import CSSListType, JSListType

from flask import render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable import (
    HTMLAttrsType, MutableType, MutableJSONType, MutableListType, 
    MutableListJSONType
)

import html
import os
from copy import copy


class Question(Data):
    """
    Base object for questions. Questions are displayed on their page in index 
    order.

    It inherits from 
    [`hemlock.models.Data`](bases.md).

    Parameters
    ----------
    label : str or None, default=None
        Question label.

    template : str, default='form-group.html'
        File name of question template.

    extra_css : list, default=[]
        List of extra CSS elements to add to the default CSS.

    extra_js : list, default=[]
        List of extra javascript elements to add to the default 
        javascript.

    form_group_class : list, default=['card', 'form-group', 'question']
        List of form group classes.

    form_group_attrs : dict, default={}
        Dictionary of HTML attribues for the form group tag.

    error_attrs : dict, default={'class' ['alert', 'alert-danger']}
        Dictionary of HTML attributes for the error alert.

    Attributes
    ----------
    append : str or None, default=None
        Text (usually) appended to the input tag.

    css : list, default=[]
        List of CSS elements.

    default : misc
        Default question response.

    error : str or None, default=None
        Error message.

    error_attrs : dict
        Set from the `error_attrs` parameter.

    form_group_class : list
        Set from the `form_group_class` parameter.

    form_group_attrs : dict
        Set from the `form_group_attrs` parameter.

    has_responded : bool, default=False
        Indicates that the participant has responded to this question.

    input_attrs : dict
        Dictionary of HTML attributes for the input tag.

    label : str or None, default=None
        Question label.

    prepend : str or None, default=None
        Text (usually) prepended to the input tag.

    response : misc
        Participant's response.

    template : str
        Set from the `template` parameter.

    Relationships
    -------------
    part : hemlock.Participant or None
        The participant to which this question belongs. Derived from 
        `self.page`.

    branch : hemlock.Branch or None
        The branch to which this question belongs. Derived from `self.page`.

    page : hemlock.Page or None
        The page to which this question belongs.

    compile : list of hemlock.Compile, default=[]
        List of compile functions; run before the question is rendered.

    validate : list of hemlock.Validate, default=[]
        List of validate functions; run to validate the participant's response.

    submit : list of hemlock.Submit, default=[]
        List of submit functions; run after the participant's responses have been validated for all questions on a page.

    debug : list of hemlock.Debug, default=[]
        List of debug functions; run during debugging. The default debug function is unique to the question type.

    Notes
    -----
    A CSS element can be any of the following:

    1. Link tag (str) e.g., `'<link rel="stylesheet" href="https://my-css-url">'`
    2. Href (str) e.g., `"https://my-css-url"`
    3. Style dictionary (dict) e.g., `{'body': {'background': 'coral'}}`

    The style dictionary maps a css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.

    A Javascript element can be any of the following:

    1. Attributes dictionary (dict) e.g., `{'src': 'https://my-js-url'}`
    2. JS code (str)
    3. Tuple of (attributes dictionary, js code)
    """
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': question_type
    }

    # relationships
    @property
    def part(self):
        return None if self.page is None else self.page.part

    @property
    def branch(self):
        return None if self.page is None else self.page.branch

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    # HTML attributes
    key = db.Column(db.String(10))
    template = db.Column(db.String)
    css = db.Column(CSSListType, default=[])
    js = db.Column(JSListType, default=[])
    form_group_class = db.Column(MutableListJSONType, default=[])
    form_group_attrs = db.Column(HTMLAttrsType, default={})
    error = db.Column(db.Text)
    error_attrs = db.Column(HTMLAttrsType, default={})
    label = db.Column(db.Text)
    prepend = db.Column(db.String)
    append = db.Column(db.String)
    input_attrs = db.Column(HTMLAttrsType)

    # Function attributes
    compile = db.Column(MutableListType, default=[])
    debug = db.Column(MutableListType, default=[])
    validate = db.Column(MutableListType, default=[])
    submit = db.Column(MutableListType, default=[])

    # Additional attributes
    default = db.Column(MutableJSONType)
    response = db.Column(MutableJSONType)
    has_responded = db.Column(db.Boolean, default=False)

    def __init__(
            self, label=None, extra_css=[], extra_js=[], 
            form_group_class=['card', 'form-group', 'question'],
            form_group_attrs={}, 
            error_attrs={'class': ['alert', 'alert-danger']}, 
            **kwargs
        ):
        def add_extra(attr, extra):
            # add extra css or javascript
            if extra:
                assert isinstance(extra, (str, list))
                attr += [extra] if isinstance(extra, str) else extra

        self.key = key(10)
        self.compile, self.debug, self.validate, self.submit = [], [], [], []
        self.css, self.js = [], []
        super().__init__(
            label=label, 
            form_group_class=form_group_class,
            form_group_attrs=form_group_attrs,
            error_attrs=error_attrs, 
            **kwargs
        )
        add_extra(self.css, extra_css)
        add_extra(self.js, extra_js)

    # methods
    def clear_error(self):
        """
        Clear the error message.

        Returns
        -------
        self : hemlock.Question
        """
        self.error = None
        return self

    def clear_response(self):
        """
        Clear the response.

        Returns
        -------
        self : hemlock.Question
        """
        self.response = None
        self.has_responded = False
        return self

    # methods executed during study
    def _compile(self):
        [f(self) for f in self.compile]
        return self

    def _render(self, body=None):
        return render_template(self.template, q=self)

    def _render_js(self):
        return self.js.render()

    def _record_response(self):
        self.has_responded = True
        self.response = request.form.get(self.key)
        if isinstance(self.response, str):
            # convert to safe html
            self.response = html.escape(self.response)
        return self
        
    def _validate(self):
        """Validate Participant response
        
        Check validate functions one at a time. If any yields an error 
        message (i.e. error is not None), indicate the response was invalid 
        and return False. Otherwise, return True.
        """
        for f in self.validate:
            self.error = f(self)
            if self.error:
                return False
        self.error = None
        return True

    def _record_data(self):
        self.data = self.response
        return self
    
    def _submit(self):
        [f(self) for f in self.submit]
        return self

    def _debug(self, driver):
        [f(driver, self) for f in self.debug]
        return self


class ChoiceQuestion(Question):
    """
    A question which contains choices. Inherits from `hemlock.Question`.

    Parameters
    ----------
    label : str or None, default=None
        Question label.

    choices : list, default=[]
        Choices which belong to this question. List items are usually 
        `hemlock.Choice` or `hemlock.Option`.

    template : str or None, default=None
        Template for the question body.

    Attributes
    ----------
    choices : list, default=[]
        Set from `choices` parameter.

    choice_cls : class, default=hemlock.Choice
        Class of the choices in the `choices` list.

    multiple : bool, default=False
        Indicates that the participant can select multiple choices.

    Notes
    -----
    A choice can be any of the following:

    1. Choice objects (type will depend on the choice question).
    2. `str`, treated as the choice label.
    3. `(choice label, value)` tuple.
    4. `(choice label, value, name)` tuple.
    5. Dictionary with choice keyword arguments.
    """
    choices = None # must be implemented by choice question

    def __init__(self, label=None, choices=[], template=None, **kwargs):
        self.choices = choices
        super().__init__(label=label, template=template, **kwargs)

    def _render(self, body=None):
        """Add choice HTML to `body`"""
        return render_template(self.template, q=self)

    def _record_response(self):
        """Record response

        The response is a single choice or a list of choices (if multiple 
        choices are allowed).
        """
        self.has_responded = True
        idx = request.form.getlist(self.key)
        self.response = [self.choices[int(i)].value for i in idx]
        if not self.multiple:
            self.response = self.response[0] if self.response else None
        return self

    def _record_data(self):
        """Record data

        For single choice questions, the data is the selected choice's 
        `value`.

        For multiple choice questions, the data is a dictionary mapping 
        each choice's `value` to a binary indicator that it was selected.
        """
        if self.multiple:
            self.data = {
                choice.value: int(choice.value in self.response)
                for choice in self.choices
            }
        else:
            self.data = self.response
        return self
    
    def _pack_data(self):
        """Pack data for storage in the `DataStore`

        For multiple choice questions, the packed data dictionary is similar to the data, but with the question's variable prepended to the key.
        """
        var = self.var
        if not self.multiple or var is None:
            return super()._pack_data()
        if self.data is None:
            packed_data = {
                var+c.value: None 
                for c in self.choices if c.value is not None
            }
        elif isinstance(self.data, dict):
            packed_data = {var+key: val for key, val in self.data.items()}
        else:
            packed_data = self.data
        return super()._pack_data(packed_data)