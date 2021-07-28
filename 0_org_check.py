# encoding:utf-8

import json
import time
import requests

import config
import captcha


def get_code_info():
    for try_cnt in range(config.CAPTCHA_FAIL_CNT):
        # 获取image、UUID值
        code_url = "https://wiki.0-sec.org/api/user/captchaImage"
        code_image = requests.get(code_url)
        json_data = json.loads(code_image.content)

        try:
            # 默认已是 base64 编码，不需要转换
            cap_code = captcha.captcha_handle(json_data['data']['img'])
        except (IndexError, NameError, TypeError):
            cap_code = ''

        if len(cap_code) == config.CAPTCHA_CHECK:
            return json_data['data']['uuid'], cap_code

        print("验证码识别抽风了, 重试第 " + str(try_cnt) + " 次ing...")
        time.sleep(1.5)
        continue
    sign_error('重试了' + str(config.CAPTCHA_FAIL_CNT) + '次, 验证码识别真的抽风了, 退出...')


def login(_captcha_uuid, _captcha_code):
    url = "https://wiki.0-sec.org/api/user/login"
    for _ in range(config.CAPTCHA_FAIL_CNT):
        login_data = {
            "account": config.ZERO_USER, "password": config.ZERO_PASSWD,
            "code": _captcha_code, "uuid": _captcha_uuid
        }
        data_json = json.dumps(login_data)
        logins = requests.post(url=url, headers=config.HTTP_HEADER, data=data_json)
        try:
            # token
            return json.loads(logins.content)['data']['token']
        except TypeError:
            _captcha_uuid, _captcha_code = get_code_info()
            continue

    sign_error('在检查一下下帐号密码有没有错喔, 没有的话可以试试 Re-run-jobs，如果还不行就是验证码识别抽风了...免费的是有极限的 (')


# PushPlus Push 消息推送
def push_plus_push(token, sign_info):
    text = "{}".format(sign_info)
    url = "https://www.pushplus.plus/send?token={0}&title={1}&content={2}&template={3}".format(
        token, "零组文库签到", text, "html"
    )

    try:
        ret = requests.get(url)
        print("pushplus: " + ret.text)
    except Exception:
        print('pushplus 推送接口访问异常, 请检查接口可达性或token是否正常')


def sign(token):
    headers = {'Zero-Token': token}
    url = "https://wiki.0-sec.org/api/profile"
    old_sign_data_json = requests.get(url=url, headers=headers)
    old_sign_data_credit = json.loads(old_sign_data_json.content)['data']['credit']

    url1 = "https://wiki.0-sec.org/api/front/user/sign"
    requests.post(url=url1, headers=headers)

    new_sign_data_json = requests.get(url=url, headers=headers)
    new_sign_data_credit = json.loads(new_sign_data_json.content)['data']['credit']

    # 消息推送
    if len(config.PLUSPUSH) != 0:
        push_plus_push(config.PLUSPUSH, '签到成功, 当前积分为: ' + str(new_sign_data_credit))

    if new_sign_data_credit > old_sign_data_credit:
        print("签到成功，当前积分为：", new_sign_data_credit)
    else:
        print("兄弟，你已经签到过了，你的积分为：", new_sign_data_credit)


def check_input(*args):
    for v in args:
        if len(v) == 0:
            sign_error('请检查 ZERO_USER ZERO_PASSWD API_KEY API_SECRET 四个字段是否存在')
        if len(v) > 128:
            sign_error('帐号密码密钥太长啦...')


def sign_error(error_text):
    # 这里写死常量, 防止不小心信息泄漏
    push_plus_push(config.PLUSPUSH, '签到失败, 请到 Github Action 查看详细原因')
    raise Exception(error_text)


if __name__ == '__main__':
    check_input(config.ZERO_USER, config.ZERO_PASSWD, config.API_KEY, config.API_SECRET)
    captcha_uuid, captcha_code = get_code_info()
    tokens = login(captcha_uuid, captcha_code)
    sign(tokens)
