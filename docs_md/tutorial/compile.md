# Compile

In the previous part of the tutorial, you learned how to install and use extensions and third-party packages.

In this part of the tutorial, you'll implement a confirmation page using compile functions.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.5/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.5/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "Why compile functions?"
    Compile functions run just before a page's HTML is compiled. This allows us to make our survey responsive to participants. The most common use for compile functions is to 'pipe text' from a participant's previous responses onto a page.

    In our case, we're going to make a confirmation page for the participant's demographic information.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Check, Compile as C

check = Check(
    'Choose the correct answer',
    ['Correct', 'Incorrect', 'Also incorrect'],
    compile=C.shuffle()
)
check.compile
```

Out:

```
[<shuffle()>]
```

You can add compile functions to a page or question by setting its `compile` attribute or passing a `compile` argument to its constructor. Compile functions run just before a page's HTML is compiled.

The `shuffle` compile function shuffles a question's choices. (Or, if attached to a page, shuffles its page's questions).

Let's watch our compile function at work:

```
check._compile()
check.choices
```

Out:

```
[<Choice 'Also incorrect'>, <Choice 'Correct'>, <Choice 'Incorrect'>]
```

Run this a few times and notice how the order of the choices changes. This behavior is useful for comprehension checks, as we'll see later.

!!! tip
    You don't need to run `_compile` yourself in the survey. Hemlock takes care of this automatically for you.

!!! tip "More compile functions"
    `shuffle` is just one of many [native hemlock compile functions](../functions/compile.md).

## An aside on tools

To make our confirmation page, we're going to need two tools.

The first is `join`. This tool joins a list of items using a 'joiner' like 'and' or 'or'. We'll use this display the participant's race.

```python
from hemlock.tools import join

print(join('and', 'White'))
print(join('and', 'White', 'Black'))
print(join('and', 'White', 'Black', 'South Asian'))
```

Out:

```
White
White and Black
White, Black, and South Asian
```

The second tool is `html_list`. This tool joins a list of items in a bullet point (unordered) or enumerated (ordered) list.

```python
from hemlock import Page, Label
from hemlock.tools import html_list

Page(
    Label(
        html_list(
            'Item 1',
            'Item 2',
            'Item 3',
            ordered=False
        )
    )
).preview()
```

!!! tip "More tools"
    `join` and `html_list` are just two of many native hemlock tools. Check out the 'Tools' heading in the navigation bar for more.

## Custom compilation

We're going to take the participant's responses to the demographics page and display them on a new page. We'll ask the participant to correct any errors by going back to the demographics page.

### The demographics page: a recap

First, let's remind ourselves what's in the basic demographics page:

```python
from hemlock_demographics import basic_demographics

demographics_page = basic_demographics(page=True)
[print(q.label) for q in demographics_page.questions]
```

Out:

```
<p>What is your gender?</p>
<p>Please specify your gender.</p>
<p>How old are you?</p>

        <p>Which race or ethnicity do you belong to?</p>
        <p>Check as many as apply.</p>
        
<p>Please specify your race or ethnicity.</p>
```

The 0th question asks for gender, the 2nd for age, and the 3rd for race. (The 1st and 4th questions ask participants to specify gender and race if they choose 'Other').

Let's enter hypothetical responses for these questions.

```python
gender = demographics_page.questions[0]
gender.response = 'Male'
age = demographics_page.questions[2]
age.response = '28'
race = demographics_page.questions[3]
race.response = ['White']
```

### The compile function

It's time to write our custom compile function.

```python
from hemlock import Compile as C

@C.register
def confirm_demographics(confirm_label, demographics_page):
    gender = demographics_page.questions[0].response
    age = demographics_page.questions[2].response
    race = join('and', *demographics_page.questions[3].response)
    demographics_list = html_list(
        'Gender: {}'.format(gender),
        'Age: {}'.format(age),
        'Race: {}'.format(race),
        ordered=False
    )
    confirm_label.label = '''
        <p>Confirm the following information:</p>
        {}
        To correct this information, click '&lt;&lt;'.
    '''.format(demographics_list)
```

First, we register a new compile function with the `@C.register` decorator. The compile function takes the confirmation label as its first argument. In general, compile functions take their parent as their first argument. We also pass in the demographics page as the compile function's second argument.

`confirm_demographics` begins by gathering the demographics data (gender, date of birth, and race) from the demographics page. We use the `join` tool to join the participant's races.

Finally, we create a list of the participant's demographic information using `html_list`, and add this to the confirmation label.

??? note "What's `'&lt;'`?"
    The `label` attribute contains an HTML string. In HTML, `'<'` has a specific meaning, so we can't say `'click <<'`. The HTML encoding of `'<'` is `'&lt;'`, so we use that instead.

    Tl;dr Use a Word to HTML converter.

??? warning "`Label` object vs. `label` attribute"
    Note that we set the confirmation label with `confirm_label.label='my awesome label'`. `confirm_label` is a `Label` object. `confirm_label.label` is the attribute which contains the HTML. Don't confuse the `Label` object with the `label` attribute!

### Our compile function at work

Finally, let's see our compile function at work.

```python
confirm_page = Page(
    Label(
        compile=C.confirm_demographics(demographics_page)
    ),
    back=True
)
confirm_page._compile()
confirm_page.preview()
```

Note that we add a back button by passing `back=True` to the label's constructor.

## Compilation in our app

Now that we've seen how to add compile functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Compile as C, Label, Page, route
from hemlock.tools import join, html_list
from hemlock_demographics import basic_demographics

@route('/survey')
def start():
    demographics_page = basic_demographics(page=True, require=True)
    return Branch(
        demographics_page,
        Page(
            Label(
                compile=C.confirm_demographics(demographics_page)
            ),
            back=True
        ),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )

@C.register
def confirm_demographics(confirm_label, demographics_page):
    # COPY AND PASTE YOUR CONFIRM DEMOGRAPHICS FUNCTION HERE
```

Run the app again to see your confirmation page.

## Summary

In this part of the tutorial, you implemented a confirmation page using compile functions.

In the next part of the tutorial, you'll learn how to set up navigation between branches.