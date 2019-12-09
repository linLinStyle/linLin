#encoding: utf-8
#create_time: 2019/7/8 9:57
from urllib.parse import urljoin,urlparse
from flask import request

def is_safe_url(target):
    ref_url = urlparse((request.host_url))
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc