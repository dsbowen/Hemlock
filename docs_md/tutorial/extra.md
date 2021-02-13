# Bells and whistles

You already know the important stuff. Here are some tips and tricks to make your life easier.

## Redis

One of hemlock's most impressive features is seamless integration with Redis for running complex background processes during surveys. [Read more here](../models/worker.md).

## Settings

We can use settings to change the default values of most attributes of most hemlock objects (see the API documentation for precise details). For example, let's add a back button to every page by default:

```python
from hemlock import Page, settings

settings['Page'].update({'back': True})
Page().preview()
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

<!-- ## Google cloud buckets

Hook up a Google cloud bucket to your app with:

```bash
$ hlk gcloud-bucket <my-billing-account>
```

Make sure you have a Google cloud computing account and Google Cloud SDK installed. If using WSL, you can install these with hemlock-CLI:

```bash
$ hlk setup win --cloud-sdk
```

Additionally, install the google cloud storage python API with:

```bash
$ pip3 install google-cloud-storage # or hlk install google-cloud-storage (see below)
``` -->