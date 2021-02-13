# Checklist

This is a checklist of the steps involved in initializing, editing, and deploying a hemlock project.

This will make sense after you [go through the tutorial](tutorial/intro.md).

## Initialize

```bash
$ hlk init <my-project-name> <my-github-username> <my-github-token>
$ cd <my-project-name>
```

??? note "Additional step for Windows git bash"
    ```bash
    hlk setup-venv <my-project-name>
    ```

## Edit

Iterate quickly on the blackboard:

```bash
$ jupyter notebook # open blackboard.ipynb, Kernel >> Change kernel >> <my-project-name>
```

Edit survey files:

```bash
$ code survey.py
```

Run locally:

```bash
$ hlk serve
```

Debug:

```bash
$ hlk debug
```

## Deploy

Deploy and test using free resources:

```bash
$ hlk deploy # make sure to set the PASSWORD environment variable
```

Destroy the test app:

```bash
$ heroku apps:destroy -a <my-app-name>
```

Change `app.json` from:

```json
{
    "addons": ["heroku-postgresql:hobby-dev"],
    "formation": {
        "web": {"quantity": 1, "size": "free"}
    },
    ...
```

to:

```json
{
    "addons": ["heroku-postgresql:standard-0"],
    "formation": {
        "web": {"quantity": 10, "size": "standard-1x"}
    },
    ...
```

Deploy 'for real':

```bash
hlk deploy # set PASSWORD
```