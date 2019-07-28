# coding: utf-8
import os


class Config(object):
    DD = 0
    RESULT_ERROR = 0
    RESULT_SUCCESS = 1
    JSON_AS_ASCII = False

    SITE_ROOT = "http://task.cocotask.com/"

    # TODO 这里下面的所有配置都要全部大写，不然识别不到，不知道为什么，有待查找一下原因
    # 小程序设置信息-比你兽
    MP_APPID = "wxd6aefbe7d94175f6"
    MP_SECRET = "bc7544bc72cae20dbef7d10be14b2e77"

    # 小程序设置信息-小精灵
    MP_APPID_EFL = "wx1b9b0e6f51b9c14e"
    MP_SECRET_EFL = "775e312fc8f20fde338b1b81511207a5"

    # 商户号信息
    MP_MCH_ID = "1533695991"
    # 这里不能用 https 地址，吃了大亏
    HTTP_ROOT = "http://swu.mynatapp.cc"
    MP_MCH_KEY = "c9a5241f1d9b1a21659f75cb0e3d82ba"

    # 微信设置信息
    WECHAT_APPID = "wxf36645bdd574084f"
    WECHAT_SECRET = "8686910394a9cc112d9cf89ccfc6c8dc"
    WECHAT_MCH_ID = "1525943361"
    WECHAT_MCH_KEY = "c9a5241f1d9b1a21659f75cb0e3d82ba"
    WECHAT_AUTH_URL = "http://task.cocotask.com/wechat/authorized"
    WECHAT_ROOT = "http://task.cocotask.com/wechat"  # 微信根目录，结尾不带"/"

    MONGODB_SETTINGS = {'ALIAS': 'default',
                        'DB': 'xcc_binishou',
                        'host': 'localhost',
                        'username': 'admin',
                        'password': ''}

    """Base config class."""
    # Flask app config
    DEBUG = True
    TESTING = True
    # secret_key 实际上是用来加密字符串的, 如果在实例化的app中没有secret_key那么开启session一定会抛异常的
    # 他是用来给 session 加密解密用的,因为flask的session会将你的SessionID存放在客户端的Cookie中
    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    SITE_TITLE = "Cocotask管理平台"
    SITE_DOMAIN = "https://swu.mynatapp.cc"

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'izt'
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_POST_CHANGE_VIEW = '/admin'
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    SECURITY_CHANGEABLE = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_MSG_DISABLED_ACCOUNT = ('账号已被禁用', 'error')
    SECURITY_MSG_INVALID_PASSWORD = ('密码错误', 'error')
    SECURITY_MSG_INVALID_REDIRECT = ('转向错误', 'error')
    SECURITY_MSG_LOGIN = ('请登录', 'error')
    SECURITY_MSG_LOGIN_EXPIRED = ('登录超时', 'error')
    SECURITY_MSG_PASSWORDLESS_LOGIN_SUCCESSFUL = ('无密码登录成功', 'error')
    SECURITY_MSG_PASSWORD_CHANGE = ('密码修改', 'error')
    SECURITY_MSG_PASSWORD_INVALID_LENGTH = ('密码不能少于6位', 'error')
    SECURITY_MSG_PASSWORD_IS_THE_SAME = ('密码和原密码相同', 'error')
    SECURITY_MSG_PASSWORD_MISMATCH = ('输入密码不匹配', 'error')
    SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('密码不能为空', 'error')
    SECURITY_MSG_PASSWORD_NOT_SET = ('密码没有设置', 'error')
    SECURITY_MSG_PASSWORD_RESET = ('密码重置', 'error')
    SECURITY_MSG_PASSWORD_RESET_EXPIRED = ('密码重置过期', 'error')
    SECURITY_MSG_PASSWORD_RESET_REQUEST = ('密码重置请求', 'error')
    SECURITY_MSG_REFRESH = ('刷新', 'error')
    SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ('两次输入密码不匹配', 'error')
    SECURITY_MSG_UNAUTHORIZED = ('未授权', 'error')
    SECURITY_MSG_USER_DOES_NOT_EXIST = ('用户不存在', 'error')

    ROLES = {'SuperAdmin': '超级管理员',
             'CompanyAdmin': '公司管理员'
             }
