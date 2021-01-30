"""# Titration tool

Titration is used primarily to elicit willingness to pay or risk preferences.
"""

from ..app import db


def titrate(
        gen_titrate_q, distribution, var, data_rows=1, 
        tol=None, max_pages=None, **kwargs
    ):
    """
    Parameters
    ----------
    gen_titrate_q : callable
        Callable which takes the titration value and returns a 
        `hemlock.Question`. If the question's `data` evaluates to `True`, the
        next iteration will increase the titration value. If the question's 
        `data` evaluates to `False`, the next iteration will decrease the
        titration value.

    distribution : callable
        Callable with a `ppf` method which takes a quantile `q` and returns
        a value (e.g. `float`). I recommend `scipy.stats` distributions.

    var : str
        Name of the variable in which to store the titrated value.

    data_rows : int, default=1
        Number of data rows for the titration variable.

    tol : float or None, default=None
        Titration will stop when the titrated value reaches this precision. If
        `None`, titration stops after a certain number of questions.

    max_pages : int or None, default=None
        Titration will stop after this number of pages. If `None`, titration
        stops after a precision level is reached.

    \*\*kwargs :
        Keyword arguments are passed to the titration page constructor.

    Returns
    -------
    FIrst titration page : hemlock.Page
    
    Examples
    --------
    This example demonstrates how to use titration to more efficiently and
    precisely implement the 
    <a href="http://www.planchet.net/EXT/ISFA/1226.nsf/9c8e3fd4d8874d60c1257052003eced6/9ba2376a9b20919cc125784b00355f88/$FILE/HOLT.pdf" target="_blank">Holt-Laury risk elicitation method</a>. 
    The titration value is the probability at which the participant is 
    indifferent between two lotteries.

    We then compute the coefficient of relative risk aversion assuming CRRA 
    utility.


    ```python
    import numpy as np
    from hemlock import Branch, Page, Binary, Label, Validate as V, route
    from hemlock.tools import titrate
    from scipy.optimize import minimize
    from scipy.stats import uniform

    import math

    def gen_titrate_q(p_larger):
    \    # p_larger is the probability of winning the larger amount of money
    \    p = round(p_larger)
    \    return Binary(
    \        '''
    \        Which lottery would you rather have?
    \        ''',
    \        [
    \            '{}/100 of $2.00, {}/100 of $1.60'.format(p, 100-p),
    \            '{}/100 of $3.85, {}/100 of $0.10'.format(p, 100-p)
    \        ],
    \        inline=False, validate=V.require()
    \    )

    @route('/survey')
    def start():
    \    return Branch(
    \        titrate(gen_titrate_q, uniform(0, 100), var='p', tol=5, back=True),
    \        Page(
    \            Label(compile=disp_risk_aversion),
    \            back=True, terminal=True,
    \        )
    \    )

    def disp_risk_aversion(label):
    \    def func(r):
    \        def u(x):
    \            # CRRA utility function
    \            return x**(1-r) if abs(1-r) > .01 else math.log(x)

    \        return (p*u(2)+(1-p)*u(1.6)-p*u(3.85)-(1-p)*u(.1))**2

    \    p = label.part.g['p'] / 100. # indifference point between 0 and 1
    \    # coefficient of relative risk aversion if optimization starts from -3
    \    res_lower = minimize(func, x0=np.array([-3])).x
    \    # coefficient of relative risk aversion if optimization starts from 2
    \    res_upper = minimize(func, x0=np.array([2])).x
    \    # you can trivially minimize the function by setting r == 1 (approximately)
    \    # this sets u(x) = 0 (approx.) for all x
    \    # so choose the r farther from 1
    \    r = res_lower if abs(res_lower-1)>abs(res_upper-1) else res_upper
    \    label.label = '''
    \        Indifference point is {:.0f}/100. Coefficient of relative risk aversion is {:.2f}
    \        '''.format(100.*p, float(r))
    ```
    """
    assert tol is not None or max_pages is not None
    n_pages_left = None if max_pages is None else max_pages - 1
    # initial titration value is the median of the distribution
    x = distribution.ppf(.5)
    return _titrate(
        gen_titrate_q, x, distribution, .5, .25, var, data_rows, tol, 
        n_pages_left, **kwargs
    )

def _titrate(
        gen_titrate_q, x, distribution, q, step, var, data_rows, tol, 
        n_pages_left, **kwargs
    ):
    from ..models import Page, Submit as S

    page =  Page(gen_titrate_q(x), **kwargs)
    # submit function computes the next titration value
    page.submit.append(
        S(
            _gen_next_titrate_page, gen_titrate_q, x, distribution, q, step, 
            var, data_rows, tol, n_pages_left, **kwargs
        )
    )
    return page

def _gen_next_titrate_page(
        page, gen_titrate_q, prev_x, distribution, q, step, var, data_rows, 
        tol, n_pages_left, **kwargs
    ):
    def remove_titration_pages():
        # remove pages in front of this page which are part of the titration
        # e.g. after navigating back during titration, you will have stale
        # titration pages
        while (
            page != page.branch.pages[-1] 
            and isinstance(page.branch.pages[page.index+1].g, dict)
            and page.branch.pages[page.index+1].g.get('Titration')
        ):
            stale_titration_page = page.branch.pages.pop(page.index+1)
            db.session.delete(stale_titration_page)

    def record_x(x):
        # record the titration value as embedded data and in the participant's
        # `g`
        from ..models import Embedded

        x = float(x)
        page.part.embedded.append(Embedded(var, x, data_rows=data_rows))
        page.part.g[var] = x
        
    remove_titration_pages()
    # step the titration value
    q += step if page.questions[-1].data else -step
    x = distribution.ppf(q)
    if (
        n_pages_left == 0 
        or (tol is not None and abs(x - prev_x) < tol)
    ):
        return record_x(x)
    step /= 2.
    n_pages_left = None if n_pages_left is None else n_pages_left - 1
    new_page = _titrate(
        gen_titrate_q, x, distribution, q, step, var, data_rows, tol, 
        n_pages_left, **kwargs
    )
    # flag this as a titration page
    new_page.g = {'Titration': True}
    page.branch.pages.insert(page.index+1, new_page)