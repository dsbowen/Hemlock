from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

import os

src_href = Github('https://github.com/dsbowen/hemlock/blob/master')

# application and settings
path = 'hemlock/app/__init__.py'
soup = PySoup(path=path, src_href=src_href)
path = 'hemlock/app/settings.py'
soup.objects += PySoup(path=path, src_href=src_href).objects
compile_md(soup, outfile='docs_md/app.md')

# debugging
path = 'hemlock/debug/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.keep_objects('debug', 'run_batch', 'run_participant')
compile_md(soup, outfile='docs_md/debug.md')

# functions
function_filenames = ('compile', 'debug', 'submit', 'validate')
for filename in function_filenames:
    path = os.path.join('hemlock/functions', filename+'.py')
    soup = PySoup(path=path, src_href=src_href)
    outfile = os.path.join('docs_md/functions', filename+'.md')
    compile_md(soup, outfile=outfile)

# models
def mod_base(soup):
    soup.rm_objects('BranchingBase')
    soup.import_path = 'hemlock.models'

def mod_question(soup):
    check = soup.objects[-1]
    check.rm_methods('validate_choice')

modifications = {'bases': mod_base, 'question': mod_question}
modifications = {}

model_filenames = [
    'bases',
    'branch',
    'embedded',
    'functions',
    'page',
    'participant',
    'question',
    'worker',
]

for filename in model_filenames:
    path = os.path.join('hemlock/models', filename+'.py')
    soup = PySoup(path=path, src_href=src_href)
    soup.import_path = 'hemlock'
    soup.rm_properties()
    func = modifications.get(filename)
    if func:
        func(soup)
    outfile = os.path.join('docs_md/models', filename+'.md')
    compile_md(soup, outfile=outfile)

# question polymorphs
def mod_input_group(soup):
    soup.objects[1].import_path = 'hemlock.qpolymorphs.'

def mod_check(soup):
    soup.objects[1].import_path = 'hemlock.qpolymorphs.check.'
    
modifications = {
    'input_group': mod_input_group,
    'check': mod_check
}
modifications = {}

qpolymorph_filenames = [
    'bases',
    'blank',
    'check',
    'choice',
    'dashboard',
    'download',
    'file',
    'input',
    'label',
    'range',
    'select',
    'textarea',
]

for filename in qpolymorph_filenames:
    path = os.path.join('hemlock/qpolymorphs', filename+'.py')
    soup = PySoup(path=path, src_href=src_href)
    soup.import_path = 'hemlock'
    soup.rm_properties()
    func = modifications.get(filename)
    if func:
        func(soup)
    outfile = os.path.join('docs_md/questions', filename+'.md')
    compile_md(soup, outfile=outfile)

# tools
tools_filenames = [
    'comprehension',
    'lang',
    'mturk',
    'navbar',
    'progress',
    'random',
    'statics',
    'titrate',
    'utils',
]

for filename in tools_filenames:
    path = os.path.join('hemlock/tools', filename+'.py')
    soup = PySoup(path=path, parser='sklearn', src_href=src_href)
    soup.import_path = 'hemlock/tools'
    soup.rm_properties()
    outfile = os.path.join('docs_md/tools', filename+'.md')
    compile_md(soup, compiler='sklearn', outfile=outfile)