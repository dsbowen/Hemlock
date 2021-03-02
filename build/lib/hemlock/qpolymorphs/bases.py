"""# Base for input questions"""

from ..app import db
from ..models import Question

from selenium_tools import get_datetime
from sqlalchemy_mutable import HTMLAttrsType

from datetime import datetime

HTML_DATETIME_TYPES = (
    'date',
    'datetime-local',
    'month',
    'time',
    'week',
)

HTML_DATETIME_FORMATS = {
    'date': 'yyyy-mm-dd',
    'datetime-local': 'yyyy-mm-ddThh:mm',
    'month': 'yyyy-mm',
    'week': 'yyyy-Www'
}


class InputBase():
    """
    This base class provides methods useful for debugging. Additionally, when 
    setting and getting attributes, it intercepts and automatically handles 
    input tag HTML attribues.
    """
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

    def __init__(self, *args, **kwargs):
        self.input_attrs = {}
        super().__init__(*args, **kwargs)

    def __getattribute__(self, key):
        if key == '_input_attr_names' or key not in self._input_attr_names:
            return super().__getattribute__(key)
        return self.input_attrs.get(key)

    def __setattr__(self, key, val):
        if key == 'type' and val in HTML_DATETIME_TYPES:
            # set the placeholder for HTML date and time input types
            # some browsers don't support these yet, so we need placeholders
            # to clarify for participants
            if not self.placeholder:
                self.placeholder = HTML_DATETIME_FORMATS[val]
        if key in self._input_attr_names:
            self.input_attrs[key] = val
        else:
            super().__setattr__(key, val)

    def input_from_driver(self, driver=None):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.Webdriver
            Driver which will be used to select the input. Does not need to be Chrome.

        Returns
        -------
        input : selenium.webdriver.remote.webelement.WebElement
            Web element of the `<input>` tag associated with this model.
        """
        return driver.find_element_by_css_selector('#'+self.key)

    def label_from_driver(self, driver):
        """
        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.Webdriver
            Driver which will be used to select the label. Does not need to be Chrome.

        Returns
        -------
        label : selenium.webdriver.remote.webelement.WebElement
            Web element of the label tag associated with this model.
        """
        selector = 'label[for={}]'.format(self.key)
        return driver.find_element_by_css_selector(selector)

    def _validate(self):
        if (
            hasattr(self, 'type')
            and self.type in HTML_DATETIME_TYPES and self.response
        ):
            # ensure response is in the proper datetime format
            # some browsers do not guarantee this natively
            try:
                get_datetime(self.type, self.response)
            except:
                self.error = 'Please format your response as {}'.format(
                    HTML_DATETIME_FORMATS[self.type]
                )
                return False
        return super()._validate()

    def _record_data(self):
        def get_data_type():
            if hasattr(self, 'min') and isinstance(self.min, float):
                return float
            if hasattr(self, 'max') and isinstance(self.max, float):
                return float
            if hasattr(self, 'step') and isinstance(self.step, float):
                return float
            return int

        if hasattr(self, 'type') and self.type in HTML_DATETIME_TYPES:
            # convert data to datetime type
            self.data = get_datetime(self.type, self.response) or None
        elif (
            hasattr(self, 'type') and self.type == 'number' 
            and self.response
        ):
            # convert data to int or float
            self.data = get_data_type()(float(self.response))
        else:
            super()._record_data()
        return self