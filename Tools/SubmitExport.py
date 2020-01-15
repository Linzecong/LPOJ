# coding=utf-8

import MySQLdb
from queue import Queue
import socket
import json
from time import sleep
import threading
import os
import json

queue = Queue() # 全局判题列表
myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

if os.environ.get("DB_USER"):
    judgerjson["db_ip"] = os.environ.get("DB_HOST")
    judgerjson["db_pass"] = os.environ.get("DB_PASSWORD")
    judgerjson["db_user"] = os.environ.get("DB_USER")
    judgerjson["db_port"] = os.environ.get("DB_PORT")

try:
    db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                         judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')
except Exception as e:
    print(e)
    exit(1)


cursor = db.cursor()


datajsonfile = open("./data.json", 'r',encoding="utf-8")
datas = json.loads(datajsonfile.read(),encoding="utf-8")

username = {}

userdata = {}

num = 0
for data in datas:
    if data["contest"] != 1:
        continue
    if username.get(data["user"],None)==None:

        cursor.execute("SELECT * from user_user where username=%s",(data["user"],))
        name = cursor.fetchone()[2]
        username[data["user"]] = name

    user = data["user"]
    name = username[data["user"]]

    if userdata.get(user,None)==None:
        #print(user)
        if user.find("@")<0:
            print(name)

        userdata[user] = {
            "email":user,
            "name":name,
            "memory":0,
            "time":0,
            "code":"",
            "submitnum":0,
            "judgetime":"2018-01-01 00:00:00.000000",
            "result":"no",
            "testcase":"",
            "acnum":0,
            "firstactime":"2018-01-01 00:00:00.000000"
        }
    
    result = data["result"]
    code = data["code"]
    memory = data["memory"]
    time = data["time"]
    judgetime = data["submittime"]
    testcase = data["testcase"]

    userdata[user]["submitnum"] = userdata[user]["submitnum"] + 1

    if result == 0:
        userdata[user]["acnum"] = userdata[user]["acnum"] + 1
        if userdata[user]["firstactime"] == "2018-01-01 00:00:00.000000":
            userdata[user]["firstactime"] = judgetime
        
        if userdata[user]["firstactime"] > judgetime:
            userdata[user]["firstactime"] = judgetime

        if judgetime > userdata[user]["judgetime"]:
            userdata[user]["result"] = "yes"
            userdata[user]["memory"] = memory
            userdata[user]["time"] = time
            userdata[user]["code"] = code
            userdata[user]["judgetime"] = judgetime
            userdata[user]["testcase"] = "0"
    else:
        if userdata[user]["result"] == "yes":
            continue
        else:
            if judgetime > userdata[user]["judgetime"]:
                userdata[user]["result"] = "no"
                userdata[user]["memory"] = memory
                userdata[user]["time"] = time
                userdata[user]["code"] = code
                userdata[user]["judgetime"] = judgetime
                userdata[user]["testcase"] = testcase



for k,v in userdata.items():
    ccc = v["code"]
    v["code"] = "PyMacroParser.py"
    j = json.dumps(v)

    try:
        os.makedirs("./new/"+v["name"])
    except FileExistsError:
        os.makedirs("./new/"+v["name"]+"2")
        v["name"] = v["name"]+"2"


    f = open("./new/"+v["name"]+"/data.json","w",encoding="utf-8")
    f.write(j)
    f.close()

    f = open("./new/"+v["name"]+"/PyMacroParser.py","w",encoding="utf-8")
    f.write(ccc)
    f.close()



print(num)

