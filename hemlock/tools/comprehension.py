"""# Comprehension check"""

ERROR_MSG = """
<p>Your response was incorrect.</p>
<p>Please reread the instructions before continuing.</p>
"""

def comprehension_check(branch, instructions=[], checks=[], attempts=None):
    """
    Add a comprehension check to a branch.

    A comprehension check consists of 'instruction' pages followed by 'check' pages. The data of all questions in a check page must evaluate to `True` to pass the check. When a participant fails a check, he is brought back to the first instructions page. 
    
    Participants only have to pass each check once. For example, suppose there are two checks, 0 and 1. A participant passes check 0 but fails check 1. He is brought back to the first page of the instructions. After rereading the instructions, he is brought directly to check 1, skipping check 0.

    Parameters
    ----------
    branch : hemlock.Branch
        Branch to which the comprehension check is attached.

    instructions : hemlock.Page or list of hemlock.Page
        Instruction page(s).

    checks : hemlock.Page or list of hemlock.Page
        Check page(s).

    attempts : int or None, default=None
        Number of attempts allotted. Participants are allowed to proceed with the survey after exceeding the maximum number of attempts. If `None`, participants must pass the comprehension check before continuing the survey.

    Returns
    -------
    branch : hemlock.Branch
        The original branch, with added comprehension check.

    Notes
    -----
    This function adds a `hemlock.Submit` function to each check page. This must be the last submit function of each check page.    
    """
    assert instructions and checks, (
        '`instructions` and `checks` must be non-empty lists of hemlock.Pages'
    )
    from hemlock.app import db
    from hemlock.models import Submit
    if not isinstance(instructions, list):
        instructions = [instructions]
    if not isinstance(check, list):
        checks = [checks]
    branch.pages += instructions + checks
    for check in checks:
        check.back_to = instructions[0]
        Submit(
            page = check,
            func = _verify_data,
            last_instr_page = instructions[-1],
            curr_attempt = 1,
            attempts = attempts
        )
    return branch

def _verify_data(check, last_instr_page, curr_attempt, attempts):
    """
    Verify that the data on the comprehension page is correct.

    Parameters
    ----------
    check : hemlock.Page
        Check page.

    last_instr_page : hemlock.Page
        Last instructions page.

    curr_attempt : int
        Current attempt number.

    attempts : int or None
        Maximum number of attempts.
    """
    if all(q.data for q in check.questions) or curr_attempt == attempts:
        if check != check.branch.pages[-1]:
            # this check does not have to be repeated
            last_instr_page.forward_to = check.branch.pages[check.index+1]
        return
    check.back_to.error = ERROR_MSG
    check.direction_from = 'back'
    check.submit_functions[-1].kwargs['curr_attempt'] = curr_attempt + 1