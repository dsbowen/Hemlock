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
</style># Check

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**binary**

<p class="func-header">
    <i>def</i> hemlock.<b>binary</b>(<i>label=None, choices=['Yes', 'No'], inline=True, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/check.py#L9">[source]</a>
</p>

Creates a binary (yes/no) check question.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=None</i></b>
<p class="attr">
    
</p>
<b>choices : <i>list, default=['Yes', 'No']</i></b>
<p class="attr">
    List of choice labels.
</p>
<b>inline : <i>bool, default=True</i></b>
<p class="attr">
    Indicates that choices should be displayed inline.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments passed to <code>Check</code> constructor.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, binary, push_app_context

app = push_app_context()

Page(binary('Yes or no?')).preview()
```

##hemlock.**Binary**

<p class="func-header">
    <i>def</i> hemlock.<b>Binary</b>(<i>*args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/check.py#L41">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Check**

<p class="func-header">
    <i>class</i> hemlock.<b>Check</b>(<i>label=None, choices=[], template='hemlock/check.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/check.py#L52">[source]</a>
</p>

Check questions use radio inputs if only one choice can be selected, or
checkbox inputs if multiple choices can be selected.

Inherits from [`hemlock.qpolymorphs.base.InputBase`](bases.md) and [`hemlock.models.ChoiceQuestion`](../models/question.md).

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
    Check question label.
</p>
<b>choices : <i>list of hemlock.Choice, str, tuple, or dict, default=[]</i></b>
<p class="attr">
    Choices which participants can check.
</p>
<b>template : <i>str, default='hemlock/check.html'</i></b>
<p class="attr">
    File name of the Jinja template.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>align : <i>str, default='left'</i></b>
<p class="attr">
    Alignment of the choice text. Value can be <code>'left'</code>, <code>'center'</code>, or <code>'right'</code>.
</p>
<b>choices : <i>list of <code>hemlock.Choice</code></i></b>
<p class="attr">
    Set from the <code>choices</code> parameter.
</p>
<b>inline : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that choices should be <a href="https://getbootstrap.com/docs/4.0/components/forms/#inline">inline</a>, as opposed to vertical.
</p>
<b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant may select multiple choices.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A choice can be input as any of the following:

1. `Choice` object.
2. `str`, treated as the choice label, value, and name.
3. `(choice label, value)` tuple.
4. `(choice label, value, name)` tuple.
5. Dictionary with choice keyword arguments.

####Examples

```python
from hemlock import Check, Page, push_app_context

app = push_app_context()

Page(Check('<p>Check one.</p>', ['Yes','No','Maybe'])).preview()
```

