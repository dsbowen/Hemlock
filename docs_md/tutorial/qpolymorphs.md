# Question polymorphs

In the previous part of the tutorial, you learned how to initialize a hemlock application and run it locally.

By the end of this part of the tutorial, you'll be able to add a variety of question polymorphs to your survey pages.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.1/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.1/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "What are 'question polymorphs'?"
    Question polymorphs are basically different types of questions. They're called 'polymorphs' because they're polymorphic with the `Question` table in your database. There's no reason you should know this, other than to sound sophisticated at dinner parties. You'll be a hit. Trust me.

## Creating a demographics page

We'll use jupyter notebook as a blackboard to iterate on our demographics page design. After pushing the application context, we'll create a demographics page based on the World Values Survey:

```python
from hemlock import Check, Input, Page, Label, RangeInput, Select, binary

p = Page(
    Select(
        'What is your gender?',
        ['', 'Male', 'Female', 'Other']
    ),
    Input(
        'How old are you?',
        type='number', min=0,
    ),
    Check(
        '''
        Which race or ethnicity do you belong to?
        
        Check as many as apply.
        ''',
        [
            'White',
            'Black',
            ('South Asian (Indian, Pakistani, etc.)', 'South Asian'),
            ('East Asian (Chinese, Japanese, etc.)', 'East Asian'),
            'Arabic or Central Asian',
            'Other',
        ],
        multiple=True
    ),
    binary(
        'Are you the primary wage earner in your household?'
    ),
    RangeInput(
        '''
        On a scale from 0 (lowest) to 10 (highest), which income group does your household belong to?
        ''',
        min=0, max=10
    )
)
p.preview()
```

As usual, use `p.preview()` to preview the page.

## Code explanation

Here we add several 'question polymorphs' (i.e., types of questions) to our page.

The first question is a select, or dropdown, question. Again, the first argument is the question label. The second argument is a list of choices the participant can select.

The next question is an input. The first argument is the question label (`'How old are you?'`). We specify the type of input by passing `type='number'` to the `Input` constructor. Without the `type` argument, participants can enter any text they want into the input. You can check out other HTML input types <a href="https://www.w3schools.com/html/html_form_input_types.asp" target="_blank">here</a>. We also specify the minimum value participants can enter, `min=0`.

The third question is a check question. Like a select question, this allows participants to select from a list of choices. The first argument is the question label, and the second argument is a list of choices. Notice that some of the choices are strings (`'White'`, `'Black'`) while some are tuples (`('South Asian (Indian, Pakistani, etc.)', 'South Asian')`). Passing the choice as a tuple tells hemlock to 'recode' the value when you download the data. Participants taking the survey see 'South Asian (Indian, Pakistani, etc.)' as one of the choices, but when you download the data, the corresponding column is named `South Asian`.

Also notice that we pass `multiple=True` to the `Check` constructor. This allows participants to select multiple choices. By default, `multiple` is `False`, meaning participants can only select one choice. We can also pass `multiple=True` to `Select` questions to allow participants to select multiple choices from a dropdown menu.

We create the fourth question using the `binary` function. `binary` creates a check question with two choices. By default, the choices are `'Yes'` and `'No'`, and their values are recoded as `1` and `0` when you download the data.

The last question is a `RangeInput`, which is what you get when a range slider and an input give each other a special hug. By default, range inputs go from 0 to 100, but we change it from 0 to 10 by specifying the `min` and `max` values.

??? tip "More question polymorphs"
    These are just some of the many question types hemlock offers. Check out the 'Question Polymorphs' header in the navigation bar for more.

## Adding the page to the survey

Once we're satisfied with the preview, we incorporate the page into our survey. Our `survey.py` file should be:

```python
from hemlock import Branch, Check, Input, Page, Label, Range, Select, route

@route('/survey')
def start():
    return Branch(
        Page(
            Select(
                'What is your gender?',
                ['', 'Male', 'Female', 'Other']
            ),
            # INSERT THE REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )
```

## Summary

In this part of the tutorial, you learned how to create a demographics questionnaire using several question polymorphs.

In the next part of the tutorial, you'll learn how to store and download survey data.