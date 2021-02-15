"""# MTurk utilities"""

from .random import key

import numpy as np
import pandas as pd
from flask_login import current_user

ID_LABEL = '<p>Enter your MTurk ID to consent</p>'
CONFIRM_LABEL = '<p>Confirm your ID</p>'

def consent_page(
        consent_label=None, 
        id_label=ID_LABEL, 
        confirm_label=CONFIRM_LABEL, 
        require=True
    ):
    """
    Parameters
    ----------
    consent_label : str or None, default=None
        The consent terms for your study. If `None`, the consent label is
        omitted.

    id_label : str, default='Enter your MTurk ID to consent'
        Label asking workers to enter their ID.

    confirm_label : str, default='Confirm your ID'
        Label asking for confirmation.

    require : bool, default=True
        Indicates that workers are required to enter their ID.

    Returns
    -------
    consent page : hemlock.Page
    """
    from ..models import Page, Debug as D, Validate as V
    from ..qpolymorphs import Label, Input

    id_q = Input(
        id_label, 
        required=require, 
        debug=D.send_keys('test'), 
        submit=_record_id
    )
    page = Page(
        id_q,
        Input(
            confirm_label, 
            required=require,
            debug=D.send_keys('test'),
            validate=V.match(
                id_q, error_msg='IDs do not match'
            )
        )
    )
    if consent_label:
        page.questions.insert(0, Label(consent_label))
    return page

def _record_id(id_input):
    current_user.meta['WorkerId'] = id_input.data.strip()

def completion_page(participant=None):
    """
    Parameters
    ----------
    participant : hemlock.Participant or None, default=None
        Record the completion code in this participant's metadata. If `None`,
        the completion code is recorded in flask-login's `current_user`.

    Returns
    -------
    completion page: hemlock.Page
        Completion page with unique completion code.
    """
    from ..models import Page
    from ..qpolymorphs import Label

    code = key(6)
    part = participant or current_user
    part.meta['SurveyCode'] = code
    return Page(
        Label(
            '''
            <p>Thank you for completing the study. Your completion code is 
            <b>{}</b></p>
            
            The completion code is case-sensitive.
            '''.format(code)
        ),
        terminal=True
    )

def get_approve_df(data_df, batch_df, bonus=False, verbose=True):
    """
    Parameters
    ----------
    data_df : str or pd.DataFrame
        Hemlock survey data. This must have `'WorkerId'` and `'SurveyCode'` 
        columns.

    bonus : bool, default=False
        Indicates that workers will receive a bonus. If bonusing workers, `data_df`` must include a column called `'BonusAmount'`.

    verbose : bool, default=True
        Indicates to print information on approvals, rejections, and bonuses.

    Returns
    -------
    approve_df : pd.DataFrame
        Dataframe with approval and bonus information.

    Examples
    --------
    ```python
    from hemlock.tools import get_approve_df, approve_assignments

    approve_df = get_approve_df(data_df, 'path/to/batch.csv', bonus=True)
    ```

    Out:

    ```
    90 assignments approved
    10 assignments rejected
    Total bonus: $90
    ```

    ```python
    import boto3

    client = boto3.client('mturk')
    approve_assignments(client, approve_df, bonus=True, reason='Great job!')
    ```
    """
    if isinstance(data_df, str):
        data_df = pd.read_csv(data_df)
    data_df = data_df.drop_duplicates('WorkerId')
    if isinstance(batch_df, str):
        batch_df = pd.read_csv(batch_df)
    data_cols = ['WorkerId', 'SurveyCode', 'Status', 'ID']
    if bonus:
        data_cols.append('BonusAmount')
    df = batch_df.merge(
        data_df[data_cols], how='left', on='WorkerId'
    )
    df['Approve'] = df.SurveyCode == df['Answer.surveycode']
    if bonus:
        df['UniqueRequestToken'] = np.random.rand(len(df))
    if verbose:
        print('{} assignments approved'.format(df.Approve.sum()))
        print('{} assignments rejected'.format((~df.Approve).sum()))
        if bonus:
            print('Total bonus: ${:.2f}'.format(df.BonusAmount.sum()))
    return df

def approve_assignments(
        client, approve_df, approve=True, bonus=False, bonus_reason='', 
        OverrideRejection=False
    ):
    """
    Approve and reject assignments and pay bonuses.

    Parameters
    ----------
    client : boto3.client

    approve_df : pd.DataFrame
        Output of `get_approve_df`.

    approve : bool, default=True
        Indicates that assignments should be approved and rejected.

    bonus : bool, default=False
        Indicates that bonuses should be paid.

    bonus_reason : str, default=''
        Reason for giving bonuses. This must be nonempty if paying bonuses.

    OverrideRejection : bool, default=False
        Indicates that this function can override rejected assignments.
    """
    assert not bonus or bonus_reason, 'Please provide a reason for bonusing workers'
    def approve_assignment(x):
        if x.Approve:
            client.approve_assignment(
                AssignmentId=x.AssignmentId,
                OverrideRejection=OverrideRejection
            )
        else:
            client.reject_assignment(
            AssignmentId=x.AssignmentId,
            RequesterFeedback='''
                Could not verify completion code. If you believe this is a 
                mistake, please contact the requester.
                '''.strip()
        )
        
    def send_bonus(x):
        if x.Approve and x.BonusAmount > 0:
            client.send_bonus(
                WorkerId=x.WorkerId,
                BonusAmount=str(round(x.BonusAmount, 2)),
                AssignmentId=x.AssignmentId,
                Reason=bonus_reason,
                UniqueRequestToken=str(x.UniqueRequestToken)
            )
        
    if approve:
        approve_df.apply(approve_assignment, axis=1)
    if bonus:
        approve_df.apply(send_bonus, axis=1)