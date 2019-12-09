#encoding: utf-8
from flask import jsonify

class HttoCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500

def restful_result(code,message,data):
    return jsonify({'code':code,'message':message,'data':data or {}})

def success(message='',data=None):
    return restful_result(code=HttoCode.ok,message=message,data=data)

def unauth_error(message=''):
    return restful_result(code=HttoCode.unautherror,message=message,data=None)

def params_error(message=''):
    return restful_result(code=HttoCode.paramserror,message=message,data=None)

def server_error(message=''):
    return restful_result(code=HttoCode.servererror,message=message,data=None)