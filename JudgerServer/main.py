# coding=utf-8

import MySQLdb
from queue import Queue
import socket
import json
from time import sleep
import threading
import os


mutex = threading.Lock()  # queue mutex

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
 
# 获取未判题列表，放入到全局队列中
def getSubmition():
    global queue, mutex, db

    cursor = db.cursor()
    while True:
        sleep(1)
        if mutex.acquire():
            cursor.execute(
                "SELECT * from judgestatus_judgestatus where result = '-1'")
            data = cursor.fetchall()
            try:
                for d in data:
                    queue.put(d[0])
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET result = '-6' WHERE id = '%d'" % d[0])
                db.commit()
            except:
                db.rollback()
            mutex.release()
    db.close()


# 处理每个判题机的逻辑
def deal_client(newSocket: socket, addr):
    global mutex, queue
    statue = False
    cursor = db.cursor()
    falsetime = 0
    while True:
        sleep(2) # 每隔两秒取两次
        if mutex.acquire(): # 获取队列锁
            try:
                if statue == True and queue.empty() is not True:
                    id = queue.get() # 如果可以判题，那就发送判题命令  
                    cursor.execute(
                        "SELECT language from judgestatus_judgestatus where id = '%d'" % (id))
                    data = cursor.fetchall()
                   # print(data[0][0])
                    newSocket.send(("judge|%d" % id).encode("utf-8"))
                    statue = False 
                else:
                    newSocket.send("getstatue".encode("utf-8"))
                    data = newSocket.recv(1024)
                    recv_data = data.decode('utf-8')
                    if recv_data == "ok": 
                        falsetime = 0
                        statue = True
                    else:
                        falsetime = falsetime + 1
                        statue = False
                        if falsetime >= 180: # 计算一下未准备好的时间，如果超过120s，发送销毁重启命令
                            newSocket.send("timeout".encode("utf-8"))
                           # print(addr, "timeout!")
                            newSocket.close()
                            mutex.release()
                            return
                   # print(addr, statue)

            except socket.error:
                newSocket.close()
                mutex.release()
                
                return
            except:
                print("error!")
                mutex.release()
                
                return
            mutex.release()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", judgerjson["server_port"]))
server.listen(20)
print("server is running!")

t = threading.Thread(target=getSubmition, args=()) # 用一个线程去跑
t.setDaemon(True)
t.start()


# 比赛题目设置为auth=2,contest开始时，自动设置题目为auth=3，比赛结束自动设置auth=1
def changeauth():
    global db, mutex
    curcontest = set()
    curpro = set()
    curinpro = set()
    cursor = db.cursor()
    while True:
        sleep(2)
        if mutex.acquire():
            cursor.execute(
                "SELECT * from contest_contestinfo where type <> 'Personal' and TO_SECONDS(NOW()) - TO_SECONDS(begintime) <= lasttime")
            data = cursor.fetchall()
            getcontest = set()
            for d in data:
                getcontest.add(d[0])  # 用于求结束的比赛
                cursor.execute(
                    "SELECT * from contest_contestproblem where contestid=%d" % d[0])
                pros = cursor.fetchall()
                for pid in pros:
                    if pid[2] not in curpro:
                        curpro.add(pid[2])
                        cursor.execute(
                            "UPDATE  problem_problemdata SET auth = 2 WHERE problem = %s" % pid[2])
                        cursor.execute(
                            "UPDATE  problem_problem SET auth = 2 WHERE problem = %s" % pid[2])
                db.commit()

            cursor.execute(
                "SELECT * from contest_contestinfo where type <> 'Personal' and TO_SECONDS(NOW()) - TO_SECONDS(begintime) <= lasttime and TO_SECONDS(NOW()) - TO_SECONDS(begintime) >=-1")
            data = cursor.fetchall()
            for d in data:
                cursor.execute(
                    "SELECT * from contest_contestproblem where contestid=%d" % d[0])
                pros = cursor.fetchall()
                for pid in pros:
                    if pid[2] not in curinpro:
                        curinpro.add(pid[2])
                        cursor.execute(
                            "UPDATE  problem_problemdata SET auth = 3 WHERE problem = %s" % pid[2])
                        cursor.execute(
                            "UPDATE  problem_problem SET auth = 3 WHERE problem = %s" % pid[2])
                db.commit()

            endcontest = curcontest.difference(getcontest)
           # print("curcontest", curcontest)
            for eid in endcontest:
                cursor.execute(
                    "SELECT * from contest_contestproblem where contestid=%d" % eid)
                pros = cursor.fetchall()
                for pid in pros:
                    try:
                        curpro.remove(pid[2])
                        curinpro.remove(pid[2])
                    except KeyError:
                        pass
                    cursor.execute(
                        "UPDATE  problem_problemdata SET auth = 1 WHERE problem = %s" % pid[2])
                    cursor.execute(
                        "UPDATE  problem_problem SET auth = 1 WHERE problem = %s" % pid[2])
                db.commit()
            curcontest = getcontest
            mutex.release()


t1 = threading.Thread(target=changeauth, args=())
t1.setDaemon(True)
t1.start()


# 循环监听
while True:
    newSocket, addr = server.accept()
    print("client [%s] is connected!" % str(addr))
    client = threading.Thread(target=deal_client, args=(newSocket, addr))
    client.setDaemon(True)
    client.start()
