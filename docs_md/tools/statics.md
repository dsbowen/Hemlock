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
</style># Statics

Tool for embedding statics:

- css
- javascript
- images
- iframes
- YouTube videos
- links to Google bucket files

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**format_attrs**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>format_attrs</b>(<i>**attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L22">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i>dict</i></b>
<p class="attr">
    Maps HTML attribute name to value.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>attrs : <i>str</i></b>
<p class="attr">
    Formated attributes for insertion into HTML tag.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**external_css**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>external_css</b>(<i>href, rel='stylesheet', type='text/css', **attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L49">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;link/&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>css : <i>str</i></b>
<p class="attr">
    <code>&lt;link/&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import external_css

app = push_app_context()

p = Page(extra_css=external_css(href='https://my-css-url'))
p.css
```

Out:

```
...
<link href="https://my-css-url" rel="stylesheet" type="text/css"/>
```

##hemlock.tools.**internal_css**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>internal_css</b>(<i>style</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L84">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>style : <i>dict</i></b>
<p class="attr">
    Maps css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>css : <i>str</i></b>
<p class="attr">
    <code>&lt;style&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import internal_css

app = push_app_context()

p = Page(extra_css=internal_css({'body': {'background': 'coral'}}))
p.css
```

Out:

```
...
<style>
    body {background:coral;}
</style>
```

##hemlock.tools.**external_js**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>external_js</b>(<i>src, **attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L125">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    External javascript source.
</p>
<b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import external_js

app = push_app_context()

p = Page(extra_js=external_js(src='https://my-js-url'))
p.js
```

Out:

```
...
<script src="https://my-js-url"></script>
```

##hemlock.tools.**internal_js**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>internal_js</b>(<i>js, **attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L161">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    Javascript code.
</p>
<b>**attrs : <i>dict</i></b>
<p class="attr">
    Mapping of HTML attributes to values for the <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    Javascript code wrapped in <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import internal_js

app = push_app_context()

p = Page(
    extra_js=internal_js(
        '''
        $( document ).ready(function() {
            alert('hello, world!');
        });
        '''
    )
)
p.js
```

Out:

```
...
<script>
    $( document ).ready(function() {
        alert('hello, world!');
    });
</script>
```

##hemlock.tools.**src_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>src_from_bucket</b>(<i>filename</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L216">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>filename : <i>str</i></b>
<p class="attr">
    Name of the file in the Google bucket.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    <code>src</code> html attribute which references the specified file in the Google bucket.
</p></td>
</tr>
    </tbody>
</table>

####Examples

Set up a
[Google bucket](https://cloud.google.com/storage/docs/creating-buckets)
with the appropriate
[CORS permissions](https://cloud.google.com/storage/docs/cross-origin).

Set an environment variable `BUCKET` to the name of the bucket.

```
$ export BUCKET=<my-bucket>
```

Upload a file to the bucket, e.g. <https://xkcd.com/2138/> and name it
`wanna_see_the_code.png`.

```python
from hemlock import Branch, Page, Label, push_app_context
from hemlock.tools import Img, src_from_bucket

app = push_app_context()

img = Img(
    src=src_from_bucket('wanna_see_the_code.png'),
    align='center'
).render()
Page(Label(img)).preview()
```

##hemlock.tools.**url_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>url_from_bucket</b>(<i>filename, expiration=1800, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L262">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>filename : <i>str</i></b>
<p class="attr">
    Name of the file in the Google bucket.
</p>
<b>expiration : <i>float, default=1800</i></b>
<p class="attr">
    Number of seconds until the url expires.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments are passed to the [<code>generate_signed_url</code> method] (https://cloud.google.com/storage/docs/access-control/signed-urls).
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>signed_url : <i>str</i></b>
<p class="attr">
    Signed url for the file in the app's bucket.
</p></td>
</tr>
    </tbody>
</table>

####Examples

Set up a
[Google bucket](https://cloud.google.com/storage/docs/creating-buckets)
with the appropriate
[CORS permissions](https://cloud.google.com/storage/docs/cross-origin).

Set an environment variable `BUCKET` to the name of the bucket, and
`GOOGLE_APPLICATION_CREDENTIALS` to the name of your
[Google application credentials JSON file](https://cloud.google.com/docs/authentication/getting-started).

```
$ export BUCKET=<my-bucket> GOOGLE_APPLICATION_CREDENTIALS=<my-credentials.json>
```

In `survey.py`:

```python
from hemlock import Branch, Page, Download, route
from hemlock.tools import url_from_bucket

@route('/survey')
def start():
    filename = 'wanna_see_the_code.png'
    url = url_from_bucket(filename)
    return Branch(Page(Download(downloads=[(url, filename)])))
```

In `app.py`:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run the app locally with:

```
$ python app.py # or python3 app.py
```

And open your browser to <http://localhost:5000/>. Click on the
download button to download the file from your Google bucket.

##hemlock.tools.**img**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>img</b>(<i>src, caption='', img_align='left', caption_align='left', figure_class='figure w-100', figure_attrs={}, img_class= 'figure-img img-fluid rounded', img_attrs={}, caption_class= 'figure-caption', caption_attrs={}, template=os.path.join(DIR, 'img.html') </i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L337">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    Image source.
</p>
<b>caption : <i>str</i></b>
<p class="attr">
    
</p>
<b>img_align : <i>str, default='left'</i></b>
<p class="attr">
    
</p>
<b>caption_align : <i>str, default='left'</i></b>
<p class="attr">
    
</p>
<b>figure_class : <i>list or str, default='figure w-100'</i></b>
<p class="attr">
    Class for the <code>&lt;figure&gt;</code> tag.
</p>
<b>figure_attrs : <i>dict, default={}</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;figure&gt;</code> tag.
</p>
<b>img_class : <i>list or str, default='figure-img img-fluid rounded'</i></b>
<p class="attr">
    Class for the <code>&lt;img&gt;</code> tag.
</p>
<b>img_attrs : <i>dict, default={}</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;img&gt;</code> tag.
</p>
<b>caption_class : <i>list or str, default='figure-caption'</i></b>
<p class="attr">
    Class for the <code>&lt;figcaption&gt;</code> tag.
</p>
<b>caption_attrs : <i>dict, default={}</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;figcaption&gt;</code> tag.
</p>
<b>template : <i>str, default='directory/img.html'</i></b>
<p class="attr">
    Path to image template. Default is a template in the same directory as the current file. This may also be a string to be used directly as the template.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>img : <i>str</i></b>
<p class="attr">
    Image html.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import img

img(
    'https://imgs.xkcd.com/comics/wanna_see_the_code.png',
    img_align='center', caption='Wanna See The Code?'
)
```

Out:

```
<figure class="figure w-100 text-center">
    <img class="figure-img img-fluid rounded" src="https://imgs.xkcd.com/comics/wanna_see_the_code.png">
    <figcaption class="figure-caption text-left">Wanna See The Code?</figcaption>
</figure>
```

##hemlock.tools.**iframe**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>iframe</b>(<i>src, aspect_ratio=(16, 9), query_string={}, div_class= 'embed-responsive', div_attrs={}, iframe_class='embed-responsive-item', iframe_attrs={'allowfullscreen': True}, template=os.path.join(DIR, 'iframe.html')</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L419">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    Embed source.
</p>
<b>aspect_ratio : <i>tuple of (int, int), default=(16, 9)</i></b>
<p class="attr">
    Embed <a href="https://getbootstrap.com/docs/4.0/utilities/embed/#aspect-ratios">aspect ratio</a>.
</p>
<b>query_string : <i>dict</i></b>
<p class="attr">
    Mapping of URL query keys to values.
</p>
<b>div_class : <i>str or list, default='embed-responsive'</i></b>
<p class="attr">
    Class of the <code>&lt;div&gt;</code> which wraps the <code>&lt;iframe&gt;</code>.
</p>
<b>div_attrs : <i>dict, default={}</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;div&gt;</code> wrapper.
</p>
<b>iframe_class : <i>str or list, default='embed-responsive-item'</i></b>
<p class="attr">
    Class of the <code>&lt;iframe&gt;</code> tag.
</p>
<b>iframe_attrs : <i></i></b>
<p class="attr">
    HTML attributes for the <code>&lt;iframe&gt;</code> tag.
</p>
<b>template : <i>str, default='directory/iframe.html'</i></b>
<p class="attr">
    Path to iframe template. Default is a template in the same directory as the current file. This may also be a string to be used directly as the template.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>iframe : <i>str</i></b>
<p class="attr">
    Iframe HTML.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import iframe

iframe(
    'https://www.youtube.com/embed/zpOULjyy-n8?rel=0',
    aspect_ratio=(21, 9)
)
```

Out:

```
<div class="embed-responsive embed-responsive-21by9">
    <iframe allowfullscreen class="embed-responsive-item" src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0"></iframe>
</div>
```

##hemlock.tools.**youtube**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>youtube</b>(<i>src, iframe_attrs={'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;', 'allowfullscreen': True}, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L493">[source]</a>
</p>

Embed a youtube video.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    Link to youtube video. e.g. <a href="https://www.youtube.com/watch?v=ts3s738ZkcQ">https://www.youtube.com/watch?v=ts3s738ZkcQ</a>.
</p>
<b>iframe_attrs : <i>dict</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;iframe&gt;</code> tag.
</p>
<b>*args, **kwarg : <i></i></b>
<p class="attr">
    Arguments and keyword arguments are passed to <code>hemlock.tools.iframe</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>iframe : <i>str</i></b>
<p class="attr">
    Iframe HTML.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import youtube

youtube(
    'https://www.youtube.com/watch?v=ts3s738ZkcQ',
    query_string={'autoplay': 1}
)
```

Out:

```
<div class="embed-responsive embed-responsive-16by9">
    <iframe allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;" allowfullscreen class="embed-responsive-item" src="https://www.youtube.com/embed/ts3s738ZkcQ?autoplay=1"></iframe>
</div>
```