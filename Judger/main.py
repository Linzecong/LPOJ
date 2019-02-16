# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
import threading
import _judger
import os


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 



statue = True

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

judgername = judgerjson["judger_name"]
host = judgerjson["server_ip"]
port = judgerjson["server_port"]

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"], judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8' )
cursor = db.cursor()

def reconnect():
    global statue, clientsocket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        clientsocket.connect((host,port))
        statue = True
    except :
        print("connect error!")
        pass

reconnect()



def judge(id, code, lang, problem):
    global statue, cursor

    # print(id,code,lang,problem)

    if lang == "C":
        file = open("main.c", "w")
        file.write(code)
        file.close()
        result = os.system("gcc main.c -o main -O2")
        # print(result)
        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % (result,id))
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
        result = os.system("g++ main.cpp -o main -O2")
        # print(result)
        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % (result,id))
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return
    else:
        try:
            cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % ("Unknow language",id))
            db.commit()
            statue = True
        except:
            db.rollback()
            statue = True
        return

    cursor.execute("SELECT * from problem_problem where problem = '%s' " % problem)
    data = cursor.fetchone()

    timelimit = int(data[12])
    memorylimit = int(data[13])
    


    files = os.listdir("../DataServer/problemdata/%s/" % problem)

    print(files)

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
        print("judging!!!!!!!!",filename)
        ret = _judger.run(max_cpu_time=timelimit,
                    max_real_time=_judger.UNLIMITED,
                    max_memory=memorylimit * 1024 * 1024,
                    max_process_number=200,
                    max_output_size=32 * 1024 * 1024,
                    max_stack=32 * 1024 * 1024,
                    # five args above can be _judger.UNLIMITED
                    exe_path="main",
                    input_path="../DataServer/problemdata/%s/%s.in" % (problem,filename),
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
        print(ret)

        if ret["result"] != 0:

            if ret["result"] == 4 and ret["exit_code"] == 127 and ret["signal"] == 0:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '%s',testcase='%s'  WHERE id = '%s'" % ('3',filename, id))
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
            elif ret["result"] == 4 and ret["exit_code"] == 0 and ret["signal"] == 31:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '%s',testcase='%s'  WHERE id = '%s'" % ('3',filename, id))
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
            else:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '%s',testcase='%s'  WHERE id = '%s'" % (ret["result"],filename, id))
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
            return
        else:
            file1 = open("temp.out", "r")
            file2 = open("../DataServer/problemdata/%s/%s.out" % (problem,filename), "r")

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

                print(std,ans)

                stdout = stdout + std
                answer = answer + ans
                
                if std != ans:
                    result = -3
            
            if stdout == answer and result == -3:
                result = -5
            
            file1.close()
            file2.close()

            if result != 0:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '%s',testcase='%s' WHERE id = '%s'" % (result,filename, id))
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
                return
    try:
        cursor.execute("UPDATE judgestatus_judgestatus SET result = 0 WHERE id = '%s'" % id)
        db.commit()
        statue = True
    except:
        db.rollback()
        statue = True
        return
             

while True:
    sleep(1)
    try:
        data = clientsocket.recv(1024)  
        data = data.decode("utf-8")
        print(data)
        if data:
            if data == "getstatue":
                if statue == True:
                    clientsocket.send("ok".encode("utf-8"))
                else:
                    clientsocket.send("notok".encode("utf-8"))
                # print(statue)

            elif data.find("judge") != -1:
                statue = False
                tp = data.split("|")
                cursor.execute("SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                data = cursor.fetchone()
                print(data,tp[1])
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '-2',judger='%s' WHERE id = '%s'" % (judgername,tp[1]))
                    db.commit()
                    t = threading.Thread(target=judge,args=(data[0], data[12], data[8], data[3]))
                    t.setDaemon(True)
                    t.start()
                except:
                   db.rollback()
                   statue = True
        else:
            reconnect()
    except socket.error:
        reconnect()
    except:
        print("error!")
        break


