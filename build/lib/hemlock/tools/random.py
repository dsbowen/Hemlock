"""# Randomization tools"""

from flask_login import current_user

import numpy as np

import random
import time
from itertools import combinations, cycle, permutations, product
from operator import itemgetter
from random import choice, shuffle
from string import ascii_letters, digits

def key(len_=90):
    """
    Parameters
    ----------
    len_ : int, default=90
        Length of the key to generate.

    Returns
    -------
    key : str
        Randomly generated key of ascii letters and digits of specificed 
        length.

    Notes
    -----
    The first character is a letter. This allows you to use `key` to generate
    strongly random id's for html elements. (Html element id's cannot start
    with a digit.)

    Examples
    --------
    ```python
    from hemlock import tools

    tools.key(10)
    ```

    Out:

    ```
    gpGmZuRfF7
    ```
    """
    chars = ascii_letters + digits
    first_char  = choice(ascii_letters)
    return first_char + ''.join(choice(chars) for _ in range(len_-1))

def reset_random_seed():
    seed = (1000 * int(time.time())) % 2**32
    random.seed(seed)
    np.random.seed(seed)

class Randomizer():
    """
    Evenly randomizes over a set of elements.

    Parameters
    ----------
    elements : iterable
        Set of elements over which to randomize.

    r : int, default=1
        Size of the subset of elements to select.

    combination : bool, default=True
        Indicates randomization over combinations of the elements, as opposed 
        to permutations.

    Attributes
    ----------
    elements : iterable
        Set from the `elements` parameter.

    Examples
    --------
    ```python
    from hemlock.tools import Randomizer

    elements = ('world','moon','star')
    randomizer = Randomizer(elements, r=2, combination=False)
    randomizer.next()
    ```

    Out:

    ```
    ('moon', 'world')
    ```
    """
    def __init__(self, elements, r=1, combination=True):
        self.elements = elements
        idx = list(range(len(elements)))
        iter_ = combinations(idx, r) if combination else permutations(idx, r)
        iter_ = list(iter_)
        shuffle(iter_)
        self._iter = cycle(iter_)
        
    def next(self):
        """
        Returns
        -------
        subset :
            Selected subset of elements.
        """
        return itemgetter(*next(self._iter))(self.elements)


class Assigner(Randomizer):
    """
    Evenly assigns participants to conditions. Inherits from 
    `hemlock.tools.Randomizer`.

    Parameters
    ----------
    conditions : dict
        Maps condition variable name to iterable of possible assignments.

    Attributes
    ----------
    keys : iterable
        Condition variable names.

    elements : iterable
        All possible combinations of condition values to which a participant may be assigned.

    Examples
    --------
    ```python
    from hemlock import Participant, push_app_context
    from hemlock.tools import Assigner

    push_app_context()

    part = Participant.gen_test_participant()
    conditions = {'Treatment': (0,1), 'Level': ('low','med','high')}
    assigner = Assigner(conditions)
    assigner.next()
    ```

    Out:

    ```
    {'Treatment': 1, 'Level': 'low'}
    ```

    In:

    ```python
    part.meta
    ```

    Out:

    ```
    [('Treatment', 0), ('Level', 'low')]
    ```
    """

    def __init__(self, conditions):
        self.keys = conditions.keys()
        super().__init__(tuple(product(*conditions.values())))
        
    def next(self, participant=None):
        """
        Assigns the participant to a condition. The condition assigment 
        updates the participant's metadata.

        Parameters
        ----------
        participant : hemlock.Participant or None, default=None
            This method records the assignment in this participant's `meta`
            dictionary. If `None`, the participant is the current user.

        Returns
        -------
        assignment : dict
            Maps condition variable names to assigned conditions.

        Notes
        -----
        By default, this method assigns the participant using flask-login's
        `current_user`. If you're assigning the participant in function 
        handled by Redis, this won't work. You'll need to manually pass in the
        participant.
        """        
        assignment = super().next()
        assignment = {key: val for key, val in zip(self.keys, assignment)}
        try:
            participant = participant or current_user
            participant.meta.update(assignment)
        except:
            print('Unable to update participant metadata.')
        return assignment