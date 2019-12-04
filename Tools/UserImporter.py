# coding=utf-8
import requests
from time import sleep
import sys
import hashlib
# 暂时做成txt中导入，后面再加入从表格中读取

def insertUser(username, password, name, school="unknow", course="unknow", classes="unknow", number="unknow", realname="unknow", qq="unknow", email="unknow", type=1):
    
    # 待加密信息
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf-8'))
    password = hl.hexdigest()
    print(password)

    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        'User-Agent': userAgent,
    }

    mafengwoSession = requests.session()

    password2 = '123456'
    # 创建md5对象
    h2 = hashlib.md5()
    h2.update(password2.encode(encoding='utf-8'))
    password2 = h2.hexdigest()

    loginUrl = "https://www.lpoj.cn/api/login" # 登录 url
    loginData = {
        "username": "admin", # 管理员用户名和密码
        "password": password2,
    }
    responseRes = mafengwoSession.post(
        loginUrl, data=loginData, headers=header, allow_redirects=True)
    print(responseRes.text)

    postUrl = "https://www.lpoj.cn/api/register" # 注册 url
    postData = {
        "username": username, 
        "password": password,
        "name" :name,
        "school" : school,
        "course" : course,
        "classes" : classes,
        "number" : number,
        "realname" : realname,
        "qq" : qq,
        "email" :email,
        "type" :1
    }
    responseRes = mafengwoSession.post(postUrl, data=postData, headers=header)
    print(responseRes.text)

if __name__ == "__main__":
    file = open(sys.argv[1],"r",encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        items = line.split(" ")
        print(items)
        insertUser(items[0], items[1], items[2])
        sleep(0.3)
