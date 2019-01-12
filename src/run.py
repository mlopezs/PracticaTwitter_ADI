#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth
import requests
import os, signal

app = Flask(__name__)
app.config['DEBUG'] = True
oauth = OAuth()

pid = 0

# Pagina principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operations', methods=['GET'])
def show_operations():
    return render_template('tweets_adm.html')

# Recogida de tweets

@app.route('/collect', methods=['POST'])
def collectTweets():
    global pid
    pid = os.fork()
    if pid == 0:
        os.system('utils/start_flume_collect.sh')
    print("PID: {}".format(pid))
    return render_template('index.html')



@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    global pid
    if pid != 0:
        os.kill(pid, signal.SIGTERM)
        pid = 0
    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def listByWordTweets():
    if not request.json or not 'word' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    listaTweets = []

    # ejecutar weas
    os.system("pig -f scripts/pig_palabra.pig -p WORD={}".format(request.json['word']))
    # copy to local
    os.system("hdfs dfs -copyToLocal /user/storage/sol_palabra results/sol_palabra.txt")

    file = open("results/sol_palabra.txt", 'r')
    line = file.readline()

    while line:
        listaTweets.append(line)
        line = file.readline()
        
    return make_response(jsonify({'tweets' : listaTweets}), 200)

@app.route('/show_likes', methods=['POST'])
def showByYLikesTweets():
    pass

@app.route('/show_rts', methods=['POST'])
def showByZRtsTweets():
    pass



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


