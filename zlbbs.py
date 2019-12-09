from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db,mail
from flask_wtf import CSRFProtect
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app

app = create_app()

@app.template_filter('handle_time')
def handles_time(time):
    if isinstance(time,datetime):
        now = datetime.now()
        timetemp = (now - time).total_seconds()
        if timetemp < 60:
            return '刚刚'
        elif timetemp >= 60 and timetemp < 60*60:
            minutes = timetemp / 60
            return '%d分钟之前'%int(minutes)
        elif timetemp >= 60*60 and timetemp < 60*60*24:
            hours = timetemp / (60*60)
            return '%d小时前'%int(hours)
        elif timetemp >= 60*60*24 and timetemp < 60*60*24*30:
            days = timetemp / (60*60*24)
            return '%d天前'%int(days)
        elif timetemp > 60*60*24*30 and timetemp < 60*60*24*30*12:
            mouths = timetemp / (60*60*24*30)
            return '%d月前'%int(mouths)
        else:
            return time.strftime('%Y/%m/%d %H:%M')
    else:
        return time

if __name__ == '__main__':
    app.run(port=8000)
