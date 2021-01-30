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
</style># Questions

`hemlock.Question` and `hemlock.ChoiceQuestion` are 'question skeletons';
most useful when fleshed out. See section on question polymorphs.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Question**

<p class="func-header">
    <i>class</i> hemlock.<b>Question</b>(<i>label=None, extra_css=[], extra_js=[], form_group_class= ['card', 'form-group', 'question'], form_group_attrs={}, error_attrs={ 'class': ['alert', 'alert-danger']}, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L25">[source]</a>
</p>

Base object for questions. Questions are displayed on their page in index
order.

It inherits from
[`hemlock.models.Data`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Question label.
</p>
<b>template : <i>str, default='form-group.html'</i></b>
<p class="attr">
    File name of question template.
</p>
<b>extra_css : <i>list, default=[]</i></b>
<p class="attr">
    List of extra CSS elements to add to the default CSS.
</p>
<b>extra_js : <i>list, default=[]</i></b>
<p class="attr">
    List of extra javascript elements to add to the default javascript.
</p>
<b>form_group_class : <i>list, default=['card', 'form-group', 'question']</i></b>
<p class="attr">
    List of form group classes.
</p>
<b>form_group_attrs : <i>dict, default={}</i></b>
<p class="attr">
    Dictionary of HTML attribues for the form group tag.
</p>
<b>error_attrs : <i>dict, default={'class' ['alert', 'alert-danger']}</i></b>
<p class="attr">
    Dictionary of HTML attributes for the error alert.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>append : <i>str or None, default=None</i></b>
<p class="attr">
    Text (usually) appended to the input tag.
</p>
<b>css : <i>list, default=[]</i></b>
<p class="attr">
    List of CSS elements.
</p>
<b>default : <i>misc</i></b>
<p class="attr">
    Default question response.
</p>
<b>error : <i>str or None, default=None</i></b>
<p class="attr">
    Error message.
</p>
<b>error_attrs : <i>dict</i></b>
<p class="attr">
    Set from the <code>error_attrs</code> parameter.
</p>
<b>form_group_class : <i>list</i></b>
<p class="attr">
    Set from the <code>form_group_class</code> parameter.
</p>
<b>form_group_attrs : <i>dict</i></b>
<p class="attr">
    Set from the <code>form_group_attrs</code> parameter.
</p>
<b>has_responded : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant has responded to this question.
</p>
<b>input_attrs : <i>dict</i></b>
<p class="attr">
    Dictionary of HTML attributes for the input tag.
</p>
<b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Question label.
</p>
<b>prepend : <i>str or None, default=None</i></b>
<p class="attr">
    Text (usually) prepended to the input tag.
</p>
<b>response : <i>misc</i></b>
<p class="attr">
    Participant's response.
</p>
<b>template : <i>str</i></b>
<p class="attr">
    Set from the <code>template</code> parameter.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant or None</i></b>
<p class="attr">
    The participant to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>branch : <i>hemlock.Branch or None</i></b>
<p class="attr">
    The branch to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    The page to which this question belongs.
</p>
<b>compile : <i>list of hemlock.Compile, default=[]</i></b>
<p class="attr">
    List of compile functions; run before the question is rendered.
</p>
<b>validate : <i>list of hemlock.Validate, default=[]</i></b>
<p class="attr">
    List of validate functions; run to validate the participant's response.
</p>
<b>submit : <i>list of hemlock.Submit, default=[]</i></b>
<p class="attr">
    List of submit functions; run after the participant's responses have been validated for all questions on a page.
</p>
<b>debug : <i>list of hemlock.Debug, default=[]</i></b>
<p class="attr">
    List of debug functions; run during debugging. The default debug function is unique to the question type.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A CSS element can be any of the following:

1. Link tag (str) e.g., `'<link rel="stylesheet" href="https://my-css-url">'`
2. Href (str) e.g., `"https://my-css-url"`
3. Style dictionary (dict) e.g., `{'body': {'background': 'coral'}}`

The style dictionary maps a css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.

A Javascript element can be any of the following:

1. Attributes dictionary (dict) e.g., `{'src': 'https://my-js-url'}`
2. JS code (str)
3. Tuple of (attributes dictionary, js code)

####Methods



<p class="func-header">
    <i></i> <b>clear_error</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L208">[source]</a>
</p>

Clear the error message.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Question</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>clear_response</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L219">[source]</a>
</p>

Clear the response.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Question</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**ChoiceQuestion**

<p class="func-header">
    <i>class</i> hemlock.<b>ChoiceQuestion</b>(<i>label=None, choices=[], template=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L277">[source]</a>
</p>

A question which contains choices. Inherits from `hemlock.Question`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Question label.
</p>
<b>choices : <i>list, default=[]</i></b>
<p class="attr">
    Choices which belong to this question. List items are usually <code>hemlock.Choice</code> or <code>hemlock.Option</code>.
</p>
<b>template : <i>str or None, default=None</i></b>
<p class="attr">
    Template for the question body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>choices : <i>list, default=[]</i></b>
<p class="attr">
    Set from <code>choices</code> parameter.
</p>
<b>choice_cls : <i>class, default=hemlock.Choice</i></b>
<p class="attr">
    Class of the choices in the <code>choices</code> list.
</p>
<b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant can select multiple choices.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A choice can be any of the following:

1. Choice objects (type will depend on the choice question).
2. `str`, treated as the choice label.
3. `(choice label, value)` tuple.
4. `(choice label, value, name)` tuple.
5. Dictionary with choice keyword arguments.

