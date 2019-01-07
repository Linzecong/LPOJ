# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
import threading
import _judger
import os

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = "localhost"

port = 1234

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen()

statue = True


myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"], judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8' )
cursor = db.cursor()


def judge(id, code, lang, problem):
    global statue

    if lang == "C":
        file = open("main.c", "w")
        file.write(code)
        file.close()
        result = os.system("gcc main.c -o2 main")

        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4' WHERE id = '%d'" % id)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
                return

    elif lang == "C++":
        file = open("main.cpp", "w")
        file.write(code)
        file.close()
        result = os.system("g++ main.cpp -o2 main")
        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4' WHERE id = '%d'" % id)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
                return
    
    def file_name(file_dir):
        for root, dirs, files in os.walk(file_dir):
            return files  # 当前路径下所有非目录子文件

    files = file_name("../DataServer/problemdata/")

    tempset = set() # 用于判读数据是否都有in,out
    newfiles = set()
    for s in files:
        s = s.replace(".in","")
        s = s.replace(".out","")
        if s in tempset:
            newfiles.add(s)
        else:
            tempset.add(s)

    for filename in newfiles:
        ret = _judger.run(max_cpu_time=1000,
                    max_real_time=2000,
                    max_memory=128 * 1024 * 1024,
                    max_process_number=200,
                    max_output_size=10000,
                    max_stack=32 * 1024 * 1024,
                    # five args above can be _judger.UNLIMITED
                    exe_path="main",
                    input_path="../DataServer/problemdata/%s.in" % filename,
                    output_path="temp.out",
                    error_path="error.out",
                    args=[],
                    # can be empty list
                    env=[],
                    log_path="judger.log",
                    # can be None
                    seccomp_rule_name="c_cpp",
                    uid=0,
                    gid=0
                    )

        if ret["result"] != 0:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '%d' WHERE id = '%d'" % (ret["result"], id))
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
                return
        else:
            file1 = open("temp.out", "r")
            file2 = open("../DataServer/problemdata/%s.out" % filename, "r")

            result = 0 # 0 ac -3 wrong -5 presentation

            stdout = ""
            answer = ""

            while True:
                
                std = file1.readline()
                ans = file2.readline()

                if std == "" and ans == "":
                    break

                std = std.rstrip()
                ans = ans.rstrip()

                stdout = stdout + std
                answer = answer + ans
                
                if std != ans:
                    result = -3
            
            if stdout == answer:
                result = -5
            
            file1.close()
            file2.close()

            if result != 0:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '%d' WHERE id = '%d'" % (result, id))
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
                    return
    try:
        cursor.execute("UPDATE judgestatus_judgestatus SET result = 0 WHERE id = '%d'" % id)
        db.commit()
        statue = True
    except:
        db.rollback()
        statue = True
        return
             

while True:
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()   
    print(addr)
    data = clientsocket.recv(1024)  
    print(data)
    if data:
        if data == "getstatue":
            if statue == True:
                clientsocket.send("ok")
            else:
                clientsocket.send("notok")

        elif data.find("judge") != -1:
            statue = False
            tp = data.split("|")
            cursor.execute("SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
            data = cursor.fetchone()
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-2' WHERE id = '%d'" % tp[1])
                db.commit()
                t = threading.Thread(target=judge,args=(data[0], data[12], data[8], data[3]))
                t.setDaemon(True)
                t.start()
            except:
                db.rollback()
                statue = True

    clientsocket.close()
