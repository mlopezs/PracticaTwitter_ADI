import random
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Playlist, db

bp_playlist=Blueprint("bp_tweets", __name__)
