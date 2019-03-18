###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/19/2019
###############################################################################

'''
TODO:
general cleaning, incl routes folder and relationships (as opposed to queries)
for debugging, pass args to start function
back for branch embedded dataframe
record empty dataframe
vaidation bank
css - larger margins
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, modg, g, comprehension_check, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer
from hemlock.validation_bank import *
from config import Config
import pandas as pd
import numpy as np
from random import choice, shuffle
from copy import deepcopy
from flask_login import current_user

def render_function(q):
    q.reset_default()
    q.randomize()

# def Start():
    # instructions = Page()
    # Question(instructions, 'Here are some instructions', var='comp_check')
    
    # check = Page()
    # q = Question(check, 'Did you understand the instructions?', 'single choice')
    # Choice(q, 'Yes', 1)
    # Choice(q, 'No', 0)
    # q.render(render_function)
        
    # return comprehension_check(instructions.id, check.id, End, max_attempts=2)
    
# def End():
    # b = Branch()
    # p = Page(b, terminal=True)
    # Question(p, 'Thank you for participating')
    
    # return b
    

def Start():
    b = Branch(next=PreferenceQuestions)
    
    disclosed = random_assignment(b, 'condition', ['disclosed'], [[0,1,]])
    modg({'disclosed':disclosed})
    
    p = Page(b)
    q = Question(p, '''
    <p>We are researchers at the University of Pennsylvania and we are studying decision making. In this survey, you will be asked to make some estimates. Please be assured that your responses will be kept completely confidential.</p>
    <p>&nbsp;</p>
    <p>The survey will take you approximately 10 minutes to complete. For completing this survey, you will be compensated $1 by MTurk.&nbsp;</p>
    <p>&nbsp;</p>
    <p>Your participation in this research is voluntary. You have the right to withdraw from the study at any point and for any reason without penalty.</p>
    <p>&nbsp;</p>
    <p>We will make every effort to keep all the information you tell us during the study strictly confidential, except as required by law.&nbsp; Your name and other identifying information will never be connected with the responses you provide so no one will ever be able to identify you in any publications that will result from this research. If you have questions about your rights as a volunteer in this research study you can contact the Office of Regulatory Affairs at the University of Pennsylvania at (215)-898-2614. &nbsp; &nbsp; &nbsp; &nbsp;</p>
    <p>&nbsp;</p>
    <p><strong>By continuing with this survey, you acknowledge that you have read the information above and are consenting to participate.</strong></p>
    ''')
    q = Question(p, 'Enter your MTurk ID', 'free', 'workerId', all_rows=True)
    Validator(q, require)
    
    return b
    
def PreferenceQuestions():
    b = Branch()
    
    p = Page(b)
    q = Question(p, '''
    On the next page, we will ask you some questions about your behaviors and preferences. Please answer them honestly. Your responses will be confidential.
    ''')
    
    p = Page(b)
    [preference_question(p.id, text) for text in preference_question_texts]
    preference_question(p.id, 'Do you prefer tea or coffee?', 'Tea', 'Coffee')
    preference_question(p.id, 'Which sport do you prefer: basketball or football?', 'Basketball', 'Football')
    p.randomize()
    
    if g('disclosed'):
        b.next(DisclosedInstructions)
    else:
        b.next(Estimates)

    return b
    
preference_question_texts = [
    'Did you attend a music concert this year?',
    'Have you ever been to New York City?',
    'Do you enjoy swimming in the ocean?',
    'Have you ever spent the night outdoors in a tent?',
    'Did you read a book this summer?',
    'Do you typically go to bed before 11pm?',
    'Have you watched at least one episode of Stranger Things on Netflix?',
    'Have you ever seen the movie The Shining?']
    
def preference_question(p_id, text, choice1='Yes', choice2='No'):
    q = Question(query(p_id,Page), text, 'single choice', 'preference')
    Choice(q, choice1, 1, label='yes')
    Choice(q, choice2, 0, label='no')
    q.randomize()
    Validator(q, require)
    
def DisclosedInstructions():
    if g('attempt') is None:
        modg({'attempt':0})
    modg({'attempt':g('attempt')+1})

    b = Branch()
    
    p = Page(b)
    Question(p, '''
    <p>On the next pages, we will ask you to estimate the behaviors and preferences of all people completing this survey.&nbsp;</p>
    <p>&nbsp;</p>
    <p><strong>For each of the questions, we will ask you to make two estimates. You will first make one estimate, and then we will ask you to make a second estimate for that same question.</strong>&nbsp;You will be asked to make a second estimate that is not exactly the same as your first estimate.&nbsp;</p>
    <p>&nbsp;</p>
    <p>You should do your best to be accurate. You will receive a bonus of $1 if your guesses are on average less than 10 percentage points away from the answers that all survey responders give.</p>
    <p>&nbsp;</p>
    <p><strong>Since you will be making two estimates for each question, this will give you two chances to make correct estimates, and thus two chances to win a bonus.&nbsp; We will take the better of your estimates for each of the questions to determine your bonus payment.</strong></p>
    <p>&nbsp;</p>
    <p>Participants will receive their bonus via MTurk within one week of completing this survey.&nbsp;</p>
    ''')
    
    p = Page(b)
    q = Question(p, 'To be sure you read and understood the instructions, please indicate how your bonus will be determined:', 'single choice', all_rows=True)
    q.var('comprehension{0}'.format(g('attempt')))
    Choice(q, 'I will be asked to make one estimate for each question and this estimate will determine my bonus.', 0, label='incorrect1')
    Choice(q, 'I will be asked to make two estimates for each question, but only the first will determine my bonus', 0, label='incorrect2')
    Choice(q, 'I will be asked to make two estimates for each question, but only the second estimate will determine my bonus.', 0, label='incorrect3')
    Choice(q, 'I will be asked to make two estimates for each question and the better fo these two estimates will determine my bonus.', 1, label='correct')
    q.randomize()
    
    modg({'comp_check':q.id})
    
    b.next(CheckComprehension)
    
    return b
    
def CheckComprehension():
    correct = query(g('comp_check')).get_data()
    if correct or g('attempt')>3:
        if g('disclosed'):
            return Estimates()
        return Branch()
    if g('disclosed'):
        b = Branch(next=DisclosedInstructions)
    else:
        b = Branch(next=SurpriseInstructions)
    p = Page(b)
    Question(p, 'Your response to the previous question was incorrect. Click >> to see the instructions again.')
    return b
    
est_texts = [
    'attended a music concert this year']
    # 'have been to New York City',
    # 'enjoy swimming in the ocean',
    # 'have spent the night outdoors in a tent',
    # 'read a book this summer',
    # 'typically go to bed before 11pm',
    # 'have watched at least one episode of Stranger Things on Netflix',
    # 'have seen the movie The Shining',
    # 'prefer tea over coffee',
    # 'prefer basketball over football'
    # ]
    
def est_page(p_id, text, first_est_id=None):
    p = query(p_id, Page)
    if first_est_id is not None:
        q = Question(p)
        q.render(estimate_reminder, [first_est_id,text])
    q = Question(p, 'What percent of survey respondents {0}?'.format(text), 'free', 'FirstEst')
    Validator(q, require)
    Validator(q, integer)
    Validator(q, in_range, [0,100])
    if first_est_id is not None:
        q.var('SecondEst')
        Validator(q, different_second_est, first_est_id)
    return q.id
    
def estimate_reminder(q, args):
    firstest_id, text = args
    firstest = query(firstest_id).get_data()
    q.text('''
    <p>You estimated that {0} percent of survey respondents {1}.</p>
    <p>We would now like you to guess the answer to this question again, this time giving a different answer than the one you gave before.</p>
    '''.format(firstest, text))
    
def different_second_est(second_est, first_est_id):
    first_est = query(first_est_id)
    if second_est.get_data() == first_est.get_data():
        return 'Your second estimate should be different from your first'
    
def Estimates():
    b = Branch(next=Exit)
    
    [Question(branch=b, qtype='embedded', var='preference_label', data=text)
        for text in est_texts]
    
    firstest_pages = [Page() for i in range(len(est_texts))]
    firstest_questions = [est_page(p.id,t) 
        for (p,t)in zip(firstest_pages, est_texts)]
    secondest_pages = [Page() for i in range(len(est_texts))]
    [est_page(p.id,t,q_id) 
        for (p,t,q_id) in zip(secondest_pages, est_texts, firstest_questions)]
    
    order = list(range(len(est_texts)))
    shuffle(order)
    
    if g('disclosed'):
        for i in order:
            firstest_pages[i].branch(b)
            secondest_pages[i].branch(b)
    else:
        [firstest_pages[i].branch(b) for i in order]
        firstest_pages[order[-1]].next(SurpriseInstructions)
        [secondest_pages[i].branch(b) for i in order]
    
    return b
    
def SurpriseInstructions():
    if g('attempt') is None:
        modg({'attempt':0})
    modg({'attempt':g('attempt')+1})

    b = Branch()
    
    p = Page(b)
    Question(p, '''
    <p>On the next pages, we will ask you to estimate the behaviors and preferences of all people completing this survey again.</p>
    <p>&nbsp;</p>
    <p>We would like you to make a second estimate that is not exactly the same as your first estimate.&nbsp;</p>
    <p>&nbsp;</p>
    <p><strong>This will give you a second chance to make correct estimates for the behaviors and preferences of people completing this survey, and thus a second chance to earn a bonus.&nbsp;</strong>Recall that you will receive a bonus&nbsp;of $1 if your guesses are on average less than 10 percentage points away from the answers that all survey responders give.&nbsp;<strong>We will take the better&nbsp;of your estimates for each of the questions to determine your bonus payment.</strong><strong>&nbsp;</strong></p>
    <p>&nbsp;</p>
    <p>Participants will receive their bonus via MTurk within one week of completing this survey.</p>
    ''')
    
    p = Page(b)
    q = Question(p, 'To be sure that you read and understood the instructions, please indicate how your bonus will be determined:', 'single choice', all_rows=True)
    q.var('comprehension{0}'.format(g('attempt')))
    Choice(q, 'Only the estimates I previously gave (i.e. my first estimates) will be used to determine my bonus.', 0, label='incorrect1')
    Choice(q, 'Only the estimates I am about to give (i.e. my second estimates) will be used to determine my bonus.', 0, label='incorrect2')
    Choice(q, 'The better of my first and second estimates will be used to determine my bonus', 1, label='correct')
    q.randomize()
    
    modg({'comp_check':q.id})
    b.next(CheckComprehension)
    
    return b
    
def Exit():
    b = Branch()
    
    p = Page(b)
    q = Question(p, 'Please indicate your gender', 'single choice', 'Gender', all_rows=True)
    Choice(q, 'Male', 1)
    Choice(q, 'Female', 0)
    Validator(q, require)
    
    q = Question(p, 'How old are you?', 'free', 'Age', all_rows=True)
    Validator(q, require)
    Validator(q, integer)
    
    p = Page(b)
    q = Question(p, 'If you had to bet, which set of estimates do you think is more accurate on average?', 'single choice', 'MoreAccurage', all_rows=True)
    Choice(q, 'The first set', 1, label='first_set')
    Choice(q, 'The second set', 2, label='second_set')
    q.randomize()
    Validator(q, require)
    
    q = Question(p, 'Did you try harder to be accurate when making your first set of estimates or when making your second set of estimates?', 'single choice', 'TryHarder', all_rows=True)
    Choice(q, 'The first set', 1, label='first_set')
    Choice(q, 'The second set', 2, label='second_set')
    Choice(q, 'I was trying equally hard on the first and second set', 0, label='equal')
    q.randomize()
    Validator(q, require)
    
    p = Page(b, terminal=True)
    Question(p, 'Thank you for your participation. Completion code xxxx')
    
    return b
        
app = create_app(Config, 
    start=Start, 
    password='123',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}