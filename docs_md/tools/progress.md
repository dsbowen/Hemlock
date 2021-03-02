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
</style>##hemlock.tools.**progress**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>progress</b>(<i>width, text=None, progress_attrs={'class': ['progress', 'position-relative'], 'style': {'height': '25px', 'background-color': 'rgb(200,200,200)', 'box-shadow': '0 1px 2px rgba(0,0,0,0.25) inset'}}, bar_attrs={'class': ['progress-bar'], 'role': 'progressbar'}, text_attrs={'class': ['justify-content-center', 'd-flex', 'position-absolute', 'w-100', 'align-items-center']}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/progress.py#L5">[source]</a>
</p>

Creates a progress bar.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>width : <i>float between 0 and 1</i></b>
<p class="attr">
    Percent complete.
</p>
<b>text : <i>str, default=None</i></b>
<p class="attr">
    Progress text report. If <code>None</code>, the text will be the percent complete.
</p>
<b>additional parameters : <i></i></b>
<p class="attr">
    Additional parameters specify attributes for the progress bar containers.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>progress bar HTML : <i>str</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Label, push_app_context
from hemlock.tools import progress

app = push_app_context()

Page(
    Label(
        progress(0.5, "Halfway there!")
    )
).preview()
```