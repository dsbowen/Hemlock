# Mac setup

These instructions were written for Mac OS 10.9.

!!! tip
    About 50% of the problems you encounter during setup can be fixed by closing and re-opening your terminal window. If you have any problems, this is the first thing to try.

## Open a terminal window

Hemlock requires you to use a terminal window for setting up, editing, and deploying hemlock projects. To open a terminal window, enter 'terminal' in spotlight search. Terminal commands are written in bash:

```bash
$ <my-bash-command>
```

!!! tip
    1. You don't type `$`. This just indicates the beginning of a bash command.
    2. For the tutorial, always change to your home directory after you open your terminal. Do this by entering:
    
    ```bash
    $ cd
    ```

## Xcode

Mac OS typically requires Xcode Command-line Tools. Install in your terminal:

```bash
$ xcode-select --install
```

Or from the <a href="https://apps.apple.com/us/app/xcode/id497799835" target="_blank">Mac app store</a>.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI.

**Read everything until STOP before downloading or installing anything.**

You can <a href="https://www.python.org/downloads/" target="_blank">download python here</a>. If possible, download python3.6.

Why do I recommend 3.6 instead of the latest version of python? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues. Anecdotally, I've found downloading legacy version of python is a pain, so if you're having trouble, just download the latest python and make a mental note to double check that your survey works when you deploy it.

**When you start the python installer, you may see an *Add Python to PATH* option on the first page. Make sure to select this option.**

**STOP.**

Close and re-open your terminal window. Verify your python installation.

```bash
$ python3 --version
Python 3.6.8
```

Upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip xx.x.x ...
```

!!! tip "pip versus pip3"
    You'll install several python packages using `pip`. Conventionally, the command to install these is written as:

    ```bash
    $ pip install <my-requested-package>
    ```

    You may need to repace this with:

    ```bash
    $ pip3 install <my-requested-package>
    ```

    Or even:

    ```bash
    $ python3 -m pip install <my-requested-package>
    ```

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Install with:

```bash
$ pip install -U hemlock-cli
```

Verify your hemlock-CLI installation:

```bash
$ hlk --version
hlk, version x.x.xx
```

## Git and github

<a href="https://git-scm.com/" target="_blank">Git</a> is a version control system, and <a href="https://github.com/" target="_blank">github</a> hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

Macs typically have git pre-installed, which you can verify:

```bash
$ git --version
git version x.xx.x
```

If you don't have git, follow the [download and installation instructions here](https://git-scm.com/download/mac).

Then, create a [github account here](https://github.com). Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github-user-email>
```

For example, I would enter:

```bash
$ git config --global user.name dsbowen
$ git config --global user.email dsbowen@wharton.upenn.edu
```

**Read everything until STOP before creating your github token.**

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface.

1. Create a github token by following <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token" target="_blank">these instructions</a>.
2. When setting permissions (step 7), check 'repo'.
3. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

**STOP.**

## Visual studio code

I recommend visual studio code for editing python files. <a href="https://code.visualstudio.com/" target="_blank">Download VS code here</a>

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.xx.x
```

??? error "code: command not found"
    If you experience a "command not found" error, it's probably because VS code isn't in your `PATH`. Try this: 

    1. Open the VS code application and press `Command` + `Shift` + `P` or `F1`.
    2. Type `shell` in command palette. You should see an option like `shell command : Install code in PATH`. Click that.
    3. Close and re-open your terminal and verify your installation.

    <a href="https://stackoverflow.com/questions/29955500/code-not-working-in-command-line-for-visual-studio-code-on-osx-mac" target="_blank">See here for more details.</a>.

## Jupyter

<a href="https://jupyter.org/" target="_blank">Jupyter</a> allows you to quickly iterate on project designs. Install jupyter notebook with pip:

```bash
$ pip install -U notebook
```

Close and re-open your terminal. Verify your jupyter installation:

```bash
$ jupyter --version
jupyter core     : 4.6.3
jupyter-notebook : 6.0.3
qtconsole        : not installed
ipython          : 7.16.1
ipykernel        : 5.3.2
jupyter client   : 6.1.5
jupyter lab      : not installed
nbconvert        : 5.6.1
ipywidgets       : not installed
nbformat         : 5.0.7
traitlets        : 4.3.3
```

## Google chrome

Hemlock is developed and tested primarily on chrome. <a href="https://www.google.com/chrome/" target="_blank">Download chrome here</a>.

Verify that you can open it as follows:

```
$ python3 -m webbrowser https://dsbowen.github.io
```

You should see chrome open to my github.io page.

If you came here from the tutorial, you're now ready to return to it and get started with your first hemlock project. [Click here to go back to the First Project section of the tutorial](../tutorial/first_project.md).

## Chromedriver

Hemlock's custom debugging tool and survey view functions use <a href="https://chromedriver.chromium.org/downloads" target="_blank">chromedriver</a>. To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup mac --chromedriver
```

This will ask you to copy the chromedriver Mac download URL from <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a> and paste it in your terminal window.

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ chromedriver --version
ChromeDriver x.xx.x
```

!!! warning "Chrome and chromedriver compatibility"
    Google chrome will automatically update. Chromedriver will not. If you encounter a compatibility error in the future, simply repeat the above instructions.

If you came here from the Debug section of the tutorial, you're now ready to return to it and run the debugger. [Click here to go back to the Debug section of the tutorial](../tutorial/debug.md).

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e. putting them online), including hemlock applications. <a href="https://signup.heroku.com/" target="_blank">Sign up for heroku here</a>.

You can install heroku-CLI using hemlock-CLI:

```bash
$ hlk setup mac --heroku-cli
```

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x mac node-vxx.xx.x
```

??? error "EACCES error"
    See <a href="https://github.com/heroku/legacy-cli/issues/1969" target="_blank">this github issue</a> if you experience a 'EACCES' error. *Do not* simply use `sudo`; this only masks issues you'll encounter later.

[Click here to return to the Deploy section of the tutorial](../tutorial/deploy.md).