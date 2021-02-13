# Proposer branch

In the previous part of the tutorial, you learned how to randomly assign participants to conditions.

In this part of the tutorial, you'll implement the proposer branch of the ultimatum game.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.9/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.9/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

!!! note
    This is the most difficult part of the tutorial. It uses advanced techniques that you'll rarely need.
    
    Don't sweat the details here. Try to get the gist of what's going on and feel free to 'cheat' by copying and pasting liberally.

    Brace yourself. Deep breath... jump in.

## Aside on fill-in-the-blank inputs

We're going to ask proposers to make their proposals by filling in a blank. Open your notebook and run this:

```python
from hemlock import Blank, Page

Page(
    Blank(
        ('Hello, ', '!'),
        blank_empty='_____'
    )
).preview()
```

Note that the blank's first argument isn't a string like we're used to seeing. Instead, it's a tuple. Whatever the participant enters in the input field gets inserted in between the tuple entries.

A key attribute of blanks is `blank_empty`. This is what fills in the blank when the participant's response is empty.

## The proposal input

First, we'll write a function to generate an input question where the proposer will input the proposed split. Enter the following in your jupyter notebook:

```python
N_ROUNDS = 5
POT = 20

def gen_proposal_input(round_):
    return Blank(
        ('''
        <p><b>Round {} of {}</b></p>

        <p>You have ${} to split between you and the responder. Fill in the 
        blank:</p>

        <p>I would like to offer the responder 
        <b>$'''.format(round_, N_ROUNDS, POT), '.00</b>.</p>'),
        prepend='$', append='.00', 
        var='Proposal', blank_empty='__', 
        type='number', min=0, max=POT, required=True
    )

Page(
    gen_proposal_input(round_=1)
).preview()
```

This function generates an fill-in-the-blank input which asks the proposer how much money they would like to offer to the responder. We record the data in a variable named `'Proposal'`.

## Finding a responder

We can use the <a href="https://docs.sqlalchemy.org/en/13/orm/query.html" target="_blank">SQLAlchemy Query API</a> to pair the proposer with a random responder this round. 

First, we create an input with variable name `'Response'` and data `5`:

```python
from hemlock import db

response = Blank(var='Response', data=5)
db.session.add(response)
db.session.flush([response])
response
```

Out:

```
<Blank 1>
```

Next, we get all `Blank` objects in the database with the variable name `'Response'` whose data is not `None`:

```python
responses = Blank.query.filter(
    Blank.var=='Response', Blank.data!=None
).all()
responses
```

Out:

```
[<Blank 1>]
```

Finally, we choose one of these inputs randomly and get its data:

```python
import random

random.choice(responses).data
```

Out:

```
5
```

## Displaying the proposer outcome

Now we want to display the outcome of the round to the proposer. This calls for a compile function:

```python
from hemlock import Compile as C, Embedded
from hemlock.tools import html_list

from random import randint

@C.register
def proposer_outcome(outcome_label, proposal_input):
    # get the proposal
    proposal = POT-proposal_input.data, proposal_input.data
    # get all responses
    responses = Blank.query.filter(
        Blank.var=='Response', Blank.data!=None
    ).all()
    if responses:
        # randomly choose a response
        response = random.choice(responses).data
    else:
        # no responses are available
        # e.g. if this is the first participant
        response = randint(0, POT)
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Response', response),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    proposal_list = html_list(
        'You: ${}'.format(proposal[0]),
        'Responder: ${}'.format(proposal[1]),
        ordered=False
    )
    outcome_label.label = '''
        <p>You proposed the following split:</p>

        {proposal_list}

        <p>The responder said they will accept any proposal which gives
        them at least ${response}.</p>
        
        <p><b>Your proposal was {accept_reject}, giving you a payoff of 
        ${payoff}.</b></p>
    '''.format(
        proposal_list=proposal_list, 
        response=response, 
        accept_reject='accepted' if accept else 'rejected', 
        payoff=payoff[0]
    )
```

Let's go through this step by step.

First, we get the proposal from the proposal input question. Remember that we converted the data for this input to an integer using a submit function. The data for this input is the amount of money the proposer offered to the responder, meaning that the proposed split is `(POT-proposal_input.data, proposal_input.data)`.

Second, we use the Query API to randomly select a response input question. We modify our above code to account for the fact that, if the first participant is a proposer, there won't be any responses to choose from. So, if our query can't find any response input questions, we return a random response.

Third, we compute the payoff and record the results of the round using embedded data.

Finally, we set the outcome label's `label` attribute to display the outcome of the round.

Let's see what the proposer outcome would have been if they had offered $10 to the responder:

```python
from hemlock import Label

page = Page(
    Label(
        compile=C.proposer_outcome(Blank(data=10))
    )
)
page._compile()
page.preview()
```

Notice that the outcome of the round is recorded in the proposer's outcome page's embedded data:

```python
[(e.var, e.data) for e in proposal_outcome_page.embedded]
```

Out:

```
[('Response', 5),
 ('Accept', 1),
 ('ProposerPayoff', 10),
 ('ResponderPayoff', 10)]
```

What would the proposer outcome have been if they had offered $4 to the responder?

```python
page = Page(
    Label(
        compile=C.proposer_outcome(Blank(data=4))
    )
)
page._compile()
page.preview()
```

In:

```python
[(e.var, e.data) for e in page.embedded]
```

Out:

```
[('Response', 5), 
 ('Accept', 0), 
 ('ProposerPayoff', 0), 
 ('ResponderPayoff', 0)]
```

## Adding the proposer branch to our survey

### Imports

We'll begin by updating our imports:

```python
from hemlock import (
    Blank, Branch, Compile as C, Embedded, Input, Label, Page, Validate as V, 
    Submit as S, route
)
from hemlock.tools import Assigner, comprehension_check, html_list, join
from hemlock_demographics import basic_demographics

import random
from random import randint

...
```

### Navigating to the proposer branch

Next we'll modify the ultimatum game branch to navigate to the proposer branch if the participant was assigned to be a proposer. In `survey.py`:

```python
...

def ultimatum_game(start_branch):
    proposer = assigner.next()['Proposer']
    return Branch(
        ...
        Page(
            Label(
                '''
                You are about to play an ultimatum game as a <b>{}</b>.
                '''.format('proposer' if proposer else 'responder')
            )
        ),
        navigate=proposer_branch
    )

...
```

### The proposer branch navigate function

Next we'll add our proposer navigate function to the bottom of `survey.py`:

```python
...

def proposer_branch(ug_branch):
    branch = Branch()
    for round_ in range(N_ROUNDS):
        proposal_input = gen_proposal_input(round_+1)
        branch.pages.append(
            Page(
                proposal_input
            )
        )
        branch.pages.append(
            Page(
                Label(
                    compile=C.proposer_outcome(proposal_input)
                )
            )
        )
    branch.pages.append(
        Page(
            Label('Thank you for completing the survey!'),
            terminal=True      
        )
    )
    return branch
```

This navigate function simply adds two pages to the proposer branch for each of `N_ROUNDS`. The first page asks the proposer to propose a split. The second page displays the outcome of the round.

### Generating the proposal input and outcome label

Finally, we'll add the `gen_proposal_input` and `proposer_outcome` functions we wrote in our notebook:

```python
...

def gen_proposal_input(round_):
    # AS IN THE NOTEBOOK

@C.register
def proposer_outcome(outcome_label, proposal_input):
    # AS IN THE NOTEBOOK
```

Run the app and see what the survey looks like in the proposer condition.

## Summary

In this part of the tutorial, you implemented the proposer branch. Give yourself a giant pat on the back. You're officially a hemlock expert. The rest will smooth sailing.

In the next part of the tutorial, you'll implement the responder branch.