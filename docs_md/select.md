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



##hemlock.**click_choices**

<p class="func-header">
    <i>def</i> hemlock.<b>click_choices</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/select.py#L7">[source]</a>
</p>

Default select debug function. See [click choices](debug_functions.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Select**

<p class="func-header">
    <i>class</i> hemlock.<b>Select</b>(<i>page=None, template='hemlock/select.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/select.py#L23">[source]</a>
</p>

Select questions allow participants to select one or more options from a
dropdown menu.

Inherits from [`hemlock.InputGroup`](input_group.md) and
[`hemlock.ChoiceQuestion`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Page to which this question belongs.
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
<b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant may select multiple choices.
</p>
<b>select : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;select&gt;</code> tag.
</p>
<b>size : <i>int or None, default=None</i></b>
<p class="attr">
    Number of rows of choices to display.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Select, Option, push_app_context

push_app_context()

p = Page()
s = Select(p, label='<p>This is a select question.</p>')
s.choices = ['World', 'Moon', 'Star']
p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```
