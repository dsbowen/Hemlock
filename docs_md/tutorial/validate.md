# Validation

In the previous part of the tutorial, you learned how to store and download data.

By the end of this part of the tutorial, you'll be able to validate participant responses.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.3/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.3/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "Why validation?"
    I often run studies where I elicit numerical estimates. Early on, I noticed that a small but annoying faction of participants, rather than entering actual numbers (e.g., 50), answered the question in full sentences:

    > I believe the answer is fifty.

    We often need to make sure participants are entering the right kind of answer, whether it's typing the same password twice, answering a comprehension check by clicking on the correct choice, or entering a number instead of a word.

## Native HTML validation

You've already seen native HTML validation when you specified the type of input participants could enter (e.g., `type='number'`) or restricted the numerical range of their responses (e.g., `min=0`, `max=10`).

You'll often want to require participants to respond to certain questions. For `Input` questions, you can do this using native HTML validation. Open jupyter notebook and run the following:

```python
from hemlock import Page, Input

Page(
    Input(required=True)
).preview()
```

This opens a page with a blank input. Click '>>' without filling it in. Notice that you get an error message. Fill in the input, click '>>' again, and notice that you don't get the error message this time.

??? note "Learn more about native HTML attributes"
    You can set the HTML attributes of most question polymorphs by passing arguments to the constructor or by setting their attributes. Enter the following in a cell and run it.

    ```python
    Input(required=True).input_attrs
    ```

    Out:

    ```
    {'class': ['form-control'], 'type': 'text', 'required': True}
    ```

    This is a dictionary of attributes for the HTML input tag. Check out <a href="https://www.w3schools.com/html/html_form_attributes.asp" target="_blank">this resourse</a> for a full list of input tag attributes.

## Native hemlock validation

Hemlock provides an extensive library of validation functions beyond those of standard HTML.

To see the limitations of native HTML validation, preview this page:

```python
from hemlock import Check

Page(
    Check(
        'Pick one',
        ['World', 'Moon', 'Sun'],
        required=True
    )
).preview()
```

Click '>>' without checking any of the choices. Notice that there's no error message. Native HTML would have let you continue the survey without responding.

Hemlock's validation functions overcome problems like this. You can add validation functions to a page or question by passing a `validate` argument to its constructor or by setting its `validate` attribute. Validate functions run when a participant attempts to submit a page. If the participant's response is valid, the function returns `None`, allowing the participant to continue the survey. If the participant's response is invalid, the function returns an error message.

Let's use hemlock's validation to require a response to the check question from above:

```python
from hemlock import Validate as V

check = Check(
    'Pick one!',
    ['World', 'Moon', 'Star'],
    validate=V.require()
)
check.validate
```

Out:

```
[<require()>]
```

We can verify that the check question doesn't have a response or an error message yet.

```python
check.response, check.error
```

Out:

```
(None, None)
```

Let's run the validate function. Because the check has no response, the validate function will return an error message. The check stores the error message in its `error` attribute.

```python
check._validate()
check.error
```

Out:

```
'Please respond to this question.'
```

Now suppose the participant's response was `'World'` (i.e., the participant clicked 'World'), and re-run the validate function.

```python
check.response = 'World'
check._validate()
check.error
```

No error message this time!

!!! tip
    You don't need to run `_validate` yourself in the survey. Hemlock takes care of this automatically for you.

!!! tip "More validate functions"
    `require` is just one of many [native hemlock validate functions](../functions/validate.md).

## Custom validation

Hemlock also allows you to easily write custom validation functions.

For example, some of my early research involved asking participants to make two different estimates of the same quantity (don't ask, long story). I needed to validate that their second estimate was different from their first. Here's how I did it:

```python
@V.register
def different_second_estimate(second_estimate, first_estimate):
    if second_estimate.response == first_estimate.response:
        return 'Make sure your second estimate is different from your first'

first_estimate = Input(
    'Enter your first esimate',
    type='number'
)
second_estimate = Input(
    'Enter a second estimate which is different from your first',
    type='number',
    validate=V.different_second_estimate(first_estimate)
)
```

If the responses to the first and second estimate inputs are the same, the validate function returns an error message:

```python
first_estimate.response = 0
second_estimate.response = 0
second_estimate._validate()
second_estimate.error
```

Out:

```
'Make sure your second estimate is different from your first'
```

Let's see what happens when the participant's responses to the first and second estimate question are different:

```python
first_estimate.response = 0
second_estimate.response = 1
second_estimate._validate()
second_estimate.error
```

No error message this time!

### Code explanation

First, we register a new validate function with the `@V.register` decorator. The validate function takes two arguments: the second and first estimate `Input` objects. The function checks if the responses to these inputs are the same and, if they are, returns an error message.

Next, we create two inputs for the first and second estimate. We attach the validate function to the second estimate by passing `validate=V.different_second_estimate(first_estimate)` to its constructor.

Importantly, `V.my_function` does *not* return the result of `my_function`. `V.my_function` returns an object which evaluates `my_function` when a participant submits a page. `V.my_function` basically returns a sticky note reminding the survey to run `my_function` at the appropriate time. Pages and questions store these sticky notes in their `validate` attribute.

Note that `different_second_estimate` takes two arguments (the second and first estimate) but `V.different_second_estimate` only takes one (the first estimate). What's going on? In general, validate functions take their 'parent' (the page or question to which they belong) as their first argument. The arguments passed to `V.my_function` will be passed to `my_function` *after* the parent. For example:

```python
@V.register
def my_function(parent, my_argument):
    print('My parent is', parent)
    print('My argument is', my_argument)
    
inpt = Input(validate=V.my_function('hello world'))
inpt
```

Out:

```
<Input (transient 139890227379456)>
```

In:

```python
inpt._validate()
```

Out:

```
My parent is <Input (transient 139890227379456)>
My argument is hello world
```

Notice that the 'parent' is the input associated with the validation function (look at the digits after 'transient').

The same pattern holds for the other function models (submit, compile, and navigate functions) we will see in the coming sections.

## Validation in our app

Now that we've seen how to add validation in our notebook, let's add it to our app. Your goal is to require responses to each of the demographics questions.

In `survey.py`:

```python
from hemlock import (
    Binary, Branch, Check, Input, Page, Label, RangeInput, Select, 
    Validate as V, route
)

@route('/survey')
def start():
    return Branch(
        Page(
            Select(
                '<p>What is your gender?</p>',
                ['', 'Male', 'Female', 'Other'],
                var='Gender', data_rows=-1,
                validate=V.require()
            ),
            Input(
                '<p>How old are you?</p>',
                type='number', min=0, var='Age', data_rows=-1,
                required=True
            ),
            # REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('<p>Thank you for completing the survey!</p>'), 
            terminal=True
        )
    )
```

!!! tip "Tips for adding validation to your survey"
    1. For the input questions (age, income level), use native HTML validation, `required=True`.
    2. For questions that ask you to select one choice (gender, primary wage earner), use `validate=V.require()`.
    3. For questions that ask you to select at least one choice (race), use `validate=V.min_len(1)`. This means, 'select a minimum of 1 choice'.

Run the app again. Try to continue past the demographics page without filling in some of the questions, and see your validation at work!

!!! tip "Multiple validate functions"
    You can attach multiple validation functions to a page or question by setting `validate` to a list of functions. Validate functions run in the order in which you add them, stopping with the first validate function that returns an error.

## Summary

In this part of the tutorial, you learned how to validate participant responses.

In the next part of the tutorial, you'll learn how to run submit functions to modify participant data after they submit a page.