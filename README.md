# Hemlock

Hemlock aspires to be the most powerful and flexible way to create online studies, with applications in marketing and behavioral science research.

If you're new to python, or the installation and quickstart instructions don't make sense to you, check out the [tutorial](https://dsbowen.github.io/hemlock/tutorial/intro/).

## Installation

```bash
$ pip install hemlock-survey
```

## Quickstart

Create a file `app.py` in the root directory of your project:

```python
import eventlet
eventlet.monkey_patch()

from hemlock import Branch, Page, Label, create_app, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Hello, World!'),
            terminal=True
        )
    )

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run your app:

```bash
$ python3 app.py
```

And navigate to <http://localhost:5000/> in your browser.

## Citation

```
@software{bowen2021hemlock,
  author = {Dillon Bowen},
  title = {Hemlock},
  url = {https://dsbowen.github.io/hemlock/},
  date = {2021-02-13},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the [Hemlock Research License](https://github.com/dsbowen/hemlock/blob/master/LICENSE). The license permits free use for academic research, and requires written permission from hemlock's author, Dillon Bowen, for commercial use.