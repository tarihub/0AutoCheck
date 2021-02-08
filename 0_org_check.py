# coding: utf-8

import json
import requests

import config
import captcha


def get_code_info():
    # 获取image、UUID值
    code_url = "https://wiki.0-sec.org/api/user/captchaImage"
    code_image = requests.get(code_url)
    json_data = json.loads(code_image.content)

    return json_data['data']['uuid'], json_data['data']['img']


def login(_uuid, _base64_image):
    url = "https://wiki.0-sec.org/api/user/login"
    login_data = {
        "account": config.ZERO_USER, "password": config.ZERO_PASSWD,
        "code": captcha.captcha_handle(_base64_image), "uuid": _uuid
    }
    data_json = json.dumps(login_data)
    logins = requests.post(url=url, headers=config.HTTP_HEADER, data=data_json)
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
    check_input(config.ZERO_USER, config.ZERO_PASSWD, config.API_KEY, config.API_SECRET)
    uuid, base64_image = get_code_info()
    tokens = login(uuid, base64_image)
    sign(tokens)
