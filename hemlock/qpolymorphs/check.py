"""# Check"""

from ..app import db, settings
from ..models import ChoiceQuestion

def click_choices(driver, question):
    """
    Default check debug funtion. See [click choices](debug_functions.md).
    """
    from ..functions.debug import click_choices as click_choices_
    click_choices_(driver, question)

settings['Check'] = {
    'align': 'left',
    'inline': False,
    'debug_functions': click_choices,
    'multiple': False,
}


class Check(ChoiceQuestion):
    """
    Check questions use radio inputs if only one choice can be selected, or 
    checkbox inputs if multiple choices can be selected.

    Inherits from [`hemlock.ChoiceQuestion`](question.md).

    By default, choices are positioned vertically. To position them 
    horizontally, set `inline` to True.

    Parameters
    ----------
    page : hemlock.Page or None, default=None
        Page to which this question belongs.

    template : str, default='hemlock/check.html'
        Template for the check body.

    Attributes
    ----------
    align : str, default='left'
        Choice alignment; `'left'`, `'center'`, or `'right'`.

    choice_wrapper : bs4.Tag
        Tag fo the choice html wrapper.

    inline : bool, default=False
        Indicates that choices should be [inline](https://getbootstrap.com/docs/4.0/components/forms/#inline), 
        as opposed to vertical.

    multiple : bool, default=False
        Indicates that the participant may select multiple choices.

    Examples
    --------
    ```python
    from hemlock import Page, Check, push_app_context

    push_app_context()

    p = Page()
    c = Check(p, label='<p>This is a checkbox question.</p>')
    c.choices = ['Yes', 'No', 'Maybe']
    p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'check'}

    inline = db.Column(db.Boolean, default=False)

    def __init__(self, page=None, template='hemlock/check.html', **kwargs):
        super().__init__(page, template, **kwargs)

    @property
    def align(self):
        choice_wrapper = self.choice_wrapper
        if not choice_wrapper:
            return
        for class_ in choice_wrapper['class']:
            if class_ == 'text-left':
                return 'left'
            if class_ == 'text-center':
                return 'center'
            if class_ == 'text-right':
                return 'right'

    @align.setter
    def align(self, align_):
        choice_wrapper = self.choice_wrapper
        if not choice_wrapper:
            raise AttributeError('Choice wrapper does not exist')
        align_classes = ['text-'+i for i in ['left','center','right']]
        choice_wrapper['class'] = [
            c for c in choice_wrapper['class'] if c not in align_classes
        ]
        if align_:
            align_ = 'text-' + align_
            choice_wrapper['class'].append(align_)
        self.body.changed()

    @property
    def choice_wrapper(self):
        return self.body.select_one('.choice-wrapper')