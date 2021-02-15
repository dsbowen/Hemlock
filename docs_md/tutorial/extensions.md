# Extensions

In the previous part of the tutorial, you learned how to add submit functions to pages and questions.

In this part of the tutorial, you'll learn how to install and use hemlock extensions and other python packages.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4.5/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4.5/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "What are extensions and why should I use them?"
    Building the demographics page took a while, didn't it? Now imagine making a new demographics page every time you make a survey for the rest of your life. Not fun.

    Instead, what if you could install a package to create a demographics page in one line of code? That's what hemlock extensions are for. Extensions package up commonly used questions, psychological scales, and other tools so you can download and use them simply and easily.

## Installation

Install the `hemlock-demographics` extension like so:

```bash
$ hlk install hemlock-demographics
```

In general, you'll install hemlock extensions and other python packages with:

```bash
$ hlk install <my-requested-package>
```

??? tip "Why use `hlk install` instead of `pip install`?"
    We've already installed python packages with `pip install`. Why use `hlk install` instead?

    1. It's good practice to use <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank">virtual environments</a> for all your coding projects. `hlk install` automatically installs your new package in the correct virtual environment for your hemlock project. 
    2. Deployment services like heroku (my recommended method) often need a `requirements.txt` file to know what packages to install to run your application. `hlk install` automatically updates your requirements files.

## A demographics page in one line of code

Restart your jupyter notebook. In general, you need to restart jupyter notebook after installing new packages for the notebook to recognize them.

Run the first cell to push the application context, then run:

```python
from hemlock_demographics import basic_demographics

basic_demographics(page=True).preview()
```

Voila! A demographics page in one import and one line of code.

The demographics package comes with several default groups of demographics questions. `basic_demographics` is one group. You can include the entire World Values Survey demographics questionnaire just as easily:

```python
from hemlock_demographics import comprehensive_demographics

comprehensive_demographics(page=True).preview()
```

You can also customize your demographics page:

```python
from hemlock_demographics import demographics

demographics(
    'gender', 'age', 'race', 'children', 'income_group', 
    page=True, require=True
).preview()
```

This time we also passed `require=True`, which requires participants to respond to every demographics question.

You can read more about the demographics extension <a href="https://dsbowen.github.io/hemlock-demographics/" target="_blank">here</a>.

## Demographics in our survey

Here's your entire survey file:

```python
from hemlock import Branch, Label, Page, route
from hemlock_demographics import basic_demographics

@route('/survey')
def start():
    return Branch(
        basic_demographics(page=True, require=True),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )
```

Run your app again to see what it looks like.

## Summary

In this part of the tutorial, you created a demographics page using a hemlock extension.

In the next part of the tutorial, you'll implement a confirmation page using compile functions.