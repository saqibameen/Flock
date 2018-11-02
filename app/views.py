from app import app, db, auth
import os
import json
import psycopg2
import tweepy
import os
from datetime import datetime, timedelta
import time
# from apscheduler.scheduler import Scheduler.
from datetime import datetime, timedelta
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode
from functools import wraps
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for, make_response, session, g, logging

@app.before_first_request
def initialize():
    # Setup the db.
    db.setup()
    app.secret_key=os.environ['APP_SECRET_KEY']
    auth.setup()
    # Setup the auth.
    global auth0
    auth0 = auth.auth0

# Routing.
# Protected Page. Only accessible after login.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here.
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

# Flock homepage.
@app.route('/')
def index():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT hashtags, retweets FROM hashtags;")
        hashtags = cur.fetchall()
        app.logger.info(hashtags)
    return render_template('index.html', hashtags = hashtags)

# Dashboard.
@app.route('/dashboard')
@requires_auth
def dashboard():
    print('dashboard')
    # Get all the twitter accounts of given account.
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM twitteraccs where email=%s", (session['profile']['email'],))
        twitteraccounts = cur.fetchall()

    tweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
  
    api = tweepy.API(tweep)
    # Fetch data of all these accounts.
    linkedAccs = list(map(lambda x : api.get_user(x['twitter_id']) , twitteraccounts))
    return render_template('dashboard.html', accounts = linkedAccs)

# Manage add flock.
@app.route('/add-flock')
@requires_auth
def addFlock():
    # Make an instance of tweepy object.
    tweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
    # Get the authorization URL.
    redirect_url = tweep.get_authorization_url()
    # Redirect to the authorization url.
    return redirect(redirect_url)

# Twitter auth callback.
@app.route(os.environ['TWITTER_CALLBACK'])
def addFlockCallback():
    # Make an instance of tweepy object.
    tweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
    # Grab the arguments from the url.
    authToken = request.args.get('oauth_token')
    authVerifier = request.args.get('oauth_verifier')

    # Save the tokens to the tweepy object.
    tweep.request_token = { 'oauth_token' : authToken,
                            'oauth_token_secret' : authVerifier }
    # Get access tokens for the account. 
    tweep.get_access_token(authVerifier)
    # These are the two tokens we need to save in the db.
    accessKey = tweep.access_token
    accessKeySecret = tweep.access_token_secret
    
    # Pass the tweep object to access API.
    api = tweepy.API(tweep)

    with db.get_db_cursor() as cur:
        cmd = "select * from twitteraccs where email = '{}' and twitter_id = '{}';".format(session['profile']['email'], api.me().id)
        cur.execute(cmd) 
        result = cur.fetchone()

    if(result): # If the acccount already exists.
        return redirect('/dashboard')

    with db.get_db_cursor(commit=True) as cur:
        cmd = "INSERT INTO twitteraccs (email, twitter_id, access_token, access_token_secret, hashtags) VALUES ('{}', {},'{}', '{}', '{}');".format(session['profile']['email'], api.me().id, accessKey, accessKeySecret,None)
        cur.execute(cmd)        
        return redirect('/dashboard')

# Auth0 Login.
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.environ['REDIRECT_URL'], audience=os.environ['AUTH0_DOMAIN']+'/userinfo')

@app.route('/callback')
def callbackHandling():
    # Handles response from token endpoint.
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture'],
        'email': userinfo['email']
    }
    return redirect('/dashboard')

# 404. 
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# Auth0 Logout.
@app.route('/logout')
def logout():
    # Clear session stored data.
    session.clear()
    # Redirect user to logout endpoint.
    return redirect('/')
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.environ['CLIENT_ID']}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# Route to manage hashtags for individual flock.
@app.route('/flocks/<twitter_id>')
@requires_auth
def manageFlock(twitter_id):
    tweep = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['CONSUMER_SECRET'])
    api = tweepy.API(tweep)
    account = api.get_user(twitter_id)

    with db.get_db_cursor() as cur:
        cmd = "SELECT hashtags from twitteraccs where twitter_id = '{}' and email = '{}';".format(twitter_id, session['profile']['email'])
        cur.execute(cmd)     
        hashtagStr = cur.fetchone()

    session['current_twitter_id'] = account.id
    # Converts the comma separated hashtags string into a list.
    hashtags = hashtagStr[0].split(',') 
    if (hashtags[0] == 'None' or hashtags[0] == '' ):
        hashtags = []
    return render_template('flock.html', account = account, hashtags = hashtags)

# Update hashtags.
@app.route('/saveHashtags', methods=['POST'])
def saveHashtags():
    currTwitterId = session['current_twitter_id']
    email = session['profile']['email']
    hashtags = request.form['hashtags']

    with db.get_db_cursor(commit=True) as cur:
        cmd = "UPDATE twitteraccs set hashtags = '{}' where email='{}' and twitter_id='{}';".format(hashtags, email, currTwitterId)
        cur.execute(cmd)     

    return json.dumps({'status':'OK','hashtags':hashtags})

# Unlink the account via AJAX.
@app.route('/unlinkAccount', methods=['POST'])
def unlinkAccount():
    twitter_id = request.form['twitter_id']
    email = session['profile']['email']
    with db.get_db_cursor(commit=True) as cur:
        cmd = "DELETE from twitteraccs where email = '{}' and twitter_id = '{}';".format(email, twitter_id)
        cur.execute(cmd)

    return json.dumps({'status': 'OK'})  

@app.route('/searchHashtags', methods=['POST'])
def searchHashtags():
    query = request.form['query']
    if not query:
        return json.dumps({'Status':'400'})
    # Search from the db.
    with db.get_db_cursor() as cur:
        # XXX: hack for query wildcard characters w/ correct escaping.
        query_wildcard = f"%{query}%"
        cur.execute("SELECT hashtags FROM hashtags where hashtags ilike (%s)", (query_wildcard,))
        hashtags = [record for record in cur]
        app.logger.info(hashtags)
    return json.dumps({'status': 'OK', 'hashtags': hashtags}) 