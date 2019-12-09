#encoding: utf-8
#create_time: 2019/7/7 15:14
from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp,InputRequired
import hashlib

class SMSCaptchaForm(BaseForm):
    salt = 'egufwdsgdscdsuhduh$'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestramp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestramp = self.timestramp.data
        sign = self.sign.data

        #md5(timestramp+telephone+salt)
        #md5函数必须传入一个byte类型的字符串进去
        sign2 = hashlib.md5((timestramp+telephone+self.salt).encode('utf-8')).hexdigest()
        return True if sign == sign2 else False