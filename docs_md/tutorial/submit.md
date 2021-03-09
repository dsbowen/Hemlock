# Submit

In the previous part of the tutorial, you learned how to validate participant responses.

By the end of this part of the tutorial, you'll be able to run functions to handle form submission.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "Why submit functions?"
    Submit functions run after a participant submits a page and their responses are validated. The most common use for submit functions is adding or transforming data based on a participant's responses. In our example, we're going to use a submit function to record a binary variable indicating whether the participant is female based on our gender question.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Input, Submit as S

inpt = Input(
    'Enter "hello world"', 
    submit=S.match('hello world')
)
inpt.submit
```

Out:

```
[<match('hello world')>]
```

You can add submit functions to a page or question by settings its `submit` attribute or passing a `submit` argument to its constructor. Submit functions run when a participant successfully submits a page.

The `match` submit function sets a question's data to 1 if the response matches a regex pattern, in this case `'hello world'`, and 0 if it does not.

Let's set the input question's response and watch our submit function work:

```python
inpt.response = 'hello world'
inpt._submit().data
```

Out:

```
1
```

Now let's set the question's response to something other than `'hello world'` and see what happens:

```python
inpt.response = 'something other than hello world'
inpt._submit().data
```

Out:

```
0
```

!!! tip
    You don't need to run `_submit` yourself in the survey. Hemlock takes care of this automatically for you.
    
!!! tip "More submit functions"
    `match` is just one of many [native hemlock submit functions](../functions/submit.md).

## Custom submission

We're going to use a custom submit function to record the female indicator. Let's do this in our notebook first.

```python
from hemlock import Embedded, Page, Select

def record_female(gender):
    gender.page.embedded = [
        Embedded('Female', gender.response=='Female', data_rows=-1)
    ]

page = Page(
    Select(
        'What is your gender?',
        ['', 'Male', 'Female', 'Other'],
        submit=record_female
    )
)
select = page.questions[0]
select.response = 'Female'
select._submit()
page.embedded[0].data
```

Out:

```
True
```

In:

```python
select.response = 'Male'
select._submit()
page.embedded[0].data
```

Out:

```
False
```

### Code explanation

We created a custom submit function to add an embedded data element to the demographics page. The submit function takes the gender select question as its argument. In general, submit functions take their parent as their first argument.

`gender.page` is the page to which the gender question belongs. `gender.page.embedded` is a list of embedded data elements belonging to that page. We set `embedded` to a list containing a single embedded data element. The embedded data element has a variable name `'Female'` and data which indicates whether the participant is female. As we did for the demographics questions, we pass `data_rows=-1`, meaning 'this value should appear on every row the participant contributes to the data frame'.

Finally, we add the submit function to the gender select question by passing `submit=record_female` to the question's constructor. This creates a 'sticky note' reminding the select question to run the submit function at the appropriate time.

## Function patterns

In the previous part of the tutorial, we created a custom validate function by registering a new validate function with `@V.register`. We then added it to a question by passing `validate=V.my_function(my_argument)` to the question's constructor. Here, we added a submit function without registering it, simply by passing `submit=my_function` to the question's constructor. Why are validate and submit functions treated differently?

The answer is that they aren't. You can add both validate and submit functions using one of two 'patterns'.

Simple pattern:

```python
def my_validate_function(question):
    # your amazing function here

def my_submit_function(question):
    # your amazing function here

Input(
    validate=my_validate_function,
    submit=my_submit_function
)
```

Decorator pattern:

```python
@V.register
def my_validate_function(question, my_argument):
    # your amazing function here

@S.register
def my_submit_function(question, my_argument):
    # your amazing function here

Input(
    validate=V.my_validate_function(my_validate_argument),
    submit=S.my_submit_function(my_submit_argument)
)
```

The main advantage of the simple pattern is, well, its simplicity. The main advantage of the decorator pattern is that it allows you to pass additional arguments to validate and submit functions.

To see the decorator pattern in action for submit functions, run the following in a jupyter notebook cell:

```python
@S.register
def my_function(parent, my_argument):
    print('My parent is', parent)
    print('My argument is', my_argument)
    
select = Select(
    submit=S.my_function('hello world')
)
select._submit()
```

Out:

```
My parent is <Select (transient 140423771774256)>
My argument is hello world
```

## Submission in our app

Now that we've seen how to add submit functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import (
    Branch, Check, Embedded, Input, Page, Label, RangeInput, Select, 
    Submit as S, Validate as V, binary, route
)

@route('/survey')
def start():
    return Branch(
        Page(
            Select(
                'What is your gender?',
                ['', 'Male', 'Female', 'Other'],
                var='Gender', data_rows=-1,
                validate=V.require(),
                submit=record_female
            ),
            # REST OF THE DEMOGRAPHICS PAGE
        ),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )

def record_female(gender):
    gender.page.embedded = [
        Embedded('Female', gender.response=='Female', data_rows=-1)
    ]
```

Run the app again, fill in the demographics page, and download the data. You'll now see a variable 'Female' in the data frame.

## Summary

In this part of the tutorial, you learned how create and run submit functions.

In the next part of the tutorial, you'll learn how to create an entire demographics page in one line of code using hemlock extensions.