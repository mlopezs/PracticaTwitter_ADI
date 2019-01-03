import random
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Tweet, db

bp_tweets=Blueprint("bp_tweets", __name__)


@bp_tweets.route('/get_tweets', methods=['GET'])
def getTweets():
    listTweets = []
    for itTweet in Tweet.query.all():
        listTweets.append(itTweet.toJSON)
    return make_response(jsonify({"Tweets":listTweets}), 200)

@bp_tweets.route('/date_filter', methods=['POST'])
def filterByDateTweets():
    pass

@bp_tweets.route('/list_word', methods=['POST'])
def listByWordTweets():
    pass

@bp_tweets.route('/show_likes', methods=['POST'])
def showByZLikesTweets():
    pass

