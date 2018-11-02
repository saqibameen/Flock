from datetime import datetime, timedelta
import time
import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

# Everything related to db goes here.
from contextlib import contextmanager
import logging
import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

global pool
pool = None
DATABASE_URL = os.environ['DATABASE_URL']
pool = ThreadedConnectionPool(1, 4, dsn=DATABASE_URL, sslmode='require')

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()
# DB Section Ends.

sched = BlockingScheduler()
# Utility function to filter the tweets.
def filterTweets(tweets):
    filteredTweets = []
    for tweet in tweets:
        d1 = tweet.created_at # Time when tweet was created.
        # d2 = datetime.now() + timedelta(hours=5) 
        d2 = datetime.now()
        # Convert to Unix timestamp
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        # Calculate the difference.
        minDiff = int(d2_ts-d1_ts) / 60
        # Only keep if the time difference is of 5 minutes or less and it contains a hashtag.
        if (minDiff <= 5 and len(tweet.entities['hashtags']) != 0):
            filteredTweets.append(tweet)
    return filteredTweets

# Schedular function.
@sched.scheduled_job(trigger = 'interval', minutes=1)
def listenForTweets():
    # The business logic!
    # Grab all unique emails.
    with get_db_cursor() as cur:
        cur.execute("SELECT DISTINCT email FROM twitteraccs;")
        uniqueMail = cur.fetchall() 

    mailDict = {}
    # For each email account get the associated twitter accounts and build a dictionary in the form { 'email':[array of db entries against that mail]}
    with get_db_cursor() as cur:
         for mail in range(len(uniqueMail)):
            cur.execute("SELECT * FROM twitteraccs where email='{}';".format(uniqueMail[mail][0]))
            twitterAccs = cur.fetchall()
            mailDict[uniqueMail[mail][0]] = twitterAccs

    tweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
    api = tweepy.API(tweep)

    for key, value in mailDict.items():
        if(len(value) <= 1): # If the associated accounts are less than 2 then no retweets.
            continue
        for x in range(len(value)): # x represents the email.
            # Grab last 15 tweets of the account.
            tweeets = api.user_timeline(id=value[x][2], count = 15)
            # Filter the tweets done in the last 5 minutes.
            filteredTweets = filterTweets(tweeets)
            for tweet in filteredTweets:
                # Grab array of hashtags. [{ 'text': },{ 'text': },..] 
                hashTagArray = tweet.entities['hashtags']
                if (len(hashTagArray) > 0): # If the tweet contains hashtag.
                    # Visit each account for the current email again, except the current, and look for hashtags.
                    for m in range(len(value)): # Start the same loop to match the hashtags.
                        # Skip the account in two cases:
                        # 1- If we are checking tweets of the same account.
                        # 2- If the tweet is by the same account and retweeted by linked account.           
                        if (m == x or tweet.user.id == value[m][2]):
                            continue
                        # Grab the hashtag for account.
                        hashtagStr = value[m][5]
                        # Visit each hastag of the tweet and see if that is followed by current account.
                        for hashtag in hashTagArray:
                            # If the hashtag found.
                            if (not(hashtagStr.find(hashtag['text']) == -1)):
                                # Build a tweepy instance and retweet the tweet.
                                retweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
                                retweep.set_access_token(value[m][3],value[m][4])
                                retweepy = tweepy.API(retweep)
                                try:
                                    retweepy.retweet(tweet.id)
                                    with get_db_cursor(commit=True) as cur:
                                        cur.execute("SELECT retweets FROM hashtags where hashtags='{}'".format(hashtag['text']))
                                        hashtagData = cur.fetchone()
                                        if (hashtagData == None): # If record does not exists.
                                            cur.execute("INSERT INTO hashtags (hashtags, retweets) VALUES ('{}', {});".format(hashtag['text'],1))
                                        else:
                                            cur.execute("UPDATE hashtags set retweets={} where hashtags='{}'".format((hashtagData[0] + 1),hashtag['text']))
                                except:
                                    print('tweeted already')   
                                break 

sched.start()