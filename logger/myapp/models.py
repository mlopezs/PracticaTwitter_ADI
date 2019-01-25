#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import url_for
from google.appengine.ext import ndb

class Activity(ndb.Model):
    operation = ndb.StringProperty(required=True)
    date_ope = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def getAll(self):
        auxActList = []
        for itAct in Activity.query():
            auxActList.append(itAct.to_dict())
        return auxActList