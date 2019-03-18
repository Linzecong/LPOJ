# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
from Codeforces import get_CF_data
from HDU import get_HDU_data
from Vjudge import get_VJ_data


myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')

while True:
    cursor = db.cursor()
    cursor.execute( "SELECT * from board_board")
    datas = cursor.fetchall()
    for data in datas:
        username = str(data[0])
        accounts = str(data[5]).split("|")
        print(username)
        CF = get_CF_data(accounts[0])
        print(accounts[0],"CF:",CF)
        if CF[0] == -1:
            continue
        HDU = get_HDU_data(accounts[1])
        print(accounts[1],"HDU:",HDU)
        if HDU[0] == -1:
            continue
        VJ = get_VJ_data(accounts[2])
        print(accounts[2],"VJ:",VJ)
        if VJ[0] == -1:
            continue

        Others = [0,0] #其他OJ

        ac = str(CF[0]) + "|" + str(HDU[0]) + "|" + str(VJ[0]) + "|" + str(Others[0])
        submit = str(CF[1]) + "|" + str(HDU[1]) + "|" + str(VJ[1]) + "|" + str(Others[0])
        cursor.execute("UPDATE board_board SET acnum = '%s' ,submitnum = '%s'  WHERE username = '%s'" % (ac,submit,username))
        db.commit()
        print(username,ac,submit)
    sleep(300)



