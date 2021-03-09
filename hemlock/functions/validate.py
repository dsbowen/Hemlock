"""# Validation functions

These are built-in functions to validate a participant's response to a 
question. They return `None` if the response is valid, and an error message if 
the repsonse is invalid.
"""

from ..models import Validate
from ..tools.lang import join, plural
from .utils import (
    convert, correct_choices as correct_choices_, get_benchmark, 
    match as match_
)

import re
from operator import __ge__, __le__

# Require and type validation

RESP_TYPE_MSG = 'Please enter {}'

@Validate.register
def response_type(question, resp_type):
    """
    Validate that the response can be converted to a given type.
    
    Parameters
    ----------
    question : hemlock.Question

    resp_type : class
        The required type of response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.response_type(float))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number.
    ```
    """
    try:
        resp_type(question.response)
        return
    except:
        if resp_type == int:
            return RESP_TYPE_MSG.format('an integer')
        if resp_type == float:
            return RESP_TYPE_MSG.format('a number')
        return RESP_TYPE_MSG.format('the correct type of response')

REQUIRE_MSG = 'Please respond to this question'

@Validate.register
def require(question):
    """
    Require a response to this question.

    Parameters
    ----------
    question : hemlock.Question

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response=None, validate=V.require())
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please respond to this question.
    ```
    """
    return REQUIRE_MSG if question.response in (None, '') else None

# Set validation

IS_IN_MSG = 'Please enter {}'

@Validate.register
def is_in(question, valid_set, resp_type=None):
    """
    Validate that the question response is in a set of valid responses.

    Parameters
    ----------
    question : hemlock.Question
    
    valid_set : iterable
        Set of valid responses.

    resp_type : class or None, default=None
        Type of response expected; should match the type of elements in 
        `valid_set`.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='earth', validate=V.is_in(('wind', 'fire')))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter wind or fire.
    ```
    """
    resp, _ = convert(question.response, resp_type)
    if resp not in valid_set:
        return IS_IN_MSG.format(join('or', *valid_set))

NOT_IN_MSG = 'Please do not enter {}'

@Validate.register
def is_not_in(question, invalid_set, resp_type=None):
    """
    Validate that the question response is *not* in a set of invalid 
    responses.

    Parameters
    ----------
    question : hemlock.Question

    invalid_set : iterable
        Set of invalid responses.

    resp_type : class or None, default=None
        Type of response expected; should match the type of elements in
        `invalid_set`.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(
    \    response='earth', 
    \    validate=V.is_not_in(('earth', 'wind', 'fire'))
    )
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please do not enter earth, wind, or fire.
    ```
    """
    resp, _ = convert(question.response, resp_type)
    if resp in invalid_set:
        return NOT_IN_MSG.format(join('or', *invalid_set))

# Value validation

@Validate.register
def eq(question, value, resp_type=None):
    """
    Validate that the response equals the given value.

    Parameters
    ----------
    question : hemlock.Question

    value :
        Value that the response should equal. If a `Question`, then 
        `value.data` is used.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `value` will be 
        used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='51', validate=V.eq(50))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    'Please enter 50'
    ```
    """
    value, resp_type = get_benchmark(value, resp_type)
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if resp_type(question.response) != value:
        return 'Please enter {}'.format(value)

@Validate.register
def neq(question, value, resp_type=None):
    """
    Validate that the response does not equal the given value.

    Parameters
    ----------
    question : hemlock.Question

    value :
        Value that the response should not equal. If a `Question`, then 
        `value.data` is used.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `value` will be 
        used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='50', validate=V.neq(50))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    'Please do not enter 50'
    ```
    """
    value, resp_type = get_benchmark(value, resp_type)
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if resp_type(question.response) == value:
        return 'Please do not enter {}'.format(value)

@Validate.register
def max(question, max, resp_type=None):
    """
    Validate that the response does not exceed a maximum value.

    Parameters
    ----------
    question : hemlock.Question

    max : 
        Maximum value. If a `Question`, then `max.data` is the maximum value.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `max` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='101', validate=V.max(100))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response less than 100.
    ```
    """
    max, resp_type = get_benchmark(max, resp_type)
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if resp_type(question.response) > max:
        return 'Please enter a response less than {}'.format(max)

@Validate.register
def min(question, min, resp_type=None):
    """
    Validate that the response does not deceed a minumum value.

    Parameters
    ----------
    question : hemlock.Question

    min : 
        Minimum value. If a `Question`, then `min.data` is the minimum value.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the type of `min` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='-1', validate=V.min_val(0))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response greater than 0.
    ```
    """
    min, resp_type = get_benchmark(min, resp_type)
    type_error_msg = response_type(question, resp_type)
    if type_error_msg is not None:
        return type_error_msg
    if resp_type(question.response) < min:
        return 'Please enter a response greater than {}'.format(min)

@Validate.register
def range(question, min, max, resp_type=None):
    """
    Validate that the response is in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min : 
        Minimum value for the question response. If a `Question`, then 
        `min.data` is the minimum value.

    max :
        Maximum value for the question response. If a `Question`, then 
        `max.data` is the maximum value.

    resp_type : class or None, default=None
        Expected type of response. If `None`, the expected response type is 
        the type of `min` and `max`, which must be of the same type.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='101', validate=V.range(0, 100))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response between 0 and 100.
    ```
    """
    min, min_type = get_benchmark(min, resp_type)
    max, max_type = get_benchmark(max, resp_type)

    assert min_type == max_type, '`min` and `max` must be the same type'
    type_error_msg = response_type(question, min_type)
    if type_error_msg is not None:
        return type_error_msg
    if not (min <= min_type(question.response) <= max):
        return 'Please enter a response between {} and {}'.format(min, max)

# Length validation

EXACT_CHOICES_MSG = 'Please select exactly {0} {choice}'
EXACT_LEN_MSG = 'Please enter exactly {0} {character}'

@Validate.register
def exact_len(question, len_):
    """
    Validates the exact length of the repsonse. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    len_ : int
        Required length of the response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.exact_len(5))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter exactly 5 characters.
    ```
    """
    msg = require(question)
    if len_ and msg is not None:
        return msg
    if len(question.response) == len_:
        return
    if isinstance(question.response, list):
        return EXACT_CHOICES_MSG.format(len_, choice=plural(len_, 'choice'))
    return EXACT_LEN_MSG.format(len_, character=plural(len_, 'character'))

MAX_CHOICES_MSG = 'Please select at most {0} {choice}'
MAX_LEN_MSG = 'Please enter at most {0} {character}'

@Validate.register
def max_len(question, max_):
    """
    Validates the maximum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum length of the response.

    Notes
    -----
    A response of `None` is assumed to satisfy the max length validation. Use 
    `Validate.require` to require a response that is not `None`.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.max_len(5))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at most 5 characters.
    ```
    """
    if not question.response:
        return
    if len(question.response) <= max_:
        return
    if isinstance(question.response, list):
        return MAX_CHOICES_MSG.format(max_, choice=plural(max_, 'choice'))
    return MAX_LEN_MSG.format(max_, character=plural(max_, 'character'))

MIN_CHOICES_MSG = 'Please select at least {0} {choice}'
MIN_LEN_MSG = 'Please enter at least {0} {character}'

@Validate.register
def min_len(question, min_):
    """
    Valiadates the minimum length of the response. For a string response, this 
    is the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question
    
    min_ : int
        Minimum length of the response.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.min_len(15))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at least 15 characters.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    if min_ <= len(question.response):
        return
    if isinstance(question.response, list):
        return MIN_CHOICES_MSG.format(min_, choice=plural(min_, 'choice'))
    return MIN_LEN_MSG.format(min_, character=plural(min_, 'character'))

RANGE_CHOICES_MSG = 'Please select between {0} and {1} choices'
RANGE_LEN_MSG = 'Please enter between {0} and {1} characters'

@Validate.register
def range_len(question, min_, max_):
    """
    Validates the range of the response length. For a string response, this is 
    the length of the string. For a choices response, this is the number of 
    choices selected.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minimum response length.

    max_ : int
        Maximum response length.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.range_len(5, 10))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter 5 to 10 characters.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    if min_ <= len(question.response) <= max_:
        return
    if isinstance(question.response, list):
        return RANGE_CHOICES_MSG.format(min_, max_)
    return RANGE_LEN_MSG.format(min_, max_)

# Words validation

EXACT_WORDS_MSG = 'Please enter exactly {0} {word}'

@Validate.register
def exact_words(question, nwords):
    """
    Validate the exact number of words in the response.

    Parameters
    ----------
    question : hemlock.Question
    
    nwords : int
        Required number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.exact_words(1))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter exactly 1 word.
    ```
    """
    msg = require(question)
    if nwords and msg is not None:
        # a response of `None` can satisfy `exact_words` if `value==0`
        return msg
    assert isinstance(question.response, str)
    if _num_words(question.response) != nwords:
        return EXACT_WORDS_MSG.format(nwords, word=plural(nwords, 'word'))

MAX_WORDS_MSG = 'Please enter at most {0} {word}'

@Validate.register
def max_words(question, max_):
    """
    Validates the maximum number of words in the response.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.max_words(1))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at most 1 word.
    ```
    """
    if not question.response:
        return
    assert isinstance(question.response, str)
    if _num_words(question.response) > max_:
        return MAX_WORDS_MSG.format(max_, word=plural(max_,'word'))

MIN_WORDS_MSG = 'Please enter at least {0} {word}'

@Validate.register
def min_words(question, min_):
    """
    Validates the minimum number of words in the repsonse.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minimum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.min_words(3))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter at least 3 words.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg
    assert isinstance(question.response, str)
    if _num_words(question.response) < min_:
        return MIN_WORDS_MSG.format(min_, word=plural(min_,'word'))

RANGE_WORDS_MSG = 'Please enter between {0} and {1} words'

@Validate.register
def range_words(question, min_, max_):
    """
    Validates the number of words falls in a given range.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minumum number of words.

    max_ : int
        Maximum number of words.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.range_words(3, 5))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter between 3 and 5 words.
    ```
    """
    if min_ <= 0:
        return
    msg = require(question)
    if msg is not None:
        return msg 
    assert isinstance(question.response, str)
    if not (min_ <= _num_words(question.response) <= max_):
        return RANGE_WORDS_MSG.format(min_, max_)

def _num_words(string):
    """Count the number of words in the string"""
    return len(re.findall(r'\w+', string))

# Decimal validation

EXACT_DECIMALS = 'Please enter a number with exactly {0} {decimal}'

@Validate.register
def exact_decimals(question, ndec):
    """
    Validates the exact number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    ndec : int
        Required number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='1', validate=V.exact_decimals(2))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with exactly 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals != ndec:
        return EXACT_DECIMALS.format(ndec, decimal=plural(ndec, 'decimal'))

MAX_DECIMALS = 'Please enter a number with at most {0} {decimal}'

@Validate.register
def max_decimals(question, max_):
    """
    Validates the maximum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    max_ : int
        Maximum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='1.123', validate=V.max_decimals(2))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with at most 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals > max_:
        return MAX_DECIMALS.format(max_, decimal=plural(max_, 'decimal'))

MIN_DECIMALS = 'Please enter a number with at least {0} {decimal}'

@Validate.register
def min_decimals(question, min_):
    """
    Validates the minumum number of decimals.

    Parameters
    ----------
    question : hemlock.Question

    min_ : int
        Minumum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='1', validate=V.min_decimals(2))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with at least 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if decimals < min_:
        return MIN_DECIMALS.format(min_, decimal=plural(min_, 'decimal'))

RANGE_DECIMALS = 'Please enter a number with {0} to {1} decimals'

@Validate.register
def range_decimals(question, min_, max_):
    """
    Validates the number of decimals are in a given range.

    Parameters
    ----------
    question : hemlock.Question
    
    min_ : int
        Minimum number of decimals.

    max_ : int
        Maximum number of decimals.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='1.123', validate=V.range_decimals(0, 2))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a number with 0 to 2 decimals.
    ```
    """
    msg, decimals = _get_decimals(question)
    if msg:
        return msg
    if not (min_ <= decimals <= max_):
        return RANGE_DECIMALS.format(min_, max_)

def _get_decimals(question):
    """Return (error message, number of decimals) tuple

    This validation will fail if the response cannot be converted to `float`.
    """
    msg = response_type(question, float)
    if msg:
        return msg, None
    split = str(question.response).split('.')
    # number of decimals is 0 when no decimal point is specified.
    decimals = 0 if len(split) == 1 else len(split[-1])
    return None, decimals

# Regex validation

REGEX_MSG = 'Please enter a response with the correct pattern'

@Validate.register
def match(question, pattern):
    """
    Validate that the response matches the regex pattern.
    
    Parameters
    ----------
    question : hemlock.Question

    pattern : str or hemlock.Question
        Regex pattern to match. If this is a `Question`, the pattern is the 
        question's `response`'.

    Examples
    --------
    ```python
    from hemlock import Input, Validate as V, push_app_context

    app = push_app_context()

    inpt = Input(response='hello world', validate=V.match('goodbye *'))
    inpt._validate()
    inpt.error
    ```

    Out:

    ```
    Please enter a response with the correct pattern.
    ```
    """
    return REGEX_MSG if not match_(question, pattern) else None

# Choice validation

@Validate.register
def correct_choices(question, *values):
    """
    Validate that selected choice(s) is correct.
    
    Parameters
    ----------
    question : hemlock.Question

    \*values : 
        Values of the correct choices.

    Examples
    --------
    ```python
    from hemlock import Check, Validate as V, push_app_context

    app = push_app_context()

    check = Check(
    \    '<p>Select the correct choice.</p>',
    \    ['correct', 'incorrect', 'also incorrect'],
    \    validate=V.correct_choices('correct'),
    )
    check.response = check.choices[1]
    check._validate()
    check.error
    ```

    Out:

    ```
    Please select the correct choice.
    ```
    """
    if not correct_choices_(question, *values):
        if question.multiple:
            return '<p>Please select the correct choice(s).</p>'
        if len(values) == 1:
            return '<p>Please select the correct choice.</p>'
        return '<p>Please select one of the correct choices.</p>'