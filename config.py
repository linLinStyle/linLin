#encoding: utf-8
import os

DEBUG = True
SECRET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlbbs'
USERNAME = 'root'
PASSWORD = 'root'
#dialect+driver://username:password@host:port/database(固定组合)
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'dsffred'
FRONT_USER_ID = 'fedrsfred'

#发送者邮箱的服务器地址
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL = False
MAIL_USERNAME = '1265677435@qq.com'
MAIL_PASSWORD = 'viudnfsgeyeqjfhf'
MAIL_DEFAULT_SENDER = '1265677435@qq.com'
#ublatcjhebzhhafe
#viudnfsgeyeqjfhf
#MAIL_USE_TLS:587
#MAIL_USE_SSL:465
#qq邮箱不支持非加密方式发送邮件

UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "EUVg-zs_7FR80B_VZjDMzap4XZ5HnhxM5aVmStBm"
UEDITOR_QINIU_SECRET_KEY = "9pHwUSb3D00qE49GZpL4pEoqe6Llaape-miqjA51"
UEDITOR_QINIU_BUCKET_NAME = "linlinstyle"
UEDITOR_QINIU_DOMAIN = "http://pud1g0cic.bkt.clouddn.com/"

PER_PACE = 10

#celery相关配置
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'