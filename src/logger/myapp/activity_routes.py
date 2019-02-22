#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from datetime import date, datetime
from google.appengine.ext import ndb
from flask import Blueprint, jsonify, abort, make_response, request

from myapp.models import Activity

bp_activity = Blueprint("bp_activity", __name__)
@bp_activity.route('/activity', methods = ['GET'])
def getActivities():
    listActivity = []
    for it in Activity.query():
        listActivity.append(it.to_dict())
    return make_response(jsonify({"activities":listActivity}), 200)

@bp_activity.route('/activity', methods = ['POST'])
def addActivity():

    newActivity = Activity(
        operation = request.json['operation']
    )
    
    try:
        keyActivity = newActivity.put()
        response = make_response(jsonify({"created":keyActivity.id()}), 200)
    except:
        abort(409)
    
    return response