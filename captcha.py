# coding: utf-8
import json
import time
import requests

import config


def ttshitu_base64_api(_base64_image):
    # 你的验证码api账户
    data = {"username": config.API_KEY, "password": config.API_SECRET, "image": _base64_image}
    for try_cnt in range(config.CAPTCHA_FAIL_CNT):
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        try:
            print(result)
            return result["data"]["result"]
        except NameError:
            print("验证码识别抽风了, 重试第" + str(try_cnt) + "ing...")
            time.sleep(1.5)
            if try_cnt > 10:
                raise Exception('重试了' + str(try_cnt) + '次, 验证码识别真的抽风了, 退出...')
            continue


def baidu_base64_api(_base64_image):
    pass


if config.CAPTCHA_HANDLE not in config.CAPTCHA_API.keys():
    print('目前只支持以下几种验证码识别API: ')
    for support_api in config.CAPTCHA_API.keys():
        print(support_api)
    raise Exception('不支持的验证码识别API')

captcha_handle = eval(config.CAPTCHA_HANDLE)
