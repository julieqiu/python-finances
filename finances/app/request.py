from flask import request


def json():
    """Proxy for flask.request.json. Request must include 'Content-Type: application/json' otherwise
    this function returns None. http://flask.pocoo.org/docs/0.12/api/#flask.Request.json"""
    return request.json


