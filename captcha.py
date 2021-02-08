# encoding:utf-8
import json
import requests

import config


def ttshitu_base64_api(_base64_image):
    data = {"username": config.API_KEY, "password": config.API_SECRET, "image": _base64_image}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if config.DEBUG:
        print('****** ttshitu API ****** ')
        print(result)
    return result["data"]["result"]


def baidu_base64_api(_base64_image):
    baidu_api_token_req = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
                     'client_id={}&client_secret={}'.format(config.API_KEY, config.API_SECRET)
    res_token = requests.get(baidu_api_token_req)
    if not res_token:
        print(res_token)
        raise Exception('无法通过 API_KEY 和 API_SECRET 获取百度API token')
    access_token = res_token.json()['access_token']

    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + str(access_token)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": _base64_image}

    res = requests.post(url, data=params, headers=headers).json()
    if config.DEBUG:
        print('****** baidu API ****** ')
        print(res)

    return str(res['words_result'][0]['words']).strip().replace(' ', '')


if config.CAPTCHA_HANDLE not in config.CAPTCHA_API.keys():
    print('目前只支持以下几种验证码识别API: ')
    for support_api in config.CAPTCHA_API.keys():
        print(support_api)
    raise Exception('不支持的验证码识别API')

captcha_handle = eval(config.CAPTCHA_HANDLE)
