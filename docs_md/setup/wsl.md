# Windows Subsystem for Linux (WSL) setup

These instructions were written for Windows 10.

Why WSL? The main reason I use WSL is that Windows OS doesn't have a fork (only a spoon), which means you'll need WSL if you want to run Redis. You can find <a href="https://docs.microsoft.com/en-us/windows/wsl/install-win10" target="_blank">download instructions for WSL here</a>. Download WSL2, not WSL1. I personally use the Ubuntu distribution.

After you've installed WSL, open a terminal window (WIN + R, then enter e.g., 'ubuntu2004'. You may be prompted to create a username and password.

!!! note
    About 50% of the problems you encounter during setup can be fixed by closing and re-opening your terminal window. If you have any problems, this is the first thing to try.

## Update your package lists

```bash
$ sudo apt-get update
```

## Visual studio code

**Read everything until STOP before downloading or installing anything.**

I recommend visual studio code for editing python files. <a href="https://code.visualstudio.com/" target="_blank">Download VS code here</a> **Make sure to download the Windows version, not the Linux version.**

**STOP**

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.xx.x
```

## X Server

X server allows you to install python packages and interact with web browsers inside WSL.

Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) **in Windows**. Make sure you allow X server to access public networks. If you accidentally didn't, see <a href="https://skeptric.com/wsl2-xserver/" target="_blank">here</a> and <a href="https://github.com/cascadium/wsl-windows-toolbar-launcher#firewall-rules" target="_blank">here</a> for troubleshooting.

Then run `xlaunch.exe` from the VcSrc folder in Program Files. Keep the default settings *except make sure to select "Disable access control"*.

Finally, we set the DISPLAY environment variable for the X server. Open your `.profile` or `.bashrc` file with:

```bash
$ code .profile # or code .bashrc
```

Add these lines to the bottom of the file.

```
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
export LIBGL_ALWAYS_INDIRECT=1
```

Verify that you've set the DISPLAY variable correctly:

```bash
$ echo $DISPLAY
172.19.192.1:0.0
```

If that didn't work, close and re-open your terminal, then run `echo $DISPLAY` again.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI.

Most WSL distributions come with python3. Verify your python installation with:

```
$ python3 --version
Python 3.x.x
```

If you don't have python intalled on your WSL distribution, <a href="https://www.python.org/downloads/" target="_blank">download python here</a>. I recommend python3.6, rather than the latest version. Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

Install pip3:

```bash
$ sudo apt install -f -y python3-pip
```

Respond 'Yes' if asked whether you want to restart services automatically.

Verify your pip3 installation:

```bash
$ pip3 --version
pip x.x.x from /usr/lib/python3/dist-packages (python 3.x)
```

You'll also need the ability to create virtual environments:

```bash
$ apt install -f -y python3-venv
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

You can find <a href="https://git-scm.com/download/linux">git download and installation instructions here</a>.

Verify your git installation:

```bash
$ git --version
git version 2.17.1
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

To download and install Google chrome, run:

```bash
$ hlk setup wsl --chrome
```

Verify your installation:

```bash
$ google-chrome-stable --version
```

Verify that you can open it as follows:

```
$ python3 -m webbrowser https://dsbowen.github.io
```

You should see chrome open to my github.io page.

If you came here from the tutorial, you're now ready to return to it and get started with your first hemlock project. [Click here to go back to the First Project section of the tutorial](../tutorial/first_project.md).

## Chromedrover

To download and install chromedriver, run:

```bash
$ hlk setup wsl --chromedriver
```

Verify your installation

```bash
$ chromedriver --version
```

#### Chrome and chromedriver compatibility

Google chrome will automatically update. Chromedriver will not. If you encounter a compatibility error in the future, simply repeat the above instructions.

If you came here from the Debug section of the tutorial, you're now ready to return to it and run the debugger. [Click here to go back to the Debug section of the tutorial](../tutorial/debug.md).

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e. putting them online), including hemlock applications. <a href="https://signup.heroku.com/" target="_blank">Sign up for heroku here</a>.

If using hemlock-CLI, you can install and configure the heroku command line interface with:

```bash
$ hlk setup wsl --heroku-cli
```

This will prompt you to create and log in to a heroku account.

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x linux-x64 node-vxx.xx.x
```

**Note.** See <a href="https://github.com/heroku/legacy-cli/issues/1969" target="_blank">this github issue</a> if you experience a 'EACCES' error. *Do not* simply use `sudo`; this only masks issues you'll encounter later.

[Click here to return to the Deploy section of the tutorial](../tutorial/deploy.md).