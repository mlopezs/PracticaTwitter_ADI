#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import Flask, make_response, jsonify


# Por defecto el root es $PREFIX/var/myapp-instance
app=Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('../instance/development.cfg')

from myapp.activity_routes import bp_activity

app.register_blueprint(bp_activity)

# Este podría ir en otro Blueprint
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

