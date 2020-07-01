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
</style># Comprehension check

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**comprehension_check**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>comprehension_check</b>(<i>branch, instructions=[], checks=[], attempts=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/comprehension.py#L8">[source]</a>
</p>

Add a comprehension check to a branch.

A comprehension check consists of 'instruction' pages followed by 'check' pages. The data of all questions in a check page must evaluate to `True` to pass the check. When a participant fails a check, he is brought back to the first instructions page.

Participants only have to pass each check once. For example, suppose there are two checks, 0 and 1. A participant passes check 0 but fails check 1. He is brought back to the first page of the instructions. After rereading the instructions, he is brought directly to check 1, skipping check 0.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch</i></b>
<p class="attr">
    Branch to which the comprehension check is attached.
</p>
<b>instructions : <i>hemlock.Page or list of hemlock.Page</i></b>
<p class="attr">
    Instruction page(s).
</p>
<b>checks : <i>hemlock.Page or list of hemlock.Page</i></b>
<p class="attr">
    Check page(s).
</p>
<b>attempts : <i>int or None, default=None</i></b>
<p class="attr">
    Number of attempts allotted. Participants are allowed to proceed with the survey after exceeding the maximum number of attempts. If <code>None</code>, participants must pass the comprehension check before continuing the survey.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch</i></b>
<p class="attr">
    The original branch, with added comprehension check.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This function adds a `hemlock.Submit` function to each check page. This must be the last submit function of each check page.