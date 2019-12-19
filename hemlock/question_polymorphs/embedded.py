"""Embedded question polymorph"""

from hemlock.question_polymorphs.utils import *


class Embedded(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}

    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    
    @Question.init('Embedded')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}