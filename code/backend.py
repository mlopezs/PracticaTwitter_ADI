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
mySession=None
currentUser=None
myOperation_url=None
myOperation_json=None
myOperation_method=None


@bp_playlist.route('/tweets', methods = ['GET'])
def getPlaylists():
    listPlaylists = []
    for itPlaylist in Playlist.query.all():
        listPlaylists.append(itPlaylist.toJSON)
    return make_response(jsonify({"playlists":listPlaylists}), 200)

