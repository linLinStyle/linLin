#encoding: utf-8
#create_time: 2019/7/12 17:47
from celery import Celery
from flask_mail import Message
from exts import mail
from flask import Flask
import config
import requests

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task
def send_mail(subject,recipients,body):
    message = Message(subject=subject,recipients=recipients,body=body)
    mail.send(message)

@celery.task
def send_sms_captcha(telephone,captcha):
    url = 'http://v.juhe.cn/sms/send'
    parms = {
        'mobile': telephone,
        'tpl_id': '170963',
        'tpl_value':'#code#='+str(captcha),
        'key': 'bf47384a6bac33a970136738c5e7caea'
    }
    result = requests.get(url,params=parms).json()
    print(result)
    return True if result['error_code'] == 0 else False

#运行代码：celery -A tasks.celery worker --pool=solo --loglevel=info