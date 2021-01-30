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
</style># Blank

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Blank**

<p class="func-header">
    <i>class</i> hemlock.<b>Blank</b>(<i>label=None, template='hemlock/input.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/blank.py#L16">[source]</a>
</p>

Fill in the blank question.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>tuple, list, or None, default=None</i></b>
<p class="attr">
    If the label is a <code>tuple</code> or <code>list</code>, the participant's response will fill in the blanks between items.
</p>
<b>template : <i>str, default='hemlock/input.html'</i></b>
<p class="attr">
    File name of the Jinja template.
</p>
<b>blank_empty : <i>str, default=''</i></b>
<p class="attr">
    String used to fill in the blank when the participant's response is empty.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Blank

Page(
    Blank(
        ('Hello, ', '!'),
        blank_empty='_____'
    )
).preview()
```

Enter 'World' in the input and the label will change to 'Hello, World!'.

