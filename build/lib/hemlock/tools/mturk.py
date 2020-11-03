from .random import key

from flask_login import current_user

def consent_page(consent_label, input_label, require=True):
    from ..models import Page
    from ..qpolymorphs import Label, Input

    return Page(
        Label(consent_label),
        Input(input_label, required=require, submit=_record_id)
    )

def _record_id(id_input):
    current_user.meta['ParticipantID'] = id_input.data

def completion_page():
    from ..models import Page
    from ..qpolymorphs import Label

    code = key(6)
    current_user.meta['CompletionCode'] = code
    return Page(
        Label(
            '''Thank you for completing the study. Your completion code is 
            <b>{}</b>.'''.format(code)
        ),
        terminal=True
    )