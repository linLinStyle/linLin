#encoding: utf-8
#create_time: 2019/7/10 12:26
from functools import wraps
from flask import session,url_for,redirect
import config

def Login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        return func(*args,**kwargs) if config.FRONT_USER_ID in session else redirect(url_for('front.signin'))
    return inner