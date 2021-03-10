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
</style># Input

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Input**

<p class="func-header">
    <i>class</i> hemlock.<b>Input</b>(<i>label=None, template='hemlock/input.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/input.py#L13">[source]</a>
</p>

Inputs take text input by default, or other types of html inputs.

Inherits from [hemlock.models.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Input label.
</p>
<b>template : <i>str, default='hemlock/input.html'</i></b>
<p class="attr">
    Template for the input body.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Page, push_app_context

app = push_app_context()

Page(Input('Input text here.')).preview()
```

