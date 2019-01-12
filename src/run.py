#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth

import requests

import os, subprocess, signal

app = Flask(__name__)
app.config['DEBUG'] = True
oauth = OAuth()

# pid = 0

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
    # global pid
    # pid = subprocess.Popen('utils/start_flume_collect.sh', shell=True).pid
    return render_template('index.html')



@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    # global pid
    # if pid != 0:
    #     #os.kill(pid, signal.SIGTERM)
    #     os.system("kill 9 {}".format(pid))
    #     pid = 0
    return render_template('index.html')

@app.route('/list_word', methods=['POST'])
def listByWordTweets():
    pass

@app.route('/show_likes', methods=['POST'])
def showByYLikesTweets():
    pass

@app.route('/show_rts', methods=['POST'])
def showByZRtsTweets():
    pass



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


