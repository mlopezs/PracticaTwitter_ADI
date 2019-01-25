#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth
import json
import requests
import os, signal, time

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'development'
oauth = OAuth()

pid = 0
scavenging = False

webhooks = ['https://practicaadi-logger.appspot.com/activity']

# Recogida de tweets

@app.route('/collect', methods=['POST'])
def collectTweets():
    global pid
    global scavenging

    notify('collect')

    if scavenging:
        return make_response(jsonify({'error' : 'Forbidden'}), 403)
    
    scavenging = True

    pid = os.fork()
    if pid is 0:
        os.system('utils/start_flume_collect.sh')
        os._exit(0)
        
    return make_response(jsonify({'message' : 'collection is starting'}), 200)



@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    global pid
    global scavenging

    notify('stop_collect')

    if not scavenging:
        return make_response(jsonify({'error' : 'Forbiden'}), 403)
        
    os.system('utils/stop_flume_collect.sh')
    pid = 0
    scavenging = False

    return make_response(jsonify({'message' : 'collection stop successfully'}), 200)

@app.route('/list_word', methods=['POST'])
def listByWordTweets():

    notify('filter_by_word')

    if not request.json or not 'tweet_word' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    listaTweets = []

    os.system("pig -f scripts/pig_palabra.pig -p PIG_HOME=$PIG_HOME -p WORD={}".format(request.json['tweet_word']))
    
    file = open("data/results/sol_palabra.txt", 'r')

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    os.system("rm data/results/sol_palabra.txt")

    return make_response(jsonify({'tweets' : listaTweets}), 200)


@app.route('/show_likes', methods=['POST'])
def showByYLikesTweets():

    notify('filter_by_likes')

    if not request.json or not 'tweet_likes' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    listaTweets = []

    os.system("pig -f scripts/pig_likes.pig -p PIG_HOME=$PIG_HOME -p LIKES={}".format(request.json['tweet_likes']))
    
    file = open("data/results/sol_mgs.txt", 'r')

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    os.system("rm data/results/sol_mgs.txt")

    return make_response(jsonify({'tweets' : listaTweets}), 200)

@app.route('/show_rts', methods=['POST'])
def showByRtsTweets():

    notify('filter_by_rt')

    if not request.json or not 'tweet_retweets' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    listaTweets = []

    os.system("pig -f scripts/pig_rts.pig -p PIG_HOME=$PIG_HOME -p RTS={}".format(request.json['tweet_retweets']))
    
    file = open("data/results/sol_rts.txt", 'r')

    file.readline() 
    line = file.readline()

    while line:
        listaTweets.append(json.loads(line))
        line = file.readline()

    os.system("rm data/results/sol_rts.txt")

    return make_response(jsonify({'tweets' : listaTweets}), 200)

@app.route('/webhook', methods = ['POST'])
def addWebhook():
    
    if not request.json or not 'endpoint' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    endpoint = request.json['endpoint']    
    
    if endpoint in webhooks:
        return make_response(jsonify({'error' : 'Conflict'}), 409)

    webhooks.append(endpoint)

    return make_response(jsonify({"created":endpoint}), 201)

def notify(operation):
    for itWH in webhooks:
        response=requests.post(itWH, json = {'operation':operation})
        print response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


