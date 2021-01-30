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
</style># Select (dropdown)

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Select**

<p class="func-header">
    <i>class</i> hemlock.<b>Select</b>(<i>label=None, choices=[], template='hemlock/select.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/select.py#L17">[source]</a>
</p>

Select questions allow participants to select one or more options from a
dropdown menu.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.ChoiceQuestion`](../models/question.md).

Its default debug function is
[`click_choices`](../functions/debug.md#hemlockfunctionsdebugclick_choices).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Select question label.
</p>
<b>choices : <i>list of hemlock.Option, str, tuple, or dict, default=[]</i></b>
<p class="attr">
    Options the participant can select.
</p>
<b>template : <i>str, default='hemlock/select.html'</i></b>
<p class="attr">
    Template for the select body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>align : <i>str, default='left'</i></b>
<p class="attr">
    Choice alignment; <code>'left'</code>, <code>'center'</code>, or <code>'right'</code>.
</p>
<b>choices : <i>list of <code>hemlock.Option</code></i></b>
<p class="attr">
    Set for the <code>choices</code> parameter.
</p>
<b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant may select multiple choices.
</p></td>
</tr>
    </tbody>
</table>

####Notes

An option can be input as any of the following:

1. `Option` object.
2. `str`, treated as the choice label.
3. `(choice label, value)` tuple.
4. `(choice label, value, name)` tuple.
5. Dictionary with choice keyword arguments.

####Examples

```python
from hemlock import Page, Select, Option, push_app_context

app = push_app_context()

Page(Select('<p>Select one.</p>', ['World','Moon','Star'])).preview()
```

