# Random assignment

In the previous part of the tutorial, you leanred how to add comprehension checks to your studies.

By the end of this part of the tutorial, you'll be able to randomly assign your participants to conditions.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Participant
from hemlock.tools import Assigner

part = Participant.gen_test_participant()
conditions = {'Treatment': (0,1), 'Level': ('low','med','high')}
assigner = Assigner(conditions)
assigner.next()
```

Out:

```
{'Treatment': 0, 'Level': 'low'}
```

The `Assigner` randomly and evenly assigns participants to conditions, and easily handles factorial designs. It automatically records the assignment in the participant's embedded data:

```python
[(e.var, e.data) for e in part.embedded]
```

Out:

```
[('Treatment', 0), ('Level', 'low')]
```

## Random assignment in our app

In `survey.py`:

```python
from hemlock import Branch, Check, Compile, Embedded, Input, Label, Navigate, Page, Range, Select, Submit, Validate, route
from hemlock.tools import Assigner, comprehension_check, join

from datetime import datetime
from random import randint

N_ROUNDS = 5
POT = 20

assigner = Assigner({'Proposer': (0,1)})

...

@Navigate.register
def ultimatum_game(start_branch):
    branch = comprehension_check(
        # COMPREHENSION CHECK HERE
    )
    proposer = assigner.next()['Proposer']
    branch.pages.append(Page(
        Label('''
            <p>You are about to play an ultimatum game as a <b>{}</b>.</p>
        '''.format('proposer' if proposer else 'responder')
        ), 
        terminal=True
    ))
    return branch
```

Run your app and pass the comprehenion check to see which condition you've been assigned to.

## Summary

In this part of the tutorial, you learned how to assign participants to conditions.

In the next part of the tutorial, you'll implement the proposer branch of the ultimatum game.