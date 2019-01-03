#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Alfonso Barragán Carmona
# Marcos López Sobrino
# Roberto Plaza Romero

from flask import Flask, request, redirect, url_for, flash, render_template, make_response, jsonify
from flask_oauthlib.client import OAuth

import requests

app = Flask(__name__)
app.config['DEBUG'] = True
oauth = OAuth()

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
    pass

@app.route('/no_collect', methods=['POST'])
def stopCollectTweets():
    pass

# Operaciones
@app.route('/date_filter', methods=['POST'])
def filterByDateTweets():
    listTweets = []
    pass

@app.route('/list_word', methods=['POST'])
def listByWordTweets():
    pass

@app.route('/show_likes', methods=['POST'])
def showByZLikesTweets():
    pass




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)


