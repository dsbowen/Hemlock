"""Page settings"""

from hemlock.app import Settings
from hemlock.tools import gen_external_css, gen_external_js, url_for

from bs4 import BeautifulSoup

from random import random, shuffle
from time import sleep

def default_css():
    attrs_list = [
        {
            'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
            'id': 'bootstrap-css'
        },
        {
            'href': url_for('hemlock.static', filename='css/default.css'),
            'id': 'hemlock-css'
        }
    ]
    css = BeautifulSoup('', 'html.parser')
    [css.append(gen_external_css(**attrs)) for attrs in attrs_list]
    return css

def default_js():
    attrs_list = [
        {
            'src': 'https://code.jquery.com/jquery-3.4.1.min.js',
            'id': 'jquery'
        },
        {
            'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
            'id': 'popper'
        },
        {
            'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
            'id': 'bootstrap-js'
        },
        {
            'src': url_for('hemlock.static', filename='js/default.js'),
            'id': 'hemlock-js'
        }
    ]
    js = BeautifulSoup('', 'html.parser')
    [js.append(gen_external_js(**attrs)) for attrs in attrs_list]
    return js

def compile_fn(page):
    [q._compile() for q in page.questions]

def validate_fn(page):
    [q._validate() for q in page.questions]
    
def submit_fn(page):
    [q._submit() for q in page.questions]

def debug_fn(page, driver):
    """Call question debug functions in random order then navigate"""
    order = list(range(len(page.questions)))
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]
    forward_exists = back_exists = True
    if random() < .8:
        try:
            driver.find_element_by_id('forward-btn').click()
        except:
            forward_exists = False
    if random() < .5:
        try:
            driver.find_element_by_id('back-btn').click()
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(3)
    driver.refresh()

@Settings.register('Page')
def page_settings():
    return {
        'css': default_css(),
        'js': default_js(),
        'back': False,
        'forward': True,
        'compile_functions': compile_fn,
        'validate_functions': validate_fn,
        'submit_functions': submit_fn,
        'debug_functions': debug_fn,
    }