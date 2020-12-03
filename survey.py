from flask_login import current_user
from hemlock import Branch, Page, Embedded, Binary, Blank, Label, RangeInput, Compile as C, Validate as V, Submit as S, route
from hemlock.tools import consent_page, completion_page, titrate
from scipy.stats import uniform

import random
from functools import partial

@route('/survey')
def start():
    return Branch(
        Page(
            RangeInput(
                '<p>This is a range input</p>',
                var='RangeInputVar',
                default=5, 
                validate=V.require()
            )
        ),
        completion_page()
    )

# STEP = 5
# TOL = 1
# COMPANIES = [
#     'Barnes and Noble', 
#     'Uber', 
#     'DoorDash', 
#     'Amazon',
#     'Walmart',
#     'Target',
#     'Old Navy',
#     'GAP',
#     'JCPenny',
#     'Sears',
#     'Nordstrom',
#     "Kohl's",
#     'Best Buy',
#     'Apple Store',
#     'Bed, Bath, and Beyond',
#     'HomeGoods',
#     'Ikea',
#     'Home Depot',
#     "Lowe's",
#     'Costco',
#     "Dunkin' Donuts",
#     "Chili's",
#     'Starbucks',
#     'Chipotle',
#     'Burger King',
#     "McDonald's",
#     "Taco Bell",
#     "Wendy's",
#     "DICK's Sporting Goods",
#     "REI",
#     "Whole Foods"
# ]

# sure_thing_titrate_template = '''
# <p>Would you purchase a <b>${l_amount} {company} gift card</b> for <b>${price:.0f}</b>?</p>
# '''

# sure_thing_open_template = '''
# <p>How much would you pay for a <b>${l_amount} {company} gift card</b>?</p>
# '''

# raffle_titrate_template = '''
# <p>Imagine a raffle ticket that gives you a 90 in 100 chance to win a <b>${l_amount} 
# {company} gift card</b> and a 10 in 100 chance to win a <b>${h_amount} {company} gift 
# card</b>. (You can win one or the other, not both).</p>

# <p>Would you purchase this raffle ticket for <b>${price:.0f}</b>?</p>
# '''

# raffle_open_template = '''
# <p>Imagine a raffle ticket that gives you a 90 in 100 chance to win a <b>${l_amount} 
# {company} gift card</b> and a 10 in 100 chance to win a <b>${h_amount} {company} gift 
# card</b>. (You can win one or the other, not both).</p>

# <p>How much would you pay for this raffle ticket?</p>
# '''

# def gen_titrate_page(label_template, company, l_amount, h_amount, var):
#     return titrate(
#         partial(
#             gen_titrate_q,
#             label_template=label_template,
#             company=company,
#             l_amount=l_amount,
#             h_amount=h_amount
#         ),
#         uniform(0, h_amount),
#         var=var,
#         tol=TOL,
#         back=True
#     )

# def gen_titrate_q(price, label_template, company, l_amount, h_amount):
#     return Binary(
#         label_template.format(
#             price=price, company=company, l_amount=l_amount, h_amount=h_amount
#         ), 
#         validate=V.require()
#     )

# def gen_open_page(label_template, company, l_amount, h_amount, var):
#     return Page(
#         Blank(
#             (
#                 label_template.format(
#                     company=company, l_amount=l_amount, h_amount=h_amount
#                 )
#                 +'<p>I would pay up to $', '''</p>
#                 <p>I would not pay more than $''', '</p>'
#             ),
#             type='number', min=0, max=h_amount, required=True, var=var,
#             prepend='$', append='.00', blank_empty='_____'
#         )
#     )

# def select_amounts():
#     amounts= [0, 0]
#     while amounts[0] == amounts[1]:
#         amounts = [
#             STEP*round(random.uniform(STEP, 100)/STEP) for _ in range(2)
#         ]
#     return sorted(amounts)

# @route('/survey')
# def start():
#     titrate_co, open_co = random.sample(COMPANIES, k=2)
#     l_amount, h_amount = select_amounts()
#     current_user.embedded += [
#         Embedded('TitrateCo', titrate_co),
#         Embedded('OpenCo', open_co),
#         Embedded('LAmount', l_amount),
#         Embedded('HAmount', h_amount)
#     ]
#     pages = [
#         gen_titrate_page(
#             sure_thing_titrate_template, 
#             company=titrate_co,
#             l_amount=l_amount,
#             h_amount=h_amount,
#             var='SureThingTitrate'
#         ),
#         gen_titrate_page(
#             raffle_titrate_template,
#             company=titrate_co,
#             l_amount=l_amount,
#             h_amount=h_amount,
#             var='RaffleTitrate'
#         ),
#         gen_open_page(
#             sure_thing_open_template, 
#             company=open_co,
#             l_amount=l_amount,
#             h_amount=h_amount,
#             var='SureThingOpen'
#         ),
#         gen_open_page(
#             raffle_open_template,
#             company=open_co,
#             l_amount=l_amount,
#             h_amount=h_amount,
#             var='RaffleOpen'
#         )
#     ]
#     random.shuffle(pages)
#     return Branch(
#         consent_page(consent_label),
#         *pages,
#         completion_page()
#     )

# consent_label = '''
# <p>Hello! We are researchers at the University of Pennsylvania and are interested in understanding gift card purchases. Please read the information below and if you wish to participate, indicate your consent.</p>

# <p><b>Because this is an experimental platform, you may encounter errors during this survey. If you experience an error, please email Dillon Bowen at dsbowen@wharton.upenn.edu. Copy this email address now in case you encounter an error during the survey.</b></p>

# <p><b>Purpose.</b> The purpose of this study is to explore different ways of pricing gift cards.</p> 

# <p><b>Procedure.</b> You will take a survey which lasts approximately 1-2 minutes.</p> 

# <p><b>Benefits & Compensation.</b> We will pay you $0.20 on MTurk for completing this study.</p> 

# <p><b>Risks.</b> There are no known risks or discomforts associated with participating in this study.</p> 

# <p>Participation in this research is completely voluntary. You can decline to participate or withdraw at any point in this study without penalty though you will not be paid.</p> 

# <p><b>Confidentiality.</b> Every effort will be made to protect your confidentiality. Your personal identifying information will not be connected to the answers that you put into this survey, so we will have no way of identifying you. We will retain anonymized data for up to 5 years after the results of the study are published, to comply with American Psychological Association data-retention rules.</p> 

# <p><b>Questions</b> Please contact the experimenters if you have concerns or questions: dsbowen@wharton.upenn.edu. You may also contact the office of the University of Pennsylvania’s Committee for the Protection of Human Subjects, at 215.573.2540 or via email at irb@pobox.upenn.edu.</p>
# '''