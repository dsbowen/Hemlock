<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Titration tool

Titration is used primarily to elicit willingness to pay or risk preferences.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**titrate**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>titrate</b>(<i>gen_titrate_q, distribution, var, data_rows=1, tol=None, max_pages=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/titrate.py#L9">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>gen_titrate_q : <i>callable</i></b>
<p class="attr">
    Callable which takes the titration value and returns a <code>hemlock.Question</code>. If the question's <code>data</code> evaluates to <code>True</code>, the next iteration will increase the titration value. If the question's <code>data</code> evaluates to <code>False</code>, the next iteration will decrease the titration value.
</p>
<b>distribution : <i>callable</i></b>
<p class="attr">
    Callable with a <code>ppf</code> method which takes a quantile <code>q</code> and returns a value (e.g. <code>float</code>). I recommend <code>scipy.stats</code> distributions.
</p>
<b>var : <i>str</i></b>
<p class="attr">
    Name of the variable in which to store the titrated value.
</p>
<b>data_rows : <i>int, default=1</i></b>
<p class="attr">
    Number of data rows for the titration variable.
</p>
<b>tol : <i>float or None, default=None</i></b>
<p class="attr">
    Titration will stop when the titrated value reaches this precision. If <code>None</code>, titration stops after a certain number of questions.
</p>
<b>max_pages : <i>int or None, default=None</i></b>
<p class="attr">
    Titration will stop after this number of pages. If <code>None</code>, titration stops after a precision level is reached.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments are passed to the titration page constructor.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>FIrst titration page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

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
    # p_larger is the probability of winning the larger amount of money
    p = round(p_larger)
    return Binary(
        '''
        Which lottery would you rather have?
        ''',
        [
            '{}/100 of $2.00, {}/100 of $1.60'.format(p, 100-p),
            '{}/100 of $3.85, {}/100 of $0.10'.format(p, 100-p)
        ],
        inline=False, validate=V.require()
    )

@route('/survey')
def start():
    return Branch(
        titrate(gen_titrate_q, uniform(0, 100), var='p', tol=5, back=True),
        Page(
            Label(compile=disp_risk_aversion),
            back=True, terminal=True,
        )
    )

def disp_risk_aversion(label):
    def func(r):
        def u(x):
            # CRRA utility function
            return x**(1-r) if abs(1-r) > .01 else math.log(x)

        return (p*u(2)+(1-p)*u(1.6)-p*u(3.85)-(1-p)*u(.1))**2

    p = label.part.g['p'] / 100. # indifference point between 0 and 1
    # coefficient of relative risk aversion if optimization starts from -3
    res_lower = minimize(func, x0=np.array([-3])).x
    # coefficient of relative risk aversion if optimization starts from 2
    res_upper = minimize(func, x0=np.array([2])).x
    # you can trivially minimize the function by setting r == 1 (approximately)
    # this sets u(x) = 0 (approx.) for all x
    # so choose the r farther from 1
    r = res_lower if abs(res_lower-1)>abs(res_upper-1) else res_upper
    label.label = '''
        Indifference point is {:.0f}/100. Coefficient of relative risk aversion is {:.2f}
        '''.format(100.*p, float(r))
```