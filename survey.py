###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock.query import query
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

# def Start():
    # b = Branch()
    
    # q = Question(branch=b, var='condition', data='treatment', all_rows=True)
    # p = Page(branch=b, terminal=True)
    # q = Question(page=p, text='hello world')
    
    # return b

def Start():
    b = Branch(next=Thanks)
    
    condition = Question(branch=b, var='condition', data='control', all_rows=True)
    
    p = Page(branch=b)
    q = Question(page=p, text='Welcome to Hemlock!')
    q = Question(page=p, text="Let's start with some simple free response questions.")
    
    p = Page(branch=b)
    first = Question(page=p, var='first_name', qtype='free', all_rows=True)
    first.set_text("What's your first name?")
    last = Question(page=p, var='last_name', qtype='free', all_rows=True)
    last.set_text("...and your last name?")
    
    b.set_args({'first':first.id, 'last':last.id})
    
    return b
    
def ice_cream(page, index):
    q = Question(page=page, var='ice_cream', qtype='free')
    q.set_text('Favorite ice cream number '+str(index))

def Thanks(name_ids):
    b = Branch(next=FirstEst)
    
    p = Page(branch=b)
    name = query(name_ids)
    q = Question(page=p, text='Thanks for taking this survey, '+name['first'].data+' '+name['last'].data+'!')
    q = Question(page=p, text="Let's continue to some more simple free response questions.")
    
    p = Page(branch=b)
    q = Question(page=p, text="Alright, now, what are your three favorite flavors of ice cream?")
    for i in range(3):
        ice_cream(p, i+1)
    
    return b
    
def FirstEst():
    b = Branch()
    
    p = Page(branch=b, next=SecondEst)
    q = Question(page=p, var='first_est', qtype='free', text='Please make your first estimate')
    p.set_args(q.id)
    
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text="Thank you for taking my survey!")
    
    return b
    
def SecondEst(first_est_id):
    b = Branch()
    
    p = Page(branch=b)
    first_est = query(first_est_id).data
    q = Question(page=p, text='Your first estimate was '+str(first_est))
    q = Question(page=p, var='second_est', qtype='free', text='Please make your second estimate.')
    
    return b