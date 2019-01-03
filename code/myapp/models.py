from flask import url_for
from . import db

tweets_tab = db.Table('tweets_tab',
    db.Column('tweet_id', db.String(64), db.ForeignKey('tweets.idTweet')),
    db.Column('playlist_id', db.String(64), db.ForeignKey('playlists.name'))
)
