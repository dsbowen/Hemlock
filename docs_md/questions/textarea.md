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
</style># Textarea

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Textarea**

<p class="func-header">
    <i>class</i> hemlock.<b>Textarea</b>(<i>label=None, template='hemlock/textarea.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/textarea.py#L13">[source]</a>
</p>

Textareas provide large text boxes for free responses.

Inherits from [`hemlock.qpolymorphs.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=None</i></b>
<p class="attr">
    Textarea label.
</p>
<b>template : <i>str, default='hemlock/textarea.html'</i></b>
<p class="attr">
    Template for the textarea body.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Textareas have a default javascript which displays the character and word
count to participants. This will be appended to any `js` and `extra_js`
arguments passed to the constructor.

####Examples

```python
from hemlock import Page, Textarea, push_app_context

app = push_app_context()

Page(Textarea('This is a textarea.')).preview()
```

