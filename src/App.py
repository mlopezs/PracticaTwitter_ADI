#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth
import json
import requests
import os, signal

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'development'
oauth = OAuth()

pid = 0
scavenging = False

# Pagina principal
@app.route('/')
def index():
    global scavenging

    if scavenging == True:
        flash(u'[200] Scavenging tweets!')

    return render_template('index.html')

@app.route('/operations', methods=['GET'])
def show_operations():
    return render_template('tweets_adm.html')

# Recogida de tweets

@app.route('/collect', methods=['POST'])
def collectTweets():
    global pid
    global scavenging

    pid = os.fork()
    if pid == 0:
        try:
            os.system('utils/start_flume_collect.sh')
            scavenging = True
            print("PID: {}".format(pid))
        except:
            error = u'[ERROR {}] Sorry, imposible to scavenging. Try again later...'.format(503)
            flash(error, 'error')
        
    return render_template('index.html')



@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    global pid
    global scavenging

    if pid != 0:
        try:
            os.system('utils/stop_flume_collect.sh')
            pid = 0
            scavenging = False
            flash(u'[200] Stop scavenging tweets!')
        except:
            error = u'[ERROR {}] Sorry, imposible to stop. Try again later...'.format(503)
            flash(error, 'error')

    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def listByWordTweets():

    try:
        word = request.form['tweet_word']
    except:
        if not request.json or not 'tweet_word' in request.json:
            return make_response(jsonify({'error' : 'Bad Request'}), 400)
        word = request.json['tweet_word']

    listaTweets = []

    # ejecutar weas
    # os.system("pig -f scripts/pig_palabra.pig -p WORD={}".format(request.json['word']))
    os.system("pig -f scripts/pig_palabra.pig -p PIG_HOME=$PIG_HOME -p WORD={}".format(word))
    
    
    file = open("data/results/sol_palabra.txt", 'r')
    # Hay que saltarse la primera linea para que json.loads funcione, porque la
    # primera linea no esta en formato json

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    
    if len(listaTweets) >=1:
        flash(u'[200] Tweets find!')
    else:
        error = u'[ERROR {}] Sorry, no tweets finded...'.format(404)
        flash(error, 'error')

    return render_template('tweets_finded.html', tweets=listaTweets)

@app.route('/show_likes', methods=['POST'])
def showByYLikesTweets():
    try:
        number_mgs = request.form['tweet_likes']
    except:
        if not request.json or not 'tweet_likes' in request.json:
            return make_response(jsonify({'error' : 'Bad Request'}), 400)
        number_mgs = request.json['tweet_likes']

    listaTweets = []

    # ejecutar weas
    # os.system("pig -f scripts/pig_palabra.pig -p WORD={}".format(request.json['word']))
    os.system("pig -f scripts/pig_likes.pig -p PIG_HOME=$PIG_HOME -p LIKES={}".format(number_mgs))
    
    
    file = open("data/results/sol_mgs.txt", 'r')
    # Hay que saltarse la primera linea para que json.loads funcione, porque la
    # primera linea no esta en formato json

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    
    if len(listaTweets) >=1:
        flash(u'[200] Tweets find!')
    else:
        error = u'[ERROR {}] Sorry, no tweets finded...'.format(404)
        flash(error, 'error')

    return render_template('tweets_finded.html', tweets=listaTweets)

@app.route('/show_rts', methods=['POST'])
def showByZRtsTweets():
     #if not request.json or not 'word' in request.json:
        #return make_response(jsonify({'error' : 'Bad Request'}), 400)
    try:
        number_rts = request.form['tweet_retweets']
    except:
        if not request.json or not 'tweet_retweets' in request.json:
            return make_response(jsonify({'error' : 'Bad Request'}), 400)
        number_rts = request.json['tweet_retweets']

    listaTweets = []

    # ejecutar weas
    # os.system("pig -f scripts/pig_palabra.pig -p WORD={}".format(request.json['word']))
    os.system("pig -f scripts/pig_rts.pig -p PIG_HOME=$PIG_HOME -p RTS={}".format(number_rts))
    
    
    file = open("data/results/sol_rts.txt", 'r')
    # Hay que saltarse la primera linea para que json.loads funcione, porque la
    # primera linea no esta en formato json

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    
    if len(listaTweets) >=1:
        flash(u'[200] Tweets find!')
    else:
        error = u'[ERROR {}] Sorry, no tweets finded...'.format(404)
        flash(error, 'error')

    return render_template('tweets_finded.html', tweets=listaTweets)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


