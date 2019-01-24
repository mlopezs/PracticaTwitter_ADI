#!/usr/bin/python2.7

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth

import json
import requests

app                 =   Flask(__name__)
app.config['DEBUG'] =   True
app.secret_key      =   'development'
oauth               =   OAuth()

endpoint            =   'http://localhost:8080'

my_session          =   None
current_user        =   None

twitter = oauth.remote_app( 'twitter',
    base_url            =   'https://api.twitter.com/1.1/',
    request_token_url   =   'https://api.twitter.com/oauth/request_token',
    access_token_url    =   'https://api.twitter.com/oauth/access_token',
    authorize_url       =   'https://api.twitter.com/oauth/authenticate',
    consumer_key        =   'kaZxew3pORQWPaa7ncK009x7u',
    consumer_secret     =   'VcXVuZBobDJq9GXqYhDrmUeRE0gdpkYL6dBnc4gL7J9uOUAYwC'
)

@twitter.tokengetter
def get_twitter_token(token=None):
    global my_session

    if my_session is not None:
        return my_session['oauth_token'], my_session['oauth_token_secret']

@app.before_request
def before_request():
    global my_session
    global currentUser
    
    currentUser = None
    if my_session is not None:
        currentUser = my_session

@app.route('/login')
def login():
    callback_url=url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)

@app.route('/logout')
def logout():
    global my_session
    
    my_session = None
    return redirect(url_for('index'))

@app.route('/oauthorized')
def oauthorized():
    global my_session
    
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        my_session = resp
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operations')
def show_operation():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))

    return render_template('tweets_adm.html')

@app.route('/collect', methods=['POST'])
def collect_tweets():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))

    response = requests.post(endpoint + '/collect')

    if response.status_code == 403:
        flash('Already collecting', 'error')
    else:
        flash('Collecting tweets')

    return render_template('index.html')

@app.route('/no_collect', methods=['POST'])
def stop_collect():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))

    response = requests.post(endpoint + '/no_collect')

    if response.status_code == 403:
        flash('Wasn\'t collecting', 'error')
    else:
        flash('Collection stop')

    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def list_tweets_by_word():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))

    word = request.form['tweet_word']
    response  = requests.post(endpoint + '/list_word', json={'tweet_word' : word})

    if not response.status_code == 200:
        flash('Unexpected Error', 'error')
        return render_template('index.html')
    else:
        return render_template('tweets_finded.html', tweets=response.json()['tweets'])

@app.route('/show_likes', methods=['POST'])
def list_tweets_by_likes():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))

    like_count = request.form['tweet_likes']
    response =  requests.post(endpoint + '/show_likes', json={'tweet_likes' : like_count})

    if not response.status_code == 200: 
        flash('Unexpected Error', 'error')
        return render_template('index.html')
    else:
        return render_template('tweets_finded.html', tweets=response.json()['tweets'])


@app.route('/show_rts', methods=['POST'])
def list_tweets_by_rt():
    if my_session is None or current_user is None:
        return redirect(url_for('login'))
        
    rt_count = request.form['tweet_retweets']
    response = requests.post(endpoint + '/show_rts', json={'tweet_retweets' : rt_count})

    if not response.status_code == 200:
        flash('Unexpected Error', 'error')
        return render_template('index.html')
    else:
        return render_template('tweets_finded.html', tweets=response.json()['tweets'])    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)