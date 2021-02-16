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
</style># MTurk utilities

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**consent_page**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>consent_page</b>(<i>consent_label=None, id_label=ID_LABEL, confirm_label= CONFIRM_LABEL, require=True</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/mturk.py#L12">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>consent_label : <i>str or None, default=None</i></b>
<p class="attr">
    The consent terms for your study. If <code>None</code>, the consent label is omitted.
</p>
<b>id_label : <i>str, default='Enter your MTurk ID to consent'</i></b>
<p class="attr">
    Label asking workers to enter their ID.
</p>
<b>confirm_label : <i>str, default='Confirm your ID'</i></b>
<p class="attr">
    Label asking for confirmation.
</p>
<b>require : <i>bool, default=True</i></b>
<p class="attr">
    Indicates that workers are required to enter their ID.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>consent page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**completion_page**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>completion_page</b>(<i>participant=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/mturk.py#L65">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>participant : <i>hemlock.Participant or None, default=None</i></b>
<p class="attr">
    Record the completion code in this participant's metadata. If <code>None</code>, the completion code is recorded in flask-login's <code>current_user</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>completion page : <i>hemlock.Page</i></b>
<p class="attr">
    Completion page with unique completion code.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**get_approve_df**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>get_approve_df</b>(<i>data_df, batch_df, bonus=False, verbose=True</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/mturk.py#L96">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>data_df : <i>str or pd.DataFrame</i></b>
<p class="attr">
    Hemlock survey data. This must have <code>'WorkerId'</code> and <code>'SurveyCode'</code> columns.
</p>
<b>bonus : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that workers will receive a bonus. If bonusing workers, <code>data_df`` must include a column called</code>'BonusAmount'`.
</p>
<b>verbose : <i>bool, default=True</i></b>
<p class="attr">
    Indicates to print information on approvals, rejections, and bonuses.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>approve_df : <i>pd.DataFrame</i></b>
<p class="attr">
    Dataframe with approval and bonus information.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import get_approve_df, approve_assignments

approve_df = get_approve_df(data_df, 'path/to/batch.csv', bonus=True)
```

Out:

```
90 assignments approved
10 assignments rejected
Total bonus: $90
```

```python
import boto3

client = boto3.client('mturk')
approve_assignments(client, approve_df, bonus=True, reason='Great job!')
```

##hemlock.tools.**approve_assignments**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>approve_assignments</b>(<i>client, approve_df, approve=True, bonus=False, bonus_reason='', OverrideRejection=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/mturk.py#L159">[source]</a>
</p>

Approve and reject assignments and pay bonuses.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>client : <i>boto3.client</i></b>
<p class="attr">
    
</p>
<b>approve_df : <i>pd.DataFrame</i></b>
<p class="attr">
    Output of <code>get_approve_df</code>.
</p>
<b>approve : <i>bool, default=True</i></b>
<p class="attr">
    Indicates that assignments should be approved and rejected.
</p>
<b>bonus : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that bonuses should be paid.
</p>
<b>bonus_reason : <i>str, default=''</i></b>
<p class="attr">
    Reason for giving bonuses. This must be nonempty if paying bonuses.
</p>
<b>OverrideRejection : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that this function can override rejected assignments.
</p></td>
</tr>
    </tbody>
</table>

