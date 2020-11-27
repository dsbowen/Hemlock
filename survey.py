from hemlock import (
    Branch, Page, Embedded, Blank, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)
from hemlock.tools import consent_page, completion_page

from flask_login import current_user

@route('/survey')
def start():
    return Branch(
        Page(
            Label(
                'Page 0'
            )
        ),
        Page(
            Label(
                'Page 1'
            ),
            back=True, terminal=True,
            compile=log,
            # compile_worker=True
        )
    )

def log(page):
    print('here')

# "buildpacks": [
#         {"url": "heroku/python"},
#         {"url": "https://github.com/heroku/heroku-buildpack-chromedriver"},
#         {"url": "https://github.com/heroku/heroku-buildpack-google-chrome"}
#     ]