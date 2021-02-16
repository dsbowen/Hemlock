# Debugging

In the previous part of the tutorial, you implemented the responder branch.

By the end of this part of the tutorial, you'll be able to use hemlock's debugging tool to make sure your app is running smoothly.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.11/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.11/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "Why a custom debugging tool?"
    In the early days of hemlock, I coded a study in which I asked participants to estimate the ages of people in photographs. I used a submit function to change their data from strings to integers. Everything was running smoothly until one mischievous participant entered 'twenty-seven', breaking my survey and sending me home in a fit of rage.

    Since then, I took two steps to maintain equipoise when I launch my studies. First, I began daily mindfulness practice. Second, I wrote a custom debugger for hemlock.
    
    We often underestimate just how strangely participants will respond to our studies in ways that we can't foresee. Hemlock's debugger sends an *AI participant* through your survey to check things out. 'AI participant' is a bit of a misnomer. If anything, it's an artificially stupid participant. It clicks random buttons, enters random things into inputs and text boxes, drags range sliders to random values; basically stress testing your code.

## Setup

To run hemlock's custom debugging tool locally, you'll need [Google Chrome](https://www.google.com/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads). Check out the setup page for your OS for specific instructions:

- [Windows](../setup/win.md#chromedriver)
- [Windows Subsystem for Linux](../setup/wsl.md#chromedriver)
- [Mac](../setup/mac.md#chromedriver)
- [Linux](../setup/linux.md#chromedriver)

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Debug as D, Input

inpt = Input(
    debug=D.send_keys('Hello, World!')
)
inpt.debug
```

Out:

```
[<send_keys('Hello, World!')>]
```

You can add debug functions to a page or quesiton by settings its `debug` attribute or passing a `debug` argument to its constructor. Debug functions run when we run the debugger (in just a moment).

As its name suggests, the `send_keys` debug function tells the AI participant to send keys to the input.

Let's watch our debug function at work:

```python
from hemlock import Page
from hemlock.tools import chromedriver

driver = chromedriver()
page = Page(
    Input(
        debug=D.send_keys('Hello, World!')
    ),
    debug=D.debug_questions()
)
page.preview(driver)
page._debug(driver)
```

First, we use `chromedriver` to open Chromedriver with <a href="https://selenium-python.readthedocs.io/" target="_blank">selenium python</a>.

Next, we create a page with our input question. By default, a page has two debug functions. The first runs its questions' debug functions, and the second clicks the forward or back button. Here, we just want the page to run the question's debug function, so we pass `debug=D.debug_questions()` to the page's constructor.

Finally, we run the debug function. You'll notice it enters 'Hello, World!' in the input.

After you're done, close the driver:

```python
driver.close()
```

!!! tip
    You don't need to run `_debug` yourself in the survey. Hemlock takes care of this automatically for you.

!!! tip "More debug functions"
    `send_keys` is just one of many [native hemlock debug functions](../functions/debug.md).

## Default debug functions

We can attach debug functions to pages or questions. Most questions have a default debug function. For example, input questions have a default debug function which sends random ASCII characters to the input. Check out the default debug function at work:

```python
page = Page(
    Input(),
    debug=D.debug_questions()
)
page.preview(driver)
page._debug(driver)
```

## Custom debug functions

We won't need custom debug functions for our survey, but you may need them elsewhere. Creating custom debug function is similar to creating custom compile, validate, submit, and navigate functions, with one important difference. While the functions you've seen take their parent as their first argument, debug functions take a selenium webdriver as their first argument and their parent as their second argument:

Simple pattern:

```python
def my_debug_function(driver, parent):
    # your awesome debug function

Input(debug=my_debug_function)
```

Decorator pattern:

```python
@D.register
def my_debug_function(driver, parent, my_argument):
    # your awesome debug function

Input(
    debug=D.my_debug_function(my_argument)
)
```

Before writing custom debug functions, I recommend checking out the <a href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py" target="_blank">source code</a> for inspiration.

## Run the debugger

It's time to run hemlock's debugger through our app.

Open another terminal window. As always, change to your project directory:

```bash
$ cd
$ cd my-first-project
```

You should have three terminals open: one for jupyter, one for editing `survey.py` and running `hlk serve`, and now a third for running the debugger. In one of the terminal windows, run the hemlock app as usual (`hlk serve`). In the third terminal, run the debugger:

```bash
$ hlk debug
```

To run several AI participants through the survey, e.g. 3, use:

```bash
$ hlk debug -n 3
```

## Summary

In this part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In the next part of the tutorial, you'll learn how to deploy your application (i.e., put it on the web).

<!-- If you don't want to use hemlock-CLI, you can run the debugger with the python interpreter:

```bash
$ python3
>>> from hemlock.debug import AIParticipant, debug
>>> debug() # or debug(3) to run 3 AI participants
``` -->