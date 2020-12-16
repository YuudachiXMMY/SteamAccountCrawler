import sys
sys.path.append(r'E:\anaconda\Lib\site-packages')
import requests
import time
import rsa
import base64
import execjs
from Crypto.Cipher import PKCS1_v1_5
import ssl
import time

get_rsakey_url = 'https://store.steampowered.com/login/getrsakey/'
login_url = 'https://store.steampowered.com/login/dologin/'
login_headers = {
    'Referer':'https://store.steampowered.com/login/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

req = requests.session()
sign_dict = {'account_incorrect_sign':1,'guard_fail_sign':1}


def get_login_rsakey():
    #第一次输入账号密码错误后，会被置0，应该在开始置1
    sign_dict['guard_fail_sign'] = 1

    username = input('input your steam account number:')
    password = input('input your steam account password:')

    if username == '' or username == 'q' or password == '' or password == 'q':
        return None

    data = {
    'donotcache':str(int(time.time()*1000)),
    'username':username
    }
    getkey_html = req.post(get_rsakey_url,data=data,headers=login_headers).json()
    pub_mod = getkey_html.get('publickey_mod')
    pub_exp = getkey_html.get('publickey_exp')
    timestamp = getkey_html.get('timestamp')
    #加密密码    RSA
    with open('rsa.js',encoding='utf-8') as f:
        jsdata = f.read()
    password_encrypt = execjs.compile(jsdata).call('getpwd',password,pub_mod,pub_exp)
    return username,password_encrypt,timestamp

def login_request(_data_):
    login_data = {'donotcache':str(int(time.time()*1000)),
        'username':_data_[0],
        'password':_data_[1],
        'twofactorcode':'',
        'emailauth':'',
        'loginfriendlyname':'',
        'captchagid':'-1',
        'captcha_text':'',
        'emailsteamid':'',
        'rsatimestamp':_data_[2],
        'remember_login':'false',
        }

    response_data = req.post(login_url,data=login_data,headers=login_headers).json()
    print('\nlogin_html\n',response_data)
    return response_data,login_data

def input_guard_number(_data_):
    html_data = _data_[0]
    login_data = _data_[1]
    #没有手机令牌的账号，在输入过邮箱令牌一次后可以直接登录
    if (html_data.get('success') == True) and (html_data.get('login_complete') == True):
        sign_dict['guard_fail_sign'] = 0
        sign_dict['account_incorrect_sign']= 0
        return html_data
    #没有手机令牌，第一次登录需要邮箱验证码
    elif html_data.get('emailauth_needed') == True:
        email_guard_number = input('input the email guard number:')
        login_data['twofactorcode'] = email_guard_number
        sign_dict['account_incorrect_sign']= 0
        return req.post(login_url, data=login_data, headers=login_headers).json()
    #输入手机令牌
    elif (html_data.get('success') == False) and (html_data.get('message') == ''):
        phone_guard_number = input('input the phone guard number:')
        login_data['twofactorcode'] = phone_guard_number
        sign_dict['account_incorrect_sign']= 0
        return req.post(login_url, data=login_data, headers=login_headers).json()
    #输入账号密码错误
    elif (html_data.get('success') == False) and (html_data.get('message') == 'The account name or password that you have entered is incorrect.'):
        sign_dict['guard_fail_sign'] = 0
        print('\n***** Incorrect input !!! Please try again :( *****\n')

#判断是否登录成功
def if_login_successful(login_with_guard_html):
    if login_with_guard_html != None:
        if (login_with_guard_html.get('success') == True) and (login_with_guard_html.get('login_complete') == True):
            sign_dict['guard_fail_sign'] = 0
            print('\nsuccessfully login')

if __name__ == '__main__':
    #账号密码错误，重新输入账号密码
    while(bool(sign_dict['account_incorrect_sign'])):
        data = get_login_rsakey()
        if data == None:
            print("***** Program Manually ended !!! *****")
            break
        data2 = login_request(data)
        #令牌输入错误，重新输入令牌
        while(bool(sign_dict['guard_fail_sign'])):
            html_data = input_guard_number(data2)
            if_login_successful(html_data)