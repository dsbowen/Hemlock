from hemlock import Branch, Page, Binary, Check, Input, Label, Range, Textarea, Compile as C, Validate as V, route
from hemlock_demographics import demographics
from hemlock_berlin import berlin
from hemlock_crt import crt

consent_label = '''
<p>Hello! We are researchers at the University of Pennsylvania studying how people make predictions. In this study, you will be using an experimental platform to answer some questions.</p>

<p><b>Because this is an experimental platform, you may encounter errors during this survey. If you experience an error, please email Dillon Bowen at dsbowen@wharton.upenn.edu. Copy this email address now in case you encounter an error during the survey.</b></p>

<p> We thank you in advance for your patience while using this platform.</p>

<p><b>Purpose.</b> The purpose of this study is to explore how people think about the future.</p> 

<p><b>Procedure.</b> We will ask you to complete a survey that will take approximately 2-5 minutes.</p> 

<p><b>Benefits & Compensation.</b> If you complete the survey, we will pay you $1.</p> 

<p><b>Risks.</b> There are no known risks or discomforts associated with participating in this study. Participation in this research is completely voluntary. You can decline to participate or withdraw at any point in this study without penalty though you will not be paid.</p> 

<p><b>Confidentiality.</b> Every effort will be made to protect your confidentiality. Your personal identifying information will not be connected to the answers that you put into this survey, so we will have no way of identifying you. We will retain anonymized data for up to 5 years after the results of the study are published, to comply with American Psychological Association data-retention rules.</p> 

<p><b>Questions</b> Please contact the experimenters if you have concerns or questions: dsbowen@wharton.upenn.edu. You may also contact the office of the University of Pennsylvania’s Committee for the Protection of Human Subjects, at 215.573.2540 or via email at irb@pobox.upenn.edu.</p>
'''

@route('/survey')
def start():
    return Branch(
        Page(
            Label(consent_label),
            Input('To consent, please enter your MTurk ID.', required=True)
        ),
        demographics('age_bins', 'gender', 'race', page=True, require=True),
        berlin(require=True),
        *crt(page=True, require=True),
        navigate=forecast
    )

# @route('/survey')
def forecast(origin=None):
    prediction_q = Range(
        'Fill in the blank: There is a _____ in 100 chance that Joe Biden will win the presidential election.',
        prepend='There is a ', append=' in 100 chance', var='Forecast'
    )
    return Branch(
        Page(
            prediction_q,
            timer='FcastTime'
        ),
        Page(
            Label(compile=C.confirm_prediction(prediction_q)),
            back=True, timer='ConfirmTime'
        ),
        Page(
            Binary(
                "Did the survey 'crash' at any point? For example, did you see an 'Internal Server Error' message?",
                var='Crash',
                validate=V.require()
            ),
            Check(
                'How often did the pages take a long time (3 or more seconds) to load?',
                [
                    ('Never: the pages always loaded in less than 3 seconds', 0),
                    ('1 or 2 pages took at least 3 seconds to load', 1),
                    ('3 or more mages took at least 3 seconds to load', 2)
                ],
                var='Runtime',
                validate=V.require()
            ),
            Range(
                "From 1 (hardest) and 7 (easiest), how easy was it to use this survey?",
                var='Easy',
                min=1, max=7
            ),
            Textarea(
                'Do you have any suggestions for improving the platform?',
                var='Improve'
            ),
            timer='EvalTime'
        ),
        Page(
            Label('Thank you for completing the study. Your completion code is <b>hlk235</b>.'),
            terminal=True
        )
    )

@C.register
def confirm_prediction(confirm_label, prediction_q):
    confirm_label.label = '''
        <p>You predicted that there is a {} in 100 chance that Joe Biden will win the presidential election</p>
        Click >> to confirm your prediction or << to change your prediction.
    '''.format(prediction_q.response)