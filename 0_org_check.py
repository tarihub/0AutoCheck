# coding:utf-8

import os
import json
import requests

# 零组登录帐号
ZERO_USER = os.environ['ZERO_USER']
# 零组登录密码
ZERO_PASSWD = os.environ['ZERO_PASSWD']
# 第三方图形验证码识别 api key
API_KEY = os.environ['API_KEY']
# 第三方图形验证码识别 api secret
API_SECRET = os.environ['API_SECRET']


def get_code_uuid():
    # 获取image、UUID值
    code_url = "https://wiki.0-sec.org/api/user/captchaImage"
    code_image = requests.get(code_url)
    json_data = json.loads(code_image.content)

    return json_data['data']['uuid'], json_data['data']['img']


def base64_api(_base64_image):
    # 你的验证码api账户
    data = {"username": API_KEY, "password": API_SECRET, "image": _base64_image}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    print(result)
    if result['success']:
        return result["data"]["result"]
    else:
        raise Exception("验证码识别抽风了，再执行一遍吧")


def login(_uuid, _base64_image):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    url = "https://wiki.0-sec.org/api/user/login"
    login_data = {"account": ZERO_USER, "password": ZERO_PASSWD, "code": base64_api(_base64_image), "uuid": _uuid}
    data_json = json.dumps(login_data)
    logins = requests.post(url=url, headers=headers, data=data_json)
    # token
    return json.loads(logins.content)['data']['token']


def sign(token):
    headers = {'Zero-Token': token}
    url = "https://wiki.0-sec.org/api/profile"
    old_sign_data_json = requests.get(url=url, headers=headers)
    old_sign_data_credit = json.loads(old_sign_data_json.content)['data']['credit']

    url1 = "https://wiki.0-sec.org/api/front/user/sign"
    requests.post(url=url1, headers=headers)

    new_sign_data_json = requests.get(url=url, headers=headers)
    new_sign_data_credit = json.loads(new_sign_data_json.content)['data']['credit']

    if new_sign_data_credit > old_sign_data_credit:
        print("签到成功，您的当前积分为：", new_sign_data_credit)
    else:
        print("兄弟，你已经签到过了，你的积分为：", new_sign_data_credit)


def check_input(*args):
    for v in args:
        if len(v) > 64:
            raise Exception('帐号密码密钥太长啦...')


if __name__ == '__main__':
    check_input(ZERO_USER, ZERO_PASSWD, API_KEY, API_SECRET)
    uuid, base64_image = get_code_uuid()
    tokens = login(uuid, base64_image)
    sign(tokens)
