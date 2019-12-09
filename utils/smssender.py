#encoding: utf-8
#create_time: 2019/7/7 12:07
import requests

def send(mobile,captcha):
    url = 'http://v.juhe.cn/sms/send'
    params = {
        'mobile': mobile,
        'tpl_id': '170963',
        'tpl_value':'#code#='+str(captcha),
        'key': 'bf47384a6bac33a970136738c5e7caea'
    }
    result = requests.get(url,params=params).json()
    print(result)
    return True if result['error_code'] == 0 else False