# Module 2 Group Assignment: Generation Station

CSCI 5117, Fall 2018, [assignment description](https://docs.google.com/document/d/1HhB-96IZ-u5VlfBfdsy9-pkB59zzAapvW1MNsgvQq6M/edit)

## App Info:

<div align="center">
  <img src="https://i.imgur.com/JXAQWEU.png"/>
</div>

* Team Name: Mustache
* App Name: Flock
* App Link: <https://blooming-cove-74935.herokuapp.com/>

### Students

* JOAN ZHENG, zheng673@umn.edu
* Ounngy Ing, ingxx006@umn.edu
* Saqib Ameen, ameen007@umn.edu
* Mai Nguyen, nguy2365@umn.edu

## Key Features

* Setting up cron job to check for new tweets after regular intervals and retweet.
* Setting Cron Job on Heroku: it was quite hard to set cron jobs locally, once it was done, we had hard time deploying it on heroku. Because the cron job did not work on Heroku. We had to setup `clock dyno` on Heroku using APS Scheduler library of Python which also contains bug.
* Deployment to Heroku: We are in zone GMT-5, Twitter gives tweets time in GMT, while heroku also gives time in GMT. Since we checked for the new tweets after a specific time of lask check, it was hard to figure out and fix.
* Tweepy, which is python library for using Twitter API, is not very well documented and contains bug. Sometimes we had to change the code inside the library to fix it. 


## Screenshots of Site

* Homepage: Contains all the description of app, search box, and details.
<img src="https://i.imgur.com/snr6LyK.gif">
* Dashboard: Allows user to link the new Twitter account, unlink previous accounts, and manage hashtags for each account.
<img src="https://i.imgur.com/0aJE6Rn.png">
* Manage Hashtags: Add/Remove Hashtags.
<img src="https://i.imgur.com/xRtL8Ml.png">
* Search Box: Lists the hashtags people are retweeting about with no of retweets + AJAX Search.
<img src="https://i.imgur.com/EcBMDwW.png">


## Paper Prototype

![Paper Prototype](https://i.imgur.com/j4JYooU.jpg)
Paper Prototype with flow of application. 
1) Starting page shows login along with some recent tweets for non logged in users.
2) ~~On login it shows analytics of retweeted tweets.~~ Was not required.
3) Your Flocks link takes to the page where you can manage all the linked accounts.
4) Clicking on the account will take you to hashtag settings for that account.


## External Dependencies

* gunicorn: To deploy on Heroku
* psycopg2: To interact with db
* datetime: To compute time differences
* tweepy: Python lib to interact with Twitter API
* python-jose-cryptodome, six, flask-cors, request, auth-lib: For authentication
* apscheduler: To set cron jobs to check for tweets after regular intervals.
