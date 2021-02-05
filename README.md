# AutoCheck

## 简陋的使用方法

先 Fork 一份到自己仓库，然后在 Settings -> Secrets 添加零组的登录帐号密码以及验证码识别API
> 注意: 名字不能乱取，放心，这个别人是无法看到的
+ ZERO_USER: 零组的登录帐号
+ ZERO_PASSWD: 零组的登录密码
+ API_KEY: 第三方验证码识别API，内测期间找我要即可
+ API_SECRET: 第三方验证码识别API，内测期间找我要即可

添加完如下图
![img.png](./doc/img.png)

然后修改本文件（README.md），加个空格，啥都行，提交就会自动执行了。