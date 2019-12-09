#encoding: utf-8
from functools import wraps
from flask import session,redirect,url_for,g
import config

def Login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        return func(*args,**kwargs) if config.CMS_USER_ID in session else redirect(url_for('cms.login'))
    return inner

def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter