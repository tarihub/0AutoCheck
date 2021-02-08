# encoding:utf-8
import os

# **************** 必配选项 ****************
# 零组登录帐号
ZERO_USER = os.environ['ZERO_USER'].strip()
# 零组登录密码
ZERO_PASSWD = os.environ['ZERO_PASSWD'].strip()
# 第三方图形验证码识别 api key
API_KEY = os.environ['API_KEY'].strip()
# 第三方图形验证码识别 api secret
API_SECRET = os.environ['API_SECRET'].strip()
# **************** 必配选项 ****************

# 第三方验证码识别 api
CAPTCHA_API = {
    'ttshitu_base64_api': {
        'captcha_fail_cnt': 10,
    },
    'baidu_base64_api': {
        'captcha_fail_cnt': 100
    }
}

# 默认百度云 api
CAPTCHA_HANDLE = (os.environ.get('CAPTCHA_API', 0) or 'baidu_base64_api').strip()

# 验证码验证失败重试次数
CAPTCHA_FAIL_CNT = CAPTCHA_API[CAPTCHA_HANDLE]['captcha_fail_cnt']

# HTTP 请求头
HTTP_HEADER = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Content-Type': 'application/json;charset=UTF-8', 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# 验证码位数
CAPTCHA_CHECK = 4

# DEBUG 模式
DEBUG = True
