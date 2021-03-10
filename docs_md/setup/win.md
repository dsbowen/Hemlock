# Windows setup

These instructions were written for Windows 10.

!!! tip
    About 50% of the problems you encounter during setup can be fixed by closing and re-opening your terminal window. If you have any problems, this is the first thing to try.

## Git and github

<a href="https://git-scm.com/" target="_blank">Git</a> is a version control system, and <a href="https://github.com/" target="_blank">github</a> hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

You can find <a href="https://git-scm.com/download/win">git download and installation instructions here</a>.

We'll use the git bash terminal for this tutorial. Right click anywhere on your desktop and select 'Git Bash Here`. You should see a terminal window appear. Enter the following into your terminal:

```bash
$ cd
```

This moves you to your home directory. It's not important that you understand exactly what this means, but if you're dying to find out, <a href="https://towardsdatascience.com/basics-of-bash-for-beginners-92e53a4c117a" target="_blank">read this</a>.

!!! tip
    1. You don't type `$`. This just indicates the beginning of a bash command.
    2. For the tutorial, always change to your home directory after you open your terminal. Do this by entering:
    
    ```bash
    $ cd
    ```

Verify your git installation:

```bash
$ git --version
git version 2.27.0.windows.1
```

!!! tip
    `git --version` is the command you enter in your terminal. The line underneath it ('git version...') is the output.

Then, create a <a href="https://github.com" target="_blank">github account here</a>. Configure your github command line interface:

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

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface (more on this later).

1. Create a github token by following <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token" target="_blank">these instructions</a>.
2. When setting permissions (step 7), check 'repo'.
3. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

**STOP.**

## Python3 and pip3

**Read everything before STOP before downloading python.**

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI. Download the latest version of python <a href="https://www.python.org/downloads/" target="_blank">here</a>.

**When you start the python installer, you may see an *Add Python to PATH* option on the first page. Make sure to select this option.**

**STOP.**

Close and re-open your terminal window and enter:

```bash
$ which python
```

You should see a line print underneath `which python`. This is the location of your python executable (i.e., the file that runs python). On my computer, it looks like:

```bash
/c/Users/DBSpe/AppData/Local/Programs/Python/Python36-32/python
```

The python executable may be in a different location on your computer. In general, it'll look like:

```bash
<my-python-location>/python
```

We're going to change directories to that location (i.e. we're going to go to where the python executable is). On my computer, I would enter:

```bash
$ cd /c/Users/DBSpe/AppData/Local/Programs/Python/Python36-32
```

In general, you would enter:

```bash
$ cd <my-python-location>
```

!!! important
    The line that printed under `which python` was `<my-python-location>/python`. You'll then enter `cd <my-python-location>`, *not* `cd <my-python-location>/python`.

Copy `python.exe` to `python3.exe`:

```bash
$ cp python.exe python3.exe
```

Verify your python installation:

```bash
$ python3 --version
Python 3.6.8
```

??? error "Permission denied error"
    If you get a "Permission denied" error here, try this:

    1. Go to 'Manage app execution aliases' in system settings. You can get there by typing 'manage app execution aliases' in the Windows search bar.
    2. Turn off 'App Installer python3.exe'.

    <a href="https://stackoverflow.com/questions/56974927/permission-denied-trying-to-run-python-on-windows-10" target="_blank">See here for details.</a>

Next, upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip 20.1.1 from c:\users\dbspe\appdata\local\programs\python\python36-32\lib\site-packages\pip (python3.6)
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

Congratulations! You've installed python. Now return to your home directory:

```bash
$ cd
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

## Visual studio code

I recommend visual studio code for editing python files. <a href="https://code.visualstudio.com/" target="_blank">Download VS code here</a>

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.47.2
17299e413d5590b14ab0340ea477cdd86ff13dafx64
```

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
$ hlk setup win --chromedriver
```

This will ask you to copy the chromedriver Windows download URL from <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a> and paste it in your terminal window.

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

Then, download and install the heroku command line interface (heroku-CLI) following <a href="https://devcenter.heroku.com/articles/heroku-cli" target="_blank">these instructions</a>.

Close and re-open your terminal. Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x win32-x64 node-vxx.xx.x
```

Log into heroku:

```bash
$ heroku login
```

[Click here to return to the Deploy section of the tutorial](../tutorial/deploy.md).