# Navigate

In the previous part of the tutorial, you implemented a confirmation page using compile functions.

By the end of this part of the tutorial, you'll be able to set up navigation between branches.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.6/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.6/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

??? note "Why navigate functions?"
    Navigate functions move participants through different branches of the survey. For example, participants in the control group might follow one branch, while participants in the treatment group follow another.

    In our case, we'll use a navigate function to bring participants from the demographics branch of our survey to an 'utlimatum game' branch. In this branch, participants will play an ultimatum game with each other.

## Visualizing the 'branch stack'

We'll start by visualizing a participant's 'branch stack'. Open your jupter notebook and run the following:

```python
from hemlock import Branch, Page, Participant

def start():
    return Branch(
        Page(),
        Page(terminal=True)
    )

part = Participant.gen_test_participant(start)
part.view_nav()
```

Out:

```
 <Branch 1>
 <Page 1> C 
 <Page 2> T

 C = current page 
 T = terminal page
```

`part.view_nav()` prints the participant's branch stack. Right now there's only one branch in the stack (the one returned by `start`). The branch has two pages. The participant is currently on the first page. The terminal survey page is the next page, at the end of the branch.

## Basic syntax

You can add a navigation to a branch or page the same we we added validate, submit, and compile functions to pages and questions - by setting its `navigate` attribute or passing a `navigate` argument to its constructor.

```python
def start():
    return Branch(
        Page(),
        Page(),
        navigate=end
    )

def end(start_branch):
    return Branch(
        Page(terminal=True)
    )

part = Participant.gen_test_participant(start)
part.view_nav()
```

Out:

```
<Branch 2>
 <Page 3> C 
 <Page 4>
```

The navigate function `end` takes the start branch (the branch returned by `start`) as its first argument. In general, navigate functions take an 'origin' branch or page as their first argument. Navigate functions return a `Branch` object.

Let's make our test participant navigate forward and view the navigation again:

```python
part.forward().view_nav()
```

Out:

```
 <Branch 2>
 <Page 3> 
 <Page 4> C
```

And again:

```python
part.forward().view_nav()
```

Out:

```
 <Branch 2>
 <Page 3> 
 <Page 4> 
     <Branch (transient 139923798691696)>
     <Page (transient 139922995840960)> C T
```

What happened? Our participant reached the end of the start branch  and navigated to the end branch. It's currently on the first page of the end branch, which is the last (terminal) page of the survey.

!!! tip
    You don't need to run `forward` yourself in the survey. Hemlock takes care of this automatically for you.

??? tip "Decorator pattern"
    Like validate, submit, and compile functions, we can add navigate functions using the simple pattern or the decorator pattern. We can re-write the above navigate functions using the decorator pattern like this:

    ```python
    from hemlock import Navigate as N

    def start():
        return Branch(
            Page(),
            Page(),
            navigate=N.end()
        )

    @N.register
    def end(start_branch):
        return Branch(
            Page(terminal=True)
        )
    ```

## Branching off pages

Branching off of branches allows us to navigate to a new branch at the end of our current branch. But sometimes we'll want to navigate to a new branch from the middle of our current branch. To do this, we'll branch off of a page.

This time, instead of attaching the navigate function to the branch, we'll attach it to the first page of the branch:

```python
def start():
    return Branch(
        Page(
            navigate=middle
        ),
        Page(
            terminal=True
        )
    )

def middle(first_page):
    return Branch(
        Page()
    )

part = Participant.gen_test_participant(start)
```

As before, run `part.view_nav()` and `part.forward()` a few times. This is what you'll see:

```
 <Branch 5>
 <Page 8> C 
 <Page 9> T
```

```
 <Branch 5>
 <Page 8> 
     <Branch (transient 140643401377680)>
     <Page (transient 140643401377200)> C 
 <Page 9> T
```

```
 <Branch 5>
 <Page 8> 
     <Branch (transient 140643401377680)>
     <Page (transient 140643401377200)> 
 <Page 9> C T
```

What happened? We started on the first page of the start branch. Then, we branched off of the first page to the middle (the branch returned by `middle`). At the end of the middle branch, we picked up where we left off on the start branch.

## Navigating back

You'll often want to allow participants to navigate to a previous page. To do this, simply set a page's `back` attribute to `True`, or pass `back=True` to a page's constructor. 

You can also navigate backward in the notebook. Run this line a few times:

```python
part.back().view_nav()
```

Out:

```
 <Branch 5>
 <Page 8> 
     <Branch (transient 140643401377680)>
     <Page (transient 140643401377200)> C 
 <Page 9> T
```

```
 <Branch 5>
 <Page 8> C 
 <Page 9> T
```

## Navigation in our app

Now that we've seen how to add navigate functions in our notebook, let's add it to our app.

In `survey.py`:

```python
...

@route('/survey')
def start():
    demographics_page = basic_demographics(page=True, require=True)
    return Branch(
        ...
        navigate=ultimatum_game
    )

...

def ultimatum_game(start_branch):
    return Branch(
        Page(
            Label(
                'You are about to play an ultimatum game...'
            )
        ),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )
```

Run the app again and navigate past the demographics page. You'll find yourself on our new ultimatum game branch.

## Summary

In this part of the tutorial, you learned how to navigate between branches. 

In the next part of the tutorial, we'll tie together some of the things you've learned about page logic.