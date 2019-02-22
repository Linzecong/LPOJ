# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
import threading


mutex = threading.Lock()  # queue mutex

queue = list()
myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')


def getSubmition():
    global queue, mutex

    cursor = db.cursor()
    while True:
        sleep(1)
        cursor.execute(
            "SELECT * from judgestatus_judgestatus where result = '-1'")
        data = cursor.fetchall()

       # print(data)

        if mutex.acquire():
            try:
                for d in data:
                    queue.append(d[0])
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET result = '-6' WHERE id = '%d'" % d[0])
                db.commit()
            except:
                db.rollback()
            queue.sort(reverse=True)
            mutex.release()
    db.close()


def deal_client(newSocket: socket, addr):
    global mutex, queue
    statue = False
    while True:
        sleep(1)
        if mutex.acquire():
            try:
                print(addr)
                if statue == True and len(queue) > 0:
                    id = queue.pop()
                    statue = False
                    newSocket.send(("judge|%d" % id).encode("utf-8"))
                else:
                    newSocket.send("getstatue".encode("utf-8"))
                    print("send!!", addr)
                    data = newSocket.recv(1024)
                    recv_data = data.decode('utf-8')
                    print(recv_data)
                    if recv_data == "ok":
                        statue = True
                    else:
                        statue = False
                    print(statue)

            except socket.error:
                newSocket.close()
                mutex.release()
                return
            # except:
            #     print("error!")
            #     mutex.release()
            #     return
            mutex.release()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", judgerjson["server_port"]))
server.listen(20)
print("server is running!")

t = threading.Thread(target=getSubmition, args=())
t.setDaemon(True)
t.start()


# 记得添加contest开始时，自动设置题目为auth=3，比赛结束自动设置auth=1

while True:
    newSocket, addr = server.accept()
    print("client [%s] is connected!" % str(addr))
    client = threading.Thread(target=deal_client, args=(newSocket, addr))
    client.setDaemon(True)
    client.start()
