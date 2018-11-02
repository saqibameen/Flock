<div align="center">
  <img src="https://i.imgur.com/JXAQWEU.png"/>
</div>

> Twitter automation app to link multiple accounts, listen for hashtags, and retweet. Built using Flask (Python) and Tweepy.

<small> Note: This app for learning purposes only. 
<em>Do not use it for commercial purposes</em>
</small>

## 🚀 Set up the Application
The application was structured to run on Heroku. You can follow the steps below to set it up.

1. This app uses `postgres` db by Heroku. This app makes use of free Heroku account so you can easily follow this. First you need to link your cloned repo with Heroku. Make sure you have linked your Heroku account with the app. It makes use of Heroku CLI. Follow the [Instructions](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) on Heroku official site to install Heroku CLI. After installation follow the steps below to set up database.
* Create Heroku app.
```
heroku create
```
* Create the database.
```
heroku addons:create heroku-postgresql:hobby-dev
```
* Use the following command the get the db connection link.
```
heroku config:get DATABASE_URL
```
That's the URL you will need in the next step.

2. Rename the `sample.env` file contains all the configuration variables you need to set on Heroku.
```
# Variables for flask.
FLASK_APP=app
FLASK_ENV=development
APP_SECRET_KEY=''

# Variables for Heroku postgres.
DATABASE_URL=''

# Variables for Auth0.
AUTH0_DOMAIN=''
CLIENT_ID=''
CLIENT_SECRET=''

# Variables for Tweepy.
API_KEY=''
CONSUMER_SECRET=''
TWITTER_CALLBACK=''
```
* **Variables for Heroku postgres**: We got it in the previous step.
* **Variables for Auth0**: This app uses **auth0** for authentication purpose. So you can get those credentials by setting up an app on auth0. The `REDIRECT_URL` is the allowed callback url for logout. So make sure you add it in your app on auth0 as well.
* **Variables for Tweepy**: Tweepy is the Twitter API package for Python. And the `API_KEY` and `CONSUMER_SECRET` are required by Tweepy to conenct to Twitter app. To get these keys, you need to sign up for a [Twitter Developer Account](https://developer.twitter.com/). Once your account is approved, create an app and grab those keys.
_Remember_ when you create an app, it requires a callback URL. That's the value of `TWITTER_CALLBACK` and it should be something like `/twitter/callback`, i.e. relative to your root.
* Use the following command to set all the configuration variables on Heroku.
```
heroku config:set ENV_VARIABLE_NAME=VALUE
```

3. Set up the databse by using the instructions below:
* In the CLI run the following command in your project directory to access the database.
```
heroku psql
```
* Head to `documentation` folder of this repo, it contains all the commands you need to run at this point to create the database tables.
**Note:** This app doesn't hash the `Twitter Auth Keys` before saving in the database. 

4. Deploy it on Heroku.
* Create a `clock` dyno on Heroku.
```
heroku ps:scale clock=1
```
* Push the code to Heroku.
```
git push heroku master
```
That's it! Your site is live on Heroku! 💯

## 📸 Screenshots of App

* Homepage: Contains all the description of app, search box, and details.
<img src="https://i.imgur.com/snr6LyK.gif">

* Dashboard: Allows user to link the new Twitter account, unlink previous accounts, and manage hashtags for each account.
<img src="https://i.imgur.com/0aJE6Rn.png">

* Manage Hashtags: Add/Remove Hashtags.
<img src="https://i.imgur.com/xRtL8Ml.png">

* Search Box: Lists the hashtags people are retweeting about with no of retweets + AJAX Search.
<img src="https://i.imgur.com/EcBMDwW.png">

## License
Released under GNU GPLv2.0 or later license.

##### → Feel free to tweet and say 👋 at me [@MrSaqibAmeen](https://twitter.com/MrSaqibAmeen/)

