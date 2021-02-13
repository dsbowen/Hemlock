"""# Base for input questions"""

from ..app import db
from ..models import Question

from selenium_tools import get_datetime
from sqlalchemy_mutable import HTMLAttrsType


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

    def _record_data(self):
        html_datetime_types = (
            'date',
            'datetime-local',
            'month',
            'time',
            'week',
        )
        if self.type in html_datetime_types:
            self.data = get_datetime(self.type, self.response) or None
        elif self.type == 'number' and self.response:
            if (
                hasattr(self, 'step') 
                and (self.step is None or isinstance(self.step, int))
            ):
                type_ = int
            else:
                type_ = float
            self.data = type_(self.response)
        else:
            super()._record_data()
        return self