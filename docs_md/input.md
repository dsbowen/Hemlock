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



##hemlock.**debug_func**

<p class="func-header">
    <i>def</i> hemlock.<b>debug_func</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/input.py#L17">[source]</a>
</p>

Default debug function for input questions. This function sends a random
string or number if the input takes text, or a random `datetime.datetime`
object if the input takes dates or times.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.Input</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Input**

<p class="func-header">
    <i>class</i> hemlock.<b>Input</b>(<i>page=None, template='hemlock/input.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/input.py#L41">[source]</a>
</p>

Inputs take text input by default, or other types of html inputs.

Inherits from [`hemlock.InputGroup`](input_group.md), [`hemlock.InputBase`](bases.md) and [`hemlock.Question`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Page to which this input belongs.
</p>
<b>template : <i>str, default='hemlock/input.html'</i></b>
<p class="attr">
    Template for the input body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>input_type : <i>str, default='text'</i></b>
<p class="attr">
    Type of html input. See <a href="https://www.w3schools.com/html/html_form_input_types.asp">https://www.w3schools.com/html/html_form_input_types.asp</a>.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Input, push_app_context

push_app_context()

p = Page()
Input(p, label='<p>This is an input.</p>')
p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```
