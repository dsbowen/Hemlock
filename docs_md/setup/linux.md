# Linux setup

These instructions were written for Ubuntu 20.04.

!!! note
    About 50% of the problems you encounter during setup can be fixed by closing and re-opening your terminal window. If you have any problems, this is the first thing to try.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI. Many linux distributions come with python3.

Verify your python3 installation:

```bash
$ python3 --version
Python 3.x.x
```

If you don't have python3, <a href="https://www.python.org/downloads/" target="_blank">download it here</a>. I recommend python3.6. Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues. Make sure python3 is in your path.

Upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip xx.x.x ...
```

#### pip versus pip3

You'll install several python packages using pip. Conventionally, the command to install these is:

```bash
$ pip install <my-requested-package>
```

You may need to replace this with:

```bash
$ pip3 install <my-requested-package>
```

Many hemlock-CLI commands assume you can pip install with `pip3`.

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Download with:

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

<a href="https://git-scm.com/download/linux">Find installation instructions for git here</a>.

Verify your git installation:

```bash
$ git --version
git version x.xx.x.linux.1
```

Then, create a <a href="https://github.com" target="_blank">github account here</a>. Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github-user-email>
```

**Read everything until STOP before creating your github token.**

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface.

1. Create a github token by following <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token" target="_blank">these instructions</a>.
2. When setting permissions (step 7), check 'repo'.
3. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

**STOP.**

## Visual studio code

I recommend visual studio code for editing python files. <a href="https://code.visualstudio.com/" target="_blank">Download VS code here</a>.

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.xx.x
```

## Jupyter

<a href="https://jupyter.org/" target="_blank">Jupyter</a> allows you to quickly iterate on project designs. Install jupyter notebook with pip:

```bash
$ pip install -U notebook
```

Close and re-open your terminal. Verify your jupyter installation:

```bash
$ jupyter --version
jupyter core     : x.x.x
jupyter-notebook : x.x.x
...
```

## Google chrome

Hemlock is developed and tested primarily on chrome. <a href="https://www.google.com/chrome/" target="_blank">Download chrome here</a>.

Verify that you can open it:

```
$ python3 -m webbrowser https://dsbowen.github.io
```

You should see chrome open to my github.io page.

If you came here from the tutorial, you're now ready to return to it and get started with your first hemlock project. [Click here to go back to the First Project section of the tutorial](../tutorial/first_project.md).

## Chromedriver

Hemlock's custom debugging tool and survey view functions use <a href="https://chromedriver.chromium.org/downloads" target="_blank">chromedriver</a>. To use these features locally, you'll need to download chromedriver (this command assumes you have `curl` installed; <a href="https://www.tecmint.com/install-curl-in-linux/" target="_blank">see here to install `curl`</a>):

```bash
$ hlk setup linux --chromedriver
```

This will ask you to copy the chromedriver Linux download URL from <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a> and paste it in your terminal window.

Verify your chromedriver installation:

```bash
$ chromedriver --version
ChromeDriver xx.xxxx
```

#### Chrome and chromedriver compatibility

Google Chrome will automatically update. Chromedriver will not. If you encounter a compatibility error in the future, simply repeat the above instructions.

If you came here from the Debug section of the tutorial, you're now ready to return to it and run the debugger. [Click here to go back to the Debug section of the tutorial](../tutorial/debug.md).

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e. putting them online), including hemlock applications. <a href="https://signup.heroku.com/" target="_blank">Sign up for heroku here</a>.

You can install heroku-CLI using hemlock-CLI:

```bash
$ hlk setup linux --heroku-cli
```

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x linux-x64 node-vxx.xx.x
```

**Note.** See <a href="https://github.com/heroku/legacy-cli/issues/1969" target="_blank">this github issue</a> if you experience a 'EACCES' error. *Do not* simply use `sudo`; this only masks issues you'll encounter later.

[Click here to return to the Deploy section of the tutorial](../tutorial/deploy.md).