#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth

import requests

import subprocess

app = Flask(__name__)
app.config['DEBUG'] = True
oauth = OAuth()

SCRIPTS = '../scripts/'
UTILS = '../utils/'

process = None

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
    global process
    process = subprocess.Popen("sh " + UTILS + "start_flume_collect.sh")
    print(process.pid)
    return render_template('index.html')



@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    global process
    if process is not None:
        subprocess.Popen("kill -9 " + process.pid)
        process = None
    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def listByWordTweets():
    if not request.json or not 'word' in request.json:
        return make_response(jsonify({'error' : 'Bad Request'}), 400)

    listaTweets = []
    # Ejecutar cosas

    return make_response(jsonify({'tweets' : listaTweets}), 200)

@app.route('/show_likes', methods=['POST'])
def showByYLikesTweets():
    pass

@app.route('/show_rts', methods=['POST'])
def showByZRtsTweets():
    pass




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


