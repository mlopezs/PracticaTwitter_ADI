from flask import url_for
from . import db

tweets_tab = db.Table('tweets_tab',
    db.Column('tweet_id', db.String(64), db.ForeignKey('tweets.idTweet'))
)

class Tweet(db.Model):
    __tablename__   = 'tweets'
    idTweet         = db.Column(db.String(64), primary_key=True)
    message         = db.Column(db.String(280), nullable=False)
    user            = db.Column(db.String(40), nullable=False)
    date            = db.Column(db.Date, nullable=False)
    likes           = db.Column(db.Integer)
    retweets        = db.Column(db.Integer)
    
    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])
