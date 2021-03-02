from .statics import format_attrs

from flask import render_template

def progress(
    width, text=None,
    progress_attrs={
        'class': ['progress', 'position-relative'],
        'style': {
            'height': '25px',
            'background-color': 'rgb(200,200,200)',
            'box-shadow': '0 1px 2px rgba(0,0,0,0.25) inset'
        }
    },
    bar_attrs={
        'class': ['progress-bar'],
        'role': 'progressbar'
    },
    text_attrs={
        'class': [
            'justify-content-center',
            'd-flex',
            'position-absolute',
            'w-100',
            'align-items-center'
        ]
    }
):
    """
    Creates a progress bar.
    
    Parameters
    ----------
    width : float between 0 and 1
        Percent complete.

    text : str, default=None
        Progress text report. If `None`, the text will be the percent 
        complete.

    additional parameters :
        Additional parameters specify attributes for the progress bar 
        containers.

    Returns
    -------
    progress bar HTML : str

    Examples
    --------
    ```python
    from hemlock import Page, Label, push_app_context
    from hemlock.tools import progress

    app = push_app_context()

    Page(
    \    Label(
    \        progress(0.5, "Halfway there!")
    \    )
    ).preview()
    ```
    """
    width = '{:.0f}%'.format(100*width)
    if 'style' not in bar_attrs:
        bar_attrs['style'] = {}
    bar_attrs['style']['width'] = width
    if text is None:
        text = width
    return render_template(
        'hemlock/progress.html',
        progress_attrs=format_attrs(**progress_attrs),
        bar_attrs=format_attrs(**bar_attrs),
        text_attrs=format_attrs(**text_attrs),
        text=text
    )