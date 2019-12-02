# coding=utf-8

import MySQLdb
import socket
import json
import time
import feedparser
import os
from time import sleep
from Codeforces import get_CF_data
from CodeforcesRate import get_CF_Rate
from HDU import get_HDU_data
from Vjudge import get_VJ_data
from LPOJ import get_LPOJ_data
from urllib import request
import datetime


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

while True:
    # AC num
    cursor = db.cursor()
    cursor.execute("SELECT * from board_board")
    datas = cursor.fetchall()
    for data in datas:
        username = str(data[0])
        accounts = str(data[5]).split("|")
        print(username)

        while True:
            CF = get_CF_data(accounts[0])
            print(accounts[0], "CF:", CF)
            if CF[0] != -1:
                break
        
        
        CFRate = get_CF_Rate(accounts[0])
        print(accounts[0], "CFRate:", CFRate)
        if CFRate == -1:
            CFRate = 0
        
        while True:
            HDU = get_HDU_data(accounts[1])
            print(accounts[1], "HDU:", HDU)
            if HDU[0] != -1:
                break

        while True:
            VJ = get_VJ_data(accounts[2])
            print(accounts[2], "VJ:", VJ)
            if VJ[0] != -1:
                break
        
        while True:
            LPOJ = get_LPOJ_data(accounts[3])
            print(accounts[3], "LPOJ:", LPOJ)
            if LPOJ[0] != -1:
                break

        Others = [int(str(data[6]).split("|")[-1]),
                  int(str(data[7]).split("|")[-1])]  # 其他OJ

        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        totleac = CF[0] + HDU[0] + VJ[0] + LPOJ[0] + Others[0]

        cursor.execute("INSERT INTO board_dailyboard(username,account,collecttime,cfrate) SELECT '%s', %d, '%s',%d FROM DUAL WHERE NOT EXISTS(SELECT * FROM board_dailyboard WHERE username = '%s' and collecttime= '%s')" %
                            (username, totleac, today,int(CFRate), username, today))


        ac = str(CF[0]) + "|" + str(HDU[0]) + "|" + str(VJ[0]) + \
            "|" + str(LPOJ[0]) + "|" + str(Others[0])
        submit = str(CF[1]) + "|" + str(HDU[1]) + "|" + \
            str(VJ[1]) + "|" + str(LPOJ[1]) + "|" + str(Others[1])
        cursor.execute("UPDATE board_board SET acnum = '%s' ,submitnum = '%s',cfrate='%s'  WHERE username = '%s'" % (
            ac, submit,CFRate, username))
        db.commit()
        print(username, ac, submit)

    # Blog
    cursor = db.cursor()
    cursor.execute("SELECT * from board_board")
    datas = cursor.fetchall()

    users = dict()
    print("Start!!")
    for d in datas:
        if d[8] != "":
            users[d[0]] = d[8]

    for user in users.items():
        username = user[0]
        address = user[1]
        try:
            fp = feedparser.parse(address)
            for e in fp.entries:
                title = e.title
                url = e.links[0].href
                summary = e.summary
                time2 = e.published
                cursor.execute("INSERT INTO blog_blog(username,title,url,summary,time) SELECT %s, %s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT * FROM blog_blog WHERE url= %s)",
                            (username, title, url, summary, time2, url))
        except:
            pass
        db.commit()
        print(user, " Done!")

    # contest
    
    cursor.execute("truncate table contest_contestcominginfo")
    db.commit()


    for i in range(3):
        ss = (datetime.datetime.now()+datetime.timedelta(days=30*i)).strftime('%Y-%m')

        url = 'https://ac.nowcoder.com/acm/calendar/contest?token=&month='+ ss
        head = {}
            #写入User Agent信息
        head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36'
        req = request.Request(url, headers=head)
        response = request.urlopen(req)
        html = response.read().decode('utf-8')

        datajson = json.loads(html)

        for d in datajson["data"]:
            print(d)
            cursor.execute("INSERT INTO contest_contestcominginfo(ojName,link,startTime,endTime,contestName) SELECT %s, %s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT * FROM contest_contestcominginfo WHERE contestName= %s)",
                                (d["ojName"], d['link'], d['startTime'], d['endTime'], d['contestName'], d['contestName']))

        db.commit()

    sleep(7200)
