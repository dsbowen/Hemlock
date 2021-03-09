# Responder branch

In the previous part of the tutorial, you implemented the proposer branch.

In this part of the tutorial, you'll implement the responder branch.

The responder branch is similar to the proposer branch. For a great exercise, see if you can create it yourself without looking at my code.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.10/survey.py" target="_blank">`survey.py`</a> file should look like at the end of this part of the tutorial.

## Adding the responder branch to our survey

Because the responder branch is similar to the proposer branch, we'll skip the notebook and work straight in `survey.py`. I'll point out the differences as we go along.

First, let's add a navigate function to the end of our ultimatum game branch to bring us to the responder branch:

```python
...

def ultimatum_game(start_branch):
    proposer = assigner.next()['Proposer']
    return Branch(
        ...
        navigate=proposer_branch if proposer else responder_branch
    )

...

def responder_branch(ug_branch):
    branch = Branch(navigate=end)
    for i in range(N_ROUNDS):
        response_input = Blank(
            ('''
            The proposer has ${} to split between him/herself and you. Fill in the blank:
            
            I will accept any proposal which gives me at least **$'''.format(POT), '.00**.'),
            prepend='$', append='.00',
            var='Response', blank_empty='__',
            type='number', min=0, max=POT, required=True
        )
        branch.pages += [
            Page(
                Label(progress(
                    i/N_ROUNDS, 'Round {} of {}'.format(i+1, N_ROUNDS)
                )),
                response_input
            ),
            Page(
                Label(
                    compile=C.display_responder_outcome(response_input)
                )
            )
        ]
    return branch
```

Like in the proposer branch, we add two pages to the responder branch for each of `N_ROUNDS`. Just as the first of these two pages asked the proposer for the proposal in the proposer branch, the first of these two pages asks the responder for their response in the responder branch. Like in the proposer branch, the second of these pages displays the outcome of the round.

## Displaying the responder outcome

We register a compile function to display the responder outcome.

```python
...

@C.register
def display_responder_outcome(outcome_label, response_input):
    # get the response
    response = response_input.data
    #randomly select a proposal
    proposal_inputs = Blank.query.filter(
        Blank.var=='Proposal', Blank.data!=None
    ).all()
    if proposal_inputs:
        # randomly choose a proposal
        offer = random.choice(proposal_inputs).data
    else:
        # no proposals are available
        # e.g. if this is the first participant
        offer = randint(0, POT)
    proposal = POT-offer, offer
    # compute the payoff
    accept = response <= proposal[1]
    payoff = proposal if accept else (0, 0)
    # record results as embedded data
    outcome_label.page.embedded = [
        Embedded('Proposal', proposal[1]),
        Embedded('Accept', int(accept)),
        Embedded('ProposerPayoff', payoff[0]),
        Embedded('ResponderPayoff', payoff[1])
    ]
    # describe the outcome of the round
    outcome_label.label = '''
        The proposer proposed the following split:

        - Proposer: ${}
        - You: ${}

        You said you will accept any proposal that gives you at least ${}.
        
        **You {} the proposal, giving you a payoff of ${}.**
    '''.format(
        proposal[0], proposal[1],
        response,
        'accepted' if accept else 'rejected', 
        payoff[1]
    )
```

This is similar to the `display_proposer_outcome` compile function. First, it gets the responder's response. Second, it matches the responder with a random proposer. If no proposer is avaiable (e.g. if the responder is the first participant in the survey), it generates a random proposal. Third, we compute the payoff for the round and record it using embedded data. Finally, we update the label to display the outcome of the round to the responder.

Run the app to see what the survey looks like in the responder condition.

## Summary

In this part of the tutorial, you implemented the responder branch.

In the next part of the tutorial, you'll learn how to use hemlock's cutom debugger to make sure everything is running smoothly.