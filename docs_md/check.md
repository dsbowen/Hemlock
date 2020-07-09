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



##hemlock.**click_choices**

<p class="func-header">
    <i>def</i> hemlock.<b>click_choices</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/check.py#L6">[source]</a>
</p>

Default debug function. See
[`hemlock.functions.debug.click_choices`](debug_functions.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Check**

<p class="func-header">
    <i>class</i> hemlock.<b>Check</b>(<i>label='', choices=[], template='hemlock/check.html', ** kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/check.py#L22">[source]</a>
</p>

Check questions use radio inputs if only one choice can be selected, or
checkbox inputs if multiple choices can be selected.

Inherits from [`hemlock.ChoiceQuestion`](question.md).

By default, choices are positioned vertically. To position them
horizontally, set `inline` to True.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Check question label.
</p>
<b>choices : <i>list of hemlock.Choice or str, default=[]</i></b>
<p class="attr">
    Choices which participants can check. String inputs are automatically converted to <code>hemlock.Choice</code> objects.
</p>
<b>template : <i>str, default='hemlock/check.html'</i></b>
<p class="attr">
    Template for the check body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>align : <i>str, default='left'</i></b>
<p class="attr">
    Choice alignment; <code>'left'</code>, <code>'center'</code>, or <code>'right'</code>.
</p>
<b>choice_wrapper : <i>bs4.Tag</i></b>
<p class="attr">
    Tag fo the choice html wrapper.
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

####Examples

```python
from hemlock import Check, Page, push_app_context

push_app_context()

Page(Check('<p>Check one.</p>', ['Yes','No','Maybe'])).preview()
```

