"""# Input"""

from ..app import db, settings
from ..functions.debug import send_datetime, send_keys
from ..models import Debug, InputBase, Question
from .input_group import InputGroup

from selenium_tools import get_datetime
from sqlalchemy_mutable import HTMLAttrsType

html_datetime_types = (
    'date',
    'datetime-local',
    'month',
    'time',
    'week',
)

@Debug.register
def random_input(driver, question):
    """
    Default debug function for input questions. This function sends a random 
    string or number if the input takes text, or a random `datetime.datetime` 
    object if the input takes dates or times.

    Parameters
    ----------
    driver : selenium.webdriver.chrome.webdriver.WebDriver

    question : hemlock.Input
    """
    if question.type in html_datetime_types:
        send_datetime(driver, question)
    else:
        send_keys(driver, question)

settings['Input'] = {
    'class': ['form-control'], 'type': 'text', 'debug': random_input
}


class Input(Question):
    """
    Inputs take text input by default, or other types of html inputs.

    Inherits from [`hemlock.qpolymorphs.InputGroup`](input_group.md), 
    [`hemlock.models.InputBase`](bases.md) and 
    [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Input label.

    template : str, default='hemlock/input.html'
        Template for the input body.

    Attributes
    ----------
    
    Examples
    --------
    ```python
    from hemlock import Input, Page, push_app_context

    app = push_app_context()

    Page(Input('<p>Input text here.</p>')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'input'}

    input_attrs = db.Column(HTMLAttrsType)
    prepend = db.Column(db.Text)
    append = db.Column(db.Text)

    _input_attr_names = [
        'class',
        'type',
        'readonly',
        'disabled',
        'size',
        'maxlength',
        'max', 'min',
        'multiple',
        'pattern',
        'placeholder',
        'required',
        'step',
        'autofocus',
        'height', 'width',
        'list',
        'autocomplete',
    ]

    def __init__(self, label=None, template='hemlock/input.html', **kwargs):
        self.input_attrs = {}
        super().__init__(label=label, template=template, **kwargs)

    def _record_data(self):
        if self.type in html_datetime_types:
            self.data = get_datetime(self.type, self.response) or None
        elif self.type == 'number' and self.response: 
            self.data = float(self.response)
        else:
            super()._record_data()
        return self

    def __getattribute__(self, key):
        if key == '_input_attr_names' or key not in self._input_attr_names:
            return super().__getattribute__(key)
        return self.attrs.get(key)

    def __setattr__(self, key, val):
        if key in self._input_attr_names:
            self.input_attrs[key] = val
        else:
            super().__setattr__(key, val)