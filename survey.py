from articles import ARTICLES, ARTICLE_NAMES

import pandas as pd
from hemlock import Branch, Page, Embedded, Label, RangeInput, route
from hemlock.tools import Assigner, consent_page, completion_page
from hemlock_demographics import basic_demographics
from joblib import load

import random

N_ARTICLES = 10

# assigner = Assigner({'Ideal': (0, 1)})
assigner = Assigner({'Condition': ('random', 'actual', 'ideal')})
reg = load('model.p')
X_cols = [
    'Ideal',
    'RaceWhite',
    'RaceBlack',
    'RaceSouth Asian',
    'RaceEast Asian',
    'RaceArabic or Central Asian',
    'RaceOther',
    'Male',
    'Age',
    'ArticleNames'
]

@route('/survey')
def start():
    assigner.next()
    return Branch(
        consent_page(
            'By continuing this survey you consent to sell us your first-born child for a price no greater than $103.23.'
        ),
        basic_demographics(page=True, require=True),
        navigate=rate_articles,
        navigate_worker=True
    )

def rate_articles(start_branch):
    # def gen_rating_page(name, headline, link):
    #     page = Page(
    #         Label(
    #             'Consider this article: <b>{}</b>'.format(headline)
    #         ),
    #         RangeInput(
    #             'From 0 (not at all) to 10 (very much), how much do you think you would enjoy reading this article?',
    #             min=0, max=10, var='Enjoy',
    #             required=True
    #         )
    #     )
    #     if start_branch.part.meta['Ideal']:
    #         page.questions.insert(
    #             1,
    #             Label(
    #                 'Imagine what an ideal version of you would think of reading this article.'
    #             )
    #         )
    #     return page

    def gen_rating_page(name, headline, link):
        return Page(
            Label(
                'Take a couple of minutes and read <a href="{}" target="blank_">this article</a>.'.format(link)
            ),
            RangeInput(
                'From 0 (not at all) to 10 (very much), how much did you enjoy reading that article?',
                min=0, max=10, var='Enjoy',
                require=True
            )
        )

    # articles = random.sample(ARTICLES, k=N_ARTICLES)
    articles = select_articles(start_branch.part)
    start_branch.embedded.append(
        Embedded(
            var='ArticleNames', 
            data=[name for name, headline, ulr in articles])
    )
    return Branch(
        *[gen_rating_page(*article) for article in articles],
        navigate=end
    )

def select_articles(part):
    if part.meta['Condition'] == 'random':
        return random.sample(ARTICLES, k=N_ARTICLES)
    df = pd.DataFrame(part.get_data())
    df = df.append((len(ARTICLE_NAMES)-1)*[df], ignore_index=True)
    df['Ideal'] = df.Condition == 'ideal'
    df['ArticleNames'] = ARTICLE_NAMES
    X = df[X_cols]
    y_pred = reg.predict(X)
    article_ratings = list(zip(ARTICLES, y_pred))
    article_ratings.sort(key=lambda x: x[1], reverse=True)
    print('Selected articles', article_ratings)
    return [article for article, rating in article_ratings][:N_ARTICLES]

def end(rate_articles_branch):
    return Branch(
        completion_page()
    )