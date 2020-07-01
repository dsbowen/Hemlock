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
</style># Label

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Label**

<p class="func-header">
    <i>class</i> hemlock.<b>Label</b>(<i>page=None, template='hemlock/form-group.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/label.py#L6">[source]</a>
</p>

This question contains a label and does not receive input from the
participant.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Page to which this label belongs.
</p>
<b>template : <i>str, default='hemlock/form-group.html'</i></b>
<p class="attr">
    Path to the Jinja template for the label body.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Label, push_app_context

push_app_context()

p = Page()
Label(p, label='<p>Lorem ipsum.</p>')
p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```
