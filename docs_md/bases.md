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
</style># Common bases and mixins

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Base**

<p class="func-header">
    <i>class</i> hemlock.<b>Base</b>(<i>**kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L19">[source]</a>
</p>

Base for all Hemlock models.

Interits from
[`sqlalchemy_orderingitem.Orderingitem`](https://dsbowen.github.io/sqlalchemy-orderingitem/) and
[`sqlalchemy_modelid.ModelIdBase`](https://dsbowen.github.io/sqlalchemy-modelid/).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**kwargs : <i></i></b>
<p class="attr">
    You can set any attribute by passing it as a keyword argument.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>name : <i>str or None, default=None</i></b>
<p class="attr">
    Used primarily as a filter for database querying.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Data**



Polymorphic base for all objects which contribute data to the dataframe.

Data elements 'pack' their data and return it to their participant, who in turn sends it to the data store.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>data : <i>sqlalchemy_mutable.MutableType, default=None</i></b>
<p class="attr">
    Data this element contributes to the dataframe.
</p>
<b>data_rows : <i>int, default=1</i></b>
<p class="attr">
    Number of rows this data element contributes to the dataframe for its participant. If negative, this data element will 'fill in' any emtpy rows at the end of the dataframe with its most recent value.
</p>
<b>index : <i>int or None, default=None</i></b>
<p class="attr">
    Order in which this data element appears in its parent; usually a <code>hemlock.Branch</code>, <code>hemlock.Page</code>, or <code>hemlock.Question</code>.
</p>
<b>var : <i>str or None, default=None</i></b>
<p class="attr">
    Variable name associated with this data element. If <code>None</code>, the data will not be recorded.
</p>
<b>record_order : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the order of this data element should be recorded in the datafame. The order is the order in which this element appeared relative to other elements with the same variable name.
</p>
<b>record_index : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the index of this data element should be recorded in the dataframe. The index is the order in which this element appeared relative to other elements with the same parent. For example, the index of a question is the order in which the question appeared on its page.
</p>
<b>record_choice_index : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the index of this data element's choices should be recorded in the dataframe. For example, a <code>hemlock.Check</code> question has multiple choices that the participant can select. The index of a choice is its index in the question's choice list.
</p></td>
</tr>
    </tbody>
</table>



