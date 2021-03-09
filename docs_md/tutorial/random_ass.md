# Random assignment

In the previous part of the tutorial, you leanred how to add comprehension checks to your studies.

By the end of this part of the tutorial, you'll be able to randomly assign your participants to conditions, for example treatment and control.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.8/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.8/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Participant
from hemlock.tools import Assigner

assigner = Assigner({
    'Manipulation': ('happy', 'sad'),
    'Level': ('low', 'medium', 'high')
})
part = Participant.gen_test_participant()
assigner.next()
```

Out:

```
{'Manipulation': 'happy', 'Level': 'low'}
```

### Code explanation

FIrst, we created an `Assigner` instance. It randomly and evenly assigns participants to conditions, and easily handles factorial designs. 

The `Assigner`'s argument is a dictionary mapping treatment names to levels. In this example, we use a 2 (happy or sad manipulation) x 3 (low, medium, or high level) design.

We assign a participant to conditions using `assigner.next()`. This returns the treatment assignment and automatically records the assignment in the participant's `meta` attribute:

```python
part.meta
```

Out:

```
{'Manipulation': 'happy', 'Level': 'low'}
```

## Random assignment in our app

In `survey.py`:

```python
...
from hemlock.tools import Assigner, comprehension_check, join
...

N_ROUNDS = 5 # the number of rounds participants play
POT = 20 # the amount of money split

assigner = Assigner({'Proposer': (0, 1)})

...

def ultimatum_game(start_branch):
    ...
    
    proposer = assigner.next()['Proposer']
    return Branch(
        ...
        Page(
            Label('You passed the comprehension check!')
        ),
        Page(
            Label(
                '''
                You are about to play an ultimatum game as a **{}**.
                '''.format('proposer' if proposer else 'responder')
            )
        ),
        Page(
            Label('Thank you for completing this survey!'), 
            terminal=True
        )
    )

...
```

Run your app and pass the comprehenion check to see which condition you've been assigned to.

## Summary

In this part of the tutorial, you learned how to assign participants to conditions.

In the next part of the tutorial, you'll implement the proposer branch of the ultimatum game.