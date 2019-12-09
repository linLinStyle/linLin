#encoding: utf-8
from flask import Blueprint,request,make_response,jsonify
from utils import smssender,zlcache
from utils import restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO
import qiniu
from tasks import send_sms_captcha

bp = Blueprint('common',__name__,url_prefix='/c')

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    print('本次的图形验证码是：%s' %text)
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

# @bp.route('/sms_captcha/')
# def sms_captcha():
    # telephone = request.args.get('telephone')
    # if  not telephone:
    #     return restful.params_error(message='请输入手机号码！')
    # captcha = Captcha.gene_text(4)
    # return restful.success() if smssender.send(telephone,captcha) else restful.success()
@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(4)
        if send_sms_captcha(telephone, captcha):
            zlcache.set(telephone,captcha)
            print('本次的手机验证码是:%s' %captcha)
            return restful.success()
        else:
            zlcache.set(telephone, captcha)
            return restful.params_error(message='参数错误')
    else:
        return restful.params_error(message='参数错误')


@bp.route('/uptoken/')
def uptoken():
    accesskey = 'EUVg-zs_7FR80B_VZjDMzap4XZ5HnhxM5aVmStBm'
    secretkey = '9pHwUSb3D00qE49GZpL4pEoqe6Llaape-miqjA51'
    q = qiniu.Auth(accesskey,secretkey)
    bucket = 'linlinstyle'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})