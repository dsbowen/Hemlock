# Linux setup

These instructions are based on the Ubuntu distribution of WSL.

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
hlk x.x.x
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

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface.

**Read everything until STOP before creating your github token.**

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

Verify that you can open it as follows:

```bash
$ python3
>>> import webbrowser
>>> webbrowser.open('https://dsbowen.github.io/hemlock')
True
>>> exit()
```

You should see chrome open to the hemlock docs.

If you came here from the tutorial, you're now ready to return to it and get started with your first hemlock project. [Click here to go back to the First Project section of the tutorial](../tutorial/first_project.md).

## Chromedriver

Hemlock's custom debugging tool and survey view functions use <a href="https://chromedriver.chromium.org/downloads" target="_blank">chromedriver</a>. To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup linux --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver
/home/<my-linux-username>/webdrivers/chromedriver
```

#### Chrome and chromedriver compatibility

As of 07/14/2020, `hlk setup linux --chromedriver` installs chromedriver for chrome 83. While chrome updates automatically, chromedriver does not. This means that you will encounter compatibility issues when chrome updates to version 84+. To fix this:

1. <a href="https://chromedriver.chromium.org/downloads" target="_blank">Download the latest chromedriver here</a>.
2. Put the chrome binary in `/home/<my-linux-username>/webdrivers/`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver
/home/<my-linux-username>/webdrivers/chromedriver
```

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