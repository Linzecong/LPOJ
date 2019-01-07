# coding=utf-8

import MySQLdb
from socket import *
import json
from time import sleep
import threading


myjsonfile = open("./judger.json", 'r')
judgerjson = json.loads(myjsonfile.read())

ip = list()
port = list()
statue = list()
for s in judgerjson['judger']:
    ip.append(s['ip'])
    port.append(s['port'])
    statue.append(False)

judgernum = len(ip)

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"], judgerjson["db_database"],int(judgerjson["db_port"]), charset='utf8' )
cursor = db.cursor()

sockets = list()
for i in range(judgernum):
    tp = socket(AF_INET,SOCK_STREAM)
    tp.settimeout(2)
    sockets.append(tp)


mutex = threading.Lock() # statue mutex

def run(id):
    global sockets, mutex, statue
    while True:
        sleep(1)
        if mutex.acquire():
            try:
                print(id)
                sockets[id].connect((ip[id],int(port[id])))
                sockets[id].send("getstatue")
                total_data=[]
                while True:
                    data = sockets[id].recv(1024)   
                    if not data: 
                        break
                    total_data.append(data)
                recv_data = ''.join(total_data)
                if recv_data:
                    if recv_data == "ok":
                        statue[id]=True
                    else:
                        statue[id]=False
                else:
                    statue[id]=False
                sockets[id].close()
            except:
                pass
            mutex.release() 

for i in range(judgernum):
    t = threading.Thread(target=run,args=(i,))
    t.setDaemon(True)
    t.start()


while True:
    sleep(1)
    
    cursor.execute("SELECT * from judgestatus_judgestatus where result = '-1' order by id limit %s" % judgernum)

    data = cursor.fetchall()
    judgequeue = list()

    print(data)

    for t in data:
        judgequeue.append(t[0])
    
    if mutex.acquire():
        for id in judgequeue:
            for num in range(judgernum):
                if statue[num] == True:
                    statue[num] = False
                    try:
                        sockets[num].connect((ip[num],int(port[num])))
                        sockets[num].send("judge|%d" % id[0])
                        sockets[num].close()
                    except:
                        pass
        mutex.release()


db.close()

