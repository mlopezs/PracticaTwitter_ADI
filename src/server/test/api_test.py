#!/usr/bin/python2.7
import Server

import os
import json
import unittest
import tempfile
import time

from hamcrest import *

class RESTTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = Server.app.test_client(self)
        Server.app.config['Testing'] = True
        self.tester.post('/no_collect')

    def tearDown(self):
        del self.tester

    def test_collect(self):
        response = self.tester.post('/collect')
        self.assertEqual(response.status_code, 200)

    def test_collect_error(self):
        self.tester.post('/collect')
        response = self.tester.post('/collect')
        self.assertNotEqual(response.status_code, 200)

    def test_stop_collect(self):
        self.tester.post('/collect')
        response = self.tester.post('/no_collect')
        self.assertEqual(response.status_code, 200)

    def test_stop_collect_error(self):
        self.tester.post('/no_collect')
        response = self.tester.post('/no_collect')
        self.assertNotEqual(response.status_code, 200)

    def test_words_error(self):
        response = self.tester.post('/list_word')
        self.assertEqual(response.status_code, 400)

    def test_words(self):
        response = self.tester.post('/list_word', json={'tweet_word' : 'if'})
        self.assertEqual(response.status_code, 200)

    def test_likes_failure(self):
        response = self.tester.post('/show_likes')
        self.assertEqual(response.status_code, 400)

    def test_likes(self):
        response =  self.tester.post('/show_likes', json={'tweet_likes' : 2})
        self.assertEqual(response.status_code, 200)

    def test_retweets_failure(self):
        response = self.tester.post('/show_rts')
        self.assertEqual(response.status_code, 400)

    def test_retweets(self):
        response =  self.tester.post('/show_rts', json={'tweet_retweets' : 2})
        self.assertEqual(response.status_code, 200)

    def test_webhook_error_no_endpoint(self):
        response = self.tester.post('/webhook')
        self.assertEqual(response.status_code, 400)

    def test_webhook(self):
        response = self.tester.post('/webhook', json={'endpoint' : 'http://google.es'})
        self.assertEqual(response.status_code, 201)

    def test_webhook_error_duplicated_endpoint(self):
        self.tester.post('/webhook', json={'endpoint' : 'http://google.es'})
        response = self.tester.post('/webhook', json={'endpoint' : 'http://google.es'})
        self.assertEqual(response.status_code, 409)
