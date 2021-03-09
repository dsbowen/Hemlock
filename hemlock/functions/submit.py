"""# Submit functions"""

from ..models import Submit
from .utils import (
    convert, correct_choices as correct_choices_, get_benchmark, 
    match as match_
)

@Submit.register
def correct_choices(question, *values):
    """
    Convert the question's data to a 0-1 indicator that the participant 
    selected the correct choice(s).

    Parameters
    ----------
    question : hemlock.ChoiceQuestion

    \*values :
        Values of the correct choices.

    Notes
    -----
    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices.

    Examples
    --------
    ```python
    from hemlock import Check, Submit as S, push_app_context

    app = push_app_context()

    check = Check(
    \    '<p>Select the correct choice.</p>',
    \    ['correct', 'incorrect', 'also incorrect'],
    \    submit=S.correct_choices('correct')
    )
    check.response = check.choices[0]
    check._submit().data
    ```

    Out:

    ```
    1
    ```
    """
    question.data = int(correct_choices_(question, *values))

@Submit.register
def data_type(question, new_type, *args, **kwargs):
    """
    Convert the quesiton's data to a new type. If the question's data cannot
    be converted, it is changed to `None`.
    
    Parameters
    ----------
    question : hemlock.Question

    new_type : class
    
    \*args, \*\*kwargs :
        Arguments and keyword arguments to pass to the `new_type` constructor.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data='1', submit=S.data_type(int))
    inpt._submit()
    inpt.data, isinstance(inpt.data, int)
    ```

    Out:

    ```
    (1, True)
    ```
    """
    question.data, success = convert(question.data, new_type, *args, **kwargs)
    if not success:
        question.data = None

@Submit.register
def match(question, pattern):
    """
    Convert the question's data to a 0-1 indicator that the data matches the
    pattern.

    Parameters
    ----------
    question : hemlock.Question

    pattern : str or hemlock.Question
        Regex pattern to match. If this is a `Question`, the pattern is the 
        question's `response`'.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data='hello world', submit=S.match('hello *'))
    inpt._submit().data
    ```

    Out:

    ```
    1
    ```
    """
    question.data = int(match_(question, pattern) is not None)

# Value comparisons

@Submit.register
def eq(question, value, data_type=None):
    """
    Convert the question's data to a 0-1 indicator that the question's data 
    equals the given value.

    Parameters
    ----------
    question : hemlock.Question

    value :
        Value that the data should equal. If a `Question`, then `value.data` 
        is used.

    data_type : class or None, default=None
        Expected type of data. If `None`, the type of `value` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data=50, submit=S.eq(50))
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    1
    ```
    """
    value, data_type = get_benchmark(value, data_type)
    question.data = int(data_type(question.data) == value)

@Submit.register
def neq(question, value, data_type=None):
    """
    Convert the question's data to a 0-1 indicator that the question's data 
    does not equal the given value.

    Parameters
    ----------
    question : hemlock.Question

    value :
        Value that the data should not equal. If a `Question`, then 
        `value.data` is used.

    data_type : class or None, default=None
        Expected type of data. If `None`, the type of `value` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data=50, submit=S.neq(50))
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    0
    ```
    """
    value, data_type = get_benchmark(value, data_type)
    question.data = int(data_type(question.data) != value)

@Submit.register
def max(question, max, data_type=None):
    """
    Convert the question's data to a 0-1 indicator that the question's data 
    is less than the maximum value.

    Parameters
    ----------
    question : hemlock.Question

    max :
        Maximum value. If a `Question`, then `max.data` is used.

    data_type : class or None, default=None
        Expected type of data. If `None`, the type of `max` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data=101, submit=S.max(100))
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    0
    ```
    """
    max, data_type = get_benchmark(max, data_type)
    question.data = int(data_type(question.data) <= max)

@Submit.register
def min(question, min, data_type=None):
    """
    Convert the question's data to a 0-1 indicator that the question's data 
    is greater than the minimum value.

    Parameters
    ----------
    question : hemlock.Question

    min :
        Minimum value. If a `Question`, then `min.data` is used.

    data_type : class or None, default=None
        Expected type of data. If `None`, the type of `min` will be used.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data=-1, submit=S.min(0))
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    0
    ```
    """
    min, data_type = get_benchmark(min, data_type)
    question.data = int(data_type(question.data) >= min)

@Submit.register
def range(question, min, max, data_type=None):
    """
    Convert the question's data to a 0-1 indicator that the question's data 
    is within the range of `[min, max]`.

    Parameters
    ----------
    question : hemlock.Question

    min :
        Minimum value. If a `Question`, then `min.data` is used.

    max :
        Maximum value. If a `Question`, then `max.data` is used.

    data_type : class or None, default=None
        Expected type of data. If `None`, the type of `min` and `max` will be 
        used.

    Examples
    --------
    ```python
    from hemlock import Input, Submit as S, push_app_context

    app = push_app_context()

    inpt = Input(data=50, submit=S.range(0, 100))
    inpt._submit()
    inpt.data
    ```

    Out:

    ```
    1
    ```
    """
    min, min_type = get_benchmark(min, data_type)
    max, max_type = get_benchmark(max, data_type)

    assert min_type == max_type, '`min` and `max` must be the same type'
    question.data = int(min <= min_type(question.data) <= max)