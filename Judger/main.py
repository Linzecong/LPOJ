# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
import threading
import _judger
import os,time,datetime


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 



statue = True

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

judgername =input("Please input judger name(must different or may cause judge problem):  ")
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



def judge(id, code, lang, problem,contest,username,submittime,contestproblem):
    global statue, cursor

    acscore = False
    cursor.execute("SELECT * from judgestatus_judgestatus where user = '%s'  and problem = '%s' and result = 0" % (username,problem))
    r = cursor.fetchall()
    if len(r)>0:
        acscore=True
    

    acornot = False
    li = []
    if contest is not 0:
        cursor.execute("SELECT * from contest_contestrank where username = '%s'  and contestid = %d" % (username,contest))
        r = cursor.fetchone()
        statue = r[4]
        li = statue.split("|")
        if(li[contestproblem].find("$")>=0):
            acornot = True

    print(submittime)
    def date_time_milliseconds(date_time_obj):
        return int(time.mktime(date_time_obj.timetuple()) * 1000)
    submittime = date_time_milliseconds(submittime)
    print(submittime)

    cursor.execute("UPDATE problem_problemdata SET submission = submission+1 WHERE problem = '%s'" % problem)
    db.commit()

    if lang == "C":
        file = open("%s.c"% judgername, "w")
        file.write(code)
        file.close()
        result = os.system("gcc %s.c -o %s.out -O2" %(judgername,judgername))
        # print(result)
        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % (result,id))
                cursor.execute("UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return

    elif lang == "C++":
        file = open("%s.cpp"%judgername, "w")
        file.write(code)
        file.close()
        result = os.system("g++ %s.cpp -o %s.out -O2"%(judgername,judgername))
        # print(result)
        if result:
            try:
                cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % (result,id))
                cursor.execute("UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return
    else:
        try:
            cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % ("Unknow language",id))
            cursor.execute("UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
            db.commit()
            statue = True
        except:
            db.rollback()
            statue = True
        return

    cursor.execute("SELECT * from problem_problem where problem = '%s' " % problem)
    datat = cursor.fetchone()

    timelimit = int(datat[11])
    memorylimit = int(datat[12])

    cursor.execute("SELECT * from problem_problemdata where problem = '%s' " % problem)
    datat = cursor.fetchone()
    score = int(datat[13])

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

    maxmemory = 0
    maxtime = 0

    for filename in newfiles:
        print("judging!!!!!!!!","../DataServer/problemdata/%s/%s.in" % (problem,filename))
        ret = _judger.run(max_cpu_time=timelimit,
                    max_real_time=_judger.UNLIMITED,
                    max_memory=memorylimit * 1024 * 1024,
                    max_process_number=200,
                    max_output_size=32 * 1024 * 1024,
                    max_stack=32 * 1024 * 1024,
                    # five args above can be _judger.UNLIMITED
                    exe_path=judgername+".out",
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
        maxmemory = max(ret["memory"],maxmemory)
        maxtime = max(ret["cpu_time"],maxtime)
        if ret["result"] != 0:

            if ret["result"] == 4 and ret["exit_code"] == 127 and ret["signal"] == 0:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s'  WHERE id = '%s'" % (maxmemory/1024/1024,maxtime,'3',filename, id))
                    cursor.execute("UPDATE problem_problemdata SET mle = mle+1 WHERE problem = '%s'" % problem)
                    if contest is not 0:
                        cursor.execute("UPDATE contest_contestboard SET type =0  WHERE submitid = '%s'" %  id)
                        if acornot == False:
                            li[contestproblem]=int(li[contestproblem])
                            li[contestproblem] = li[contestproblem]-1
                            sta = '|'.join(str(i) for i in li)
                            cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (sta,username,contest))
                            
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
            elif ret["result"] == 4 and ret["exit_code"] == 0 and ret["signal"] == 31:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s'  WHERE id = '%s'" % (maxmemory/1024/1024,maxtime,'3',filename, id))
                    cursor.execute("UPDATE problem_problemdata SET mle = mle+1 WHERE problem = '%s'" % problem)
                    if contest is not 0:
                        cursor.execute("UPDATE contest_contestboard SET type =0  WHERE submitid = '%s'" %  id)
                        if acornot == False:
                            li[contestproblem]=int(li[contestproblem])
                            li[contestproblem] = li[contestproblem]-1
                            sta = '|'.join(str(i) for i in li)
                            cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (sta,username,contest))
                        
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
            else:
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s'  WHERE id = '%s'" % (maxmemory/1024/1024,maxtime,ret["result"],filename, id))
                    if ret["result"] == 2 or ret["result"] == 1:
                        cursor.execute("UPDATE problem_problemdata SET tle = tle+1 WHERE problem = '%s'" % problem)
                    if ret["result"] == 3:
                        cursor.execute("UPDATE problem_problemdata SET mle = mle+1 WHERE problem = '%s'" % problem)
                    if ret["result"] == 4:
                        cursor.execute("UPDATE problem_problemdata SET rte = rte+1 WHERE problem = '%s'" % problem)
                    if ret["result"] == 5:
                        cursor.execute("UPDATE problem_problemdata SET se = se+1 WHERE problem = '%s'" % problem)

                    if contest is not 0:
                        cursor.execute("UPDATE contest_contestboard SET type =0  WHERE submitid = '%s'" %  id)
                        if acornot == False:
                            li[contestproblem]=int(li[contestproblem])
                            li[contestproblem] = li[contestproblem]-1
                            sta = '|'.join(str(i) for i in li)
                            cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (sta,username,contest))
                        
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
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s'  WHERE id = '%s'" % (maxmemory/1024/1024,maxtime,result,filename, id))
                    if result == -5:
                        cursor.execute("UPDATE problem_problemdata SET pe = pe+1 WHERE problem = '%s'" % problem)
                    if result == -3:
                        cursor.execute("UPDATE problem_problemdata SET wa = wa+1 WHERE problem = '%s'" % problem)

                    if contest is not 0:
                        cursor.execute("UPDATE contest_contestboard SET type =0 WHERE submitid = '%s'" %  id)
                        if acornot == False:
                            li[contestproblem]=int(li[contestproblem])
                            li[contestproblem] = li[contestproblem]-1
                            sta = '|'.join(str(i) for i in li)
                            cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (sta,username,contest))
                        
                    db.commit()
                    statue = True
                except:
                    db.rollback()
                    statue = True
                return

    try:
        cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = 0  WHERE id = '%s'" % (maxmemory/1024/1024,maxtime, id))
        cursor.execute("UPDATE problem_problemdata SET ac = ac+1 WHERE problem = '%s'" % problem)

        if acscore == False:
            cursor.execute("UPDATE user_userdata SET score = score+%d WHERE username = '%s'" % (score,username) )
        if contest is not 0:
            cursor.execute("UPDATE contest_contestboard SET type =1 WHERE submitid = '%s'" %  id)
            if acornot == False:
                li[contestproblem]=str(submittime)+"$"+ str(li[contestproblem])
                sta = '|'.join(str(i) for i in li)
                cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (sta,username,contest))
            
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
                
                print(data[11],tp[1])
                try:
                    cursor.execute("UPDATE judgestatus_judgestatus SET result = '-2',judger='%s' WHERE id = '%s'" % (judgername,tp[1]))
                    db.commit()
                    t = threading.Thread(target=judge,args=(data[0], data[12], data[8], data[3],data[11],data[1],data[9],data[15]))
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


# #include<iostream>
# using namespace std;
# int main(){
# int a,b;
# cin>>a>>b;
# cout<<a+b<<endl;

# return 0;
# }