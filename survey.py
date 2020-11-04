from hemlock import (
    Branch, Page, Embedded, Binary, Check, Input, Label, Range, Textarea, 
    Compile as C, Validate as V, route, settings
)
from hemlock.tools import consent_page, completion_page

settings['collect_IP'] = False

# "buildpacks": [
#         {"url": "heroku/python"},
#         {"url": "https://github.com/heroku/heroku-buildpack-chromedriver"},
#         {"url": "https://github.com/heroku/heroku-buildpack-google-chrome"}
#     ]

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Hello World', submit=delay)
        ),
        Page(
            Label('middle'),
        ),
        Page(
            Label('Goodbye world', compile=delay),
            back=True
        )
    )

def delay(label):
    import time
    for i in range(5):
        print(i)
        time.sleep(1)