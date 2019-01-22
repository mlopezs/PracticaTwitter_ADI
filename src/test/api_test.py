#!/usr/bin/python2

from App import app

import os
import json
import unittest
import tempfile

from hamcrest import *

class RESTTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['Testing'] = True

        self.tester.post('/no_collect')

    def tearDown(self):
        del self.tester

    def test_index(self):
        return self.tester.get('/')

    def test_operations(self):
        return self.tester.get('/operations')

    def test_collect(self):
        return self.tester.post('/collect')

    def test_collect_error(self):
        return self.tester.post('/collect')

    def test_stop_collect(self):
        return self.tester.post('/no_collect')

    def test_stop_collect_error(self):
        return self.tester.post('/no_collect')

    def test_words(self):
        return self.tester.post('/list_word', json={'tweet_word' : 'algo'})

    def test_likes(self):
        return self.tester.post('/show_likes', json={'tweet_likes' : 'algo'})

    def test_retweets(self):
        return self.tester.post('/show_rts', json={'tweet_retweets' : 'algo'})