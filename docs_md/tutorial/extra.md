# Bells and whistles

You already know most of the important stuff. Here are some tips and tricks to make your life easier.

## Settings

We've already used settings to set the password for the researcher dashboard. We can also use settings to change the default values of most attributes of most hemlock objects (see the API documentation for precise details). For example, let's add a back button to every page by default:

```python
from hemlock import Page, settings

settings['Page'].update({'back': True})
path = Page().preview()
```

## Duplicates

We often want to block the same participant from going through our survey multiple times. We do this with the `duplicate_keys` setting. This blocks visitors who match participants who've already completed the study on certain keys. For example:

```python
from hemlock import settings

settings.update({'duplicate_keys': ['IPv4', 'workerId']})
```

This blocks participants who match existing participants on IP address (IPv4) or their MTurk workerId.

## Screenouts

We may also want to screen out participants, e.g. if they've participated in similar studies we've run in the past.

We do this by 1) uploading a file called `screenouts.csv` to the root directory of our hemlock project. The top row of the csv are keys on which we want to screen (much like the duplicate keys we saw above). Then modify the `screenout_keys` setting:

```python
from hemlock import settings

settings.update({'screenout_keys': ['IPv4', 'workerId']})
```

## Validation off

During development and testing, we often want to be able to click through a survey quickly, ignoring validation. We can turn all validation off as follows:

```python
from hemlock import settings

settings.update({'validate': False})
```

## Google cloud buckets

Hook up a Google cloud bucket to your app with:

```bash
$ hlk gcloud-bucket <my-billing-account>
```

Make sure you have a Google cloud computing account and Google Cloud SDK installed. If using WSL, you can install these with hemlock-CLI:

```bash
$ hlk setup win --cloud-sdk
```

## Installing 3rd party packages

We ordinarily install 3rd party packages with:

```bash
$ pip install <requested-package> # or pip3 install <requested-package>
```

If you're using heroku, you need to include these in a `requirements.txt` file. If you're sharing your hemlock project with collaborators, I recommend additionally adding these to a `local-requirements.txt` file. 

Hemlock-CLI has a shortcut for 1) installing 3rd party packages, 2) adding them to `requirements.txt`, and 3) adding them to `local-requirements.txt`:

```bash
$ hlk install <requested-package>
```

## Redis

Hemlock integrates seamlessly with Redis for running complex background processes during surveys. To run redis locally, use:

```bash
$ hlk rq
```

To spin up a redis server on heroku, set the `REDIS_PLAN`, `WORKER_PROCTYPE`, and `WORKER_SCALE` variables in `env/production-scale.yml`.

See the [API docs on workers](../workers.md) for more details.

## Restarting your app

If your app crashes in production and you don't have time to take it offline and debug it, you can reboot your app with:

```bash
$ hlk restart
```

This won't fix your bug, but it might keep it at bay for a little while.