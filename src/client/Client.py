#!/usr/bin/python2.7

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth

import json
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'development'
oauth = OAuth()

endpoint = 'http://localhost:8080'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operations')
def show_operation():
    return render_template('tweets_adm.html')

@app.route('/collect', methods=['POST'])
def collect_tweets():
    response = requests.post(endpoint + '/collect')

    if response.status_code is 403:
        flash('Already collecting')
    else:
        flash('Collecting tweets')

    return render_template('index.html')

@app.route('/no_collect', methods=['POST'])
def stop_collect():
    response = requests.post(endpoint + '/no_collect')

    if response.status_code is 403:
        flash('Wasn\'t collecting')
    else:
        flash('Stop collecting')

    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def list_tweets_by_word():

    word = request.form['tweet_word']
    response  = requests.post(endpoint + '/list_word', json={'tweet_word' : word})

    if response.status_code is not 200:
        flash(error, 'Unexpected Error')
        return render_template('index.html')
    else:
        print response.data
        return render_template('tweets_finded.html', tweets=None)

@app.route('/show_likes', methods=['POST'])
def list_tweets_by_likes():

    like_count = request.form['tweet_likes']
    response =  requests.post(endpoint + '/show_likes', json=jsonify({'tweet_likes' : like_count}))

    if response.status_code is not 200: 
        flash(error, 'Unexpected Error')
        return render_template('index.html')
    else:
        return render_template('tweets_finded.html', tweets=response.json['tweets'])


@app.route('/show_rts', methods=['POST'])
def list_tweets_by_rt():

    rt_count = request.form['tweet_retweets']
    response = requests.post(endpoint + '/show_rts', json=jsonify({'tweet_retweets' : rt_count}))

    if response.status_code is not 200:
        flash(error, 'Unexpected Error')
        return render_template('index.html')
    else:
        return render_template('tweets_finded.html', tweets=response.json['tweets'])    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)