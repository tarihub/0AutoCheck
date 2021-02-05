import argparse

parser = argparse.ArgumentParser(description='零组签到')
parser.add_argument('-u', '--z_uname', help='零组文库登录帐号')
# parser.add_argument('-o', '--z_passwd', help='零组文库登录密码')

args = parser.parse_args()
print(args.z_uname)
parser.print_help()
