# Deployment

In the previous part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In this part of the tutorial, you'll learn how to deploy your application (i.e., put it into production or put it on the web).

## Setup

The easiest way to deploy web apps is with <a href="https://heroku.com/" target="_blank">heroku</a.>. Hemlock-CLI builds on the <a href="https://devcenter.heroku.com/articles/heroku-cli/" target="_blank">heroku-CLI</a> for deployment. Find the setup page for your OS for specific instructions:

- [Windows](../setup/win.md)
- [Windows Subsystem for Linux](../setup/wsl.md)
- [Mac](../setup/mac.md)
- [Linux](../setup/linux.md)

## Deploy using free resources for testing

Before deploying your app 'for real', I recommend deploying it using free resources and going through the survey once or twice to make sure everything's working.

??? note "If it works on my computer, why wouldn't it work online?"
    You'll deploy your app with cloud computing resources (a server, database, etc.). The goal is for the cloud computing environment to match the environment on your computer (your local environment).

    Unfortunately, the cloud computing environment occasionally differs from your local environment. For example, you might have a python package installed on your computer which isn't in your `requirements.txt` file, so the cloud computing environment won't know to download it. This is why I recommend testing your app with free or cheap cloud computing resources before scaling it up.

Deploying your application is as easy as:

```bash
$ hlk deploy
```

(You may have to give heroku access to your github account the first time you do this.)

This opens a web page with the deployment information. Give your application an awesome name and click 'Deploy app' at the bottom of the page.

Heroku needs about 2-4 minutes to set up your cloud computing environment. Use this time to reflect on the meaning of life. When it's done, head to https://my-awesome-app-name.herokuapp.com/ (replace 'my-awesome-app-name' with the name you gave to your application) to see your study online.

Give it a few test runs and, when you're satisfied it's working, destroy it:

```bash
$ heroku apps:destroy -a <your-awesome-app-name>
```

You'll be prompted to confirm by re-typing the app name.

## Deploy for real

We're finally ready to deploy our application *for real*. This is similar to what we just did, with a few small changes.

First, open `app.json`:

```bash
$ code app.json
```

We're going to modify this to give us more powerful compute resources. At the top of the file, we'll change our addons and formation from:

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

Save `app.json`.

??? note "What just happened?"
    `app.json` specifies the cloud computing resources we want to rent from heroku. The original file (the one you used to deploy your app the first time) used a free database (`"heroku-postgresql:hobby-dev"`) and a free web server (`"size": "free"`). The new file uses a more powerful database (`"heroku-postgresql:standard-0"`) and 10 more powerful web servers (`"quantity": 10, "size": "standard-1x"`).

    <a href="https://devcenter.heroku.com/articles/heroku-postgres-plans" target="_blank">See here</a> for more on heroku database (postgres) plans.

    <a href="https://devcenter.heroku.com/articles/dyno-types" target="_blank">See here</a> for more on heroku servers (dynos).

Let's deploy our app and set our configuration variables like we did before:

```bash
$ hlk deploy
```

1. Enter a name for your application.
2. Set your `PASSWORD`.

Like before, click 'Deploy app' at the bottom of the page.

Congratulations! Your app is now online. Send it to your friends and family to show off your wizardly programming skills.

Don't forget to download your data and destroy your application when you're finished:

```bash
$ heroku apps:destroy -a <my-app-name>
```

??? note "How much does this cost?"
    How much will it cost me to play with my app for 15 min? Answer: $0.10. 
    
    Calculation: This formation gives us a standard-0 database ($50/mo) and 10 standard-1x 'dynos' (like servers, $25/mo/dyno * 10 dynos = $250/mo). That's $300/mo total. Heroku prorates by the second, meaning that if you mess around with the app for 15 minutes, you'll be charged $300/mo * 1 mo/30 days * 1 day/24 hours * 1 hour/60 min * 15 min = $0.10. 

    How much will it cost me to run a study? Answer: $5. Do the same math, but assume your study is online for half a day. 

    The exact amount of compute power you need depends on the application. My recommendation for a standard-0 database and 10 standard-1x web dynos is a rough recommendation that will work well for most academic studies.

??? note "Altnernative deployment options"
    Hemlock uses a <a href="https://flask.palletsprojects.com/en/1.1.x/" target="_blank">Flask</a> backend, which means you can deploy it as you would any other Flask app. The <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world" target="_blank">Flask Mega-Tutorial</a> is, imho, the best resource for learning Flask, including deployment.

## Summary

Congratulations! You've made it through the hemlock tutorial. You can now initialize, modify, and deploy hemlock projects.

On the next page, I talk about some extra bells and whistles you'll likely find helpful.