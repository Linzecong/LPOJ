# coding=utf-8

import MySQLdb
import socket
import json
import time
import os
from time import sleep
import datetime

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

try:
    db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                         judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')
except Exception as e:
    print(e)
    exit(1)


source_conntest = 100 # 比赛ID
des_conntest = 101 # 复制到哪个比赛

cursor = db.cursor()
cursor.execute("SELECT * from judgestatus_judgestatus where contest = %d "%source_conntest) # contest

datas = cursor.fetchall()

for data in datas:
    
    id = data[0]
    username = data[1]
    cursor.execute("SELECT * from user_user where username=%s",(username,))
    name = cursor.fetchone()[2]

    rank = ord(data[16]) - 65
    contestid = des_conntest

    result = data[4]
    type = -1
    if result == 0:
        type = 1
    elif type != -4 and type != -1 and type != -6 and type != -2 and type != 5:
        type = 0


    subtime = data[9]
    
    subtime = int(subtime.timestamp() * 1000)

    print(contestid,username,name,rank,type,subtime,id,1500) # contest


    #cursor.execute("INSERT INTO contest_contestboard(contestid,username,user,problemrank,type,submittime,submitid,rating) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(contestid,username,name,rank,type,subtime,id,1500))
    #                   (username, totleac, today, username, today))


#db.commit()