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
</style># Range slider

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Range**

<p class="func-header">
    <i>class</i> hemlock.<b>Range</b>(<i>label=None, template='hemlock/range.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L18">[source]</a>
</p>

Range sliders can be dragged between minimum and maximum values in step
increments.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/range.html'</i></b>
<p class="attr">
    Template for the range body.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Ranges have a default javascript which displays the value of the range
slider to participants. This will be appended to any `js` and `extra_js`
arguments passed to the constructor.

####Examples

```python
from hemlock import Range, Page, push_app_context

app = push_app_context()

Page(Range('<p>This is a range slider.</p>')).preview()
```



##hemlock.**RangeInput**

<p class="func-header">
    <i>class</i> hemlock.<b>RangeInput</b>(<i>label=None, template='hemlock/rangeinput.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L66">[source]</a>
</p>

Range slider with an input field.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/rangeinput.html'</i></b>
<p class="attr">
    Template for the range body.
</p>
<b>width : <i>str, default='5em'</i></b>
<p class="attr">
    Width of the input field.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Ranges have a default javascript which displays the value of the range
slider to participants. This will be appended to any `js` and `extra_js`
arguments passed to the constructor.

####Examples

```python
from hemlock import RangeInput, Page, push_app_context

app = push_app_context()

Page(RangeInput('<p>This is a range slider.</p>')).preview()
```

