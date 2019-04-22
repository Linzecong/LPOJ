# coding=utf-8

import MySQLdb
import socket
import json
from time import sleep
import threading
import _judger
import os
import time
import datetime


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


statue = True

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

judgername = input(
    "Please input judger name(must different or may cause judge problem):  ")
host = judgerjson["server_ip"]
port = judgerjson["server_port"]

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')
cursor = db.cursor()


def reconnect():
    global statue, clientsocket,db,cursor
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')
        cursor = db.cursor()
        clientsocket.connect((host, port))
        statue = True
    except:
        print("connect error!")
        pass


reconnect()


def judgeJava(timelimit, memorylimit, inputpath, outputpath, errorpath):

    com1 = "/usr/bin/time -f '"+"%"+"U' -o %stime.txt " % (judgername)
    com2 = "timeout %s java -cp %s -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx%sM -Djava.security.manager -Djava.security.policy==policy -Djava.awt.headless=true Main 1>%s 2>%s<%s" % (
        str(timelimit/1000.0), judgername,memorylimit, outputpath, errorpath, inputpath)
    com = com1 + com2
    #print(com)
    result = os.system(com)

    ret = dict()

    if result == 0:
        tf = open(judgername+"time.txt", "r")
        time = tf.read()
        #print(time)
        time = float(str(time).strip())*1000
        ret["cpu_time"] = int(time)
        ret["memory"] = 5201314
        ret["result"] = 0
        ret["exit_code"] = result
        ret["signal"] = 0
    elif result == 31744:
        
        ret["cpu_time"] = timelimit
        ret["memory"] = 5201314
        ret["result"] = 1
        ret["exit_code"] = result
        ret["signal"] = 0
    else:
        ret["cpu_time"] = 0
        ret["memory"] = 5201314
        ret["result"] = 4
        ret["exit_code"] = result
        ret["signal"] = 0

    return ret


def judge(id, code, lang, problem, contest, username, submittime, contestproblem):
    global statue, cursor
    contest = int(contest)
    contest = contest + 1
    contest = contest - 1

    acscore = False
    cursor.execute(
        "SELECT * from judgestatus_judgestatus where user = '%s'  and problem = '%s' and result = 0" % (username, problem))
    r = cursor.fetchall()
    if len(r) > 0:
        acscore = True

    acornot = False
    li = []
    if contest is not 0:
        cursor.execute(
                "UPDATE contest_contestboard SET type = -1 WHERE submitid = '%s'" % id)
        cursor.execute(
            "SELECT * from contest_contestrank where username = '%s'  and contestid = %d" % (username, int(contest)))
        r = cursor.fetchone()
        statue = r[4]
        li = statue.split("|")
        if(li[contestproblem].find("$") >= 0):
            acornot = True

    def date_time_milliseconds(date_time_obj):
        return int(time.mktime(date_time_obj.timetuple()) * 1000)
    submittime = date_time_milliseconds(submittime)

    cursor.execute(
        "UPDATE problem_problemdata SET submission = submission+1 WHERE problem = '%s'" % problem)
    if acscore == False:
        cursor.execute(
            "UPDATE user_userdata SET submit = submit+1 WHERE username = '%s'" % username)
    db.commit()

    if lang == "C":
        file = open("%s.c" % judgername, "w")
        file.write(code)
        file.close()
        result = os.system("gcc %s.c -o %s.out -O2 -std=c11 2>%sce.txt" %
                           (judgername, judgername,judgername))
        # print(result)
        if result:
            try:
                filece = open("%sce.txt" % judgername, "r")
                msg = str(filece.read())
                filece.close()
                cursor.execute(
                    "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s" , (msg, id))
                cursor.execute(
                    "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return

    elif lang == "C++":
        file = open("%s.cpp" % judgername, "w")
        file.write(code)
        file.close()
        result = os.system("g++ %s.cpp -o %s.out -O2 -std=c++11 2>%sce.txt" %
                           (judgername, judgername,judgername))
        # print(result)
        if result:
            try:
                filece = open("%sce.txt" % judgername, "r")
                msg = str(filece.read())
                filece.close()
                cursor.execute(
                    "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s" , (msg, id))
                cursor.execute(
                    "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return
    elif lang == "Java":
        file = open("Main.java", "w")
        file.write(code)
        file.close()

        isExists = os.path.exists(judgername)
        if not isExists:
            os.makedirs(judgername)

        result = os.system("javac Main.java -d %s 2>%sce.txt" %
                           (judgername,judgername))

        if result:
            try:
                filece = open("%sce.txt" % judgername, "r")
                msg = str(filece.read())
                filece.close()
                cursor.execute(
                    "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s" , (msg, id))
                cursor.execute(
                    "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
            except:
                db.rollback()
                statue = True
            return
    else:
        try:
            cursor.execute(
                "UPDATE judgestatus_judgestatus SET result = '-4',message='%s' WHERE id = '%s'" % ("Unknow language", id))
            cursor.execute(
                "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
            db.commit()
            statue = True
        except:
            db.rollback()
            statue = True
        return

    cursor.execute(
        "SELECT * from problem_problem where problem = '%s' " % problem)
    datat = cursor.fetchone()

    timelimit = int(datat[11])
    memorylimit = int(datat[12])

    cursor.execute(
        "SELECT * from problem_problemdata where problem = '%s' " % problem)
    datat = cursor.fetchone()
    score = int(datat[13])

    files = os.listdir("../DataServer/problemdata/%s/" % problem)

    tempset = set()  # 用于判读数据是否都有in,out
    newfiles = set()
    for s in files:
        s = s.replace(".in", "")
        s = s.replace(".out", "")
        if s in tempset:
            newfiles.add(s)
        else:
            tempset.add(s)

    maxmemory = 0
    maxtime = 0

    myresult = 100
    mytestcase = ""
    mytime = 0
    mymemory = 0

    newfiles = list(newfiles)
    newfiles.sort()

    for filename in newfiles:
        print("judging!!!!!!", id, "/%s/%s.in" % (problem, filename))
        if lang == "Java":
            ret = judgeJava(timelimit*1.5, memorylimit, "../DataServer/problemdata/%s/%s.in" % (
                            problem, filename), judgername+"temp.out", judgername+"error.out")
        else:
            ret = _judger.run(max_cpu_time=timelimit,
                              max_real_time=_judger.UNLIMITED,
                              max_memory=memorylimit * 1024 * 1024,
                              max_process_number=200,
                              max_output_size=32 * 1024 * 1024,
                              max_stack=32 * 1024 * 1024,
                              # five args above can be _judger.UNLIMITED
                              exe_path=judgername+".out",
                              input_path="../DataServer/problemdata/%s/%s.in" % (
                                  problem, filename),
                              output_path=judgername+"temp.out",
                              error_path=judgername+"error.out",
                              args=[],
                              # can be empty list
                              env=[],
                              log_path=judgername+"judger.log",
                              # can be None
                              seccomp_rule_name="c_cpp",
                              uid=0,
                              gid=0
                              )

        print(ret)
        maxmemory = max(ret["memory"], maxmemory)
        maxtime = max(ret["cpu_time"], maxtime)

        useroutputdata = ""
        outputdata = ""
        casedata = ""
        if contest is 0:
            try:
                # 计算case
                inputfile = open("../DataServer/problemdata/%s/%s.in" %
                                 (problem, filename), "r")
                casedata = inputfile.read(400)
                tmpstr = inputfile.read(10)
                if tmpstr != "":
                    casedata = casedata + '\n......'
                inputfile.close()

                outputfile = open(
                    "../DataServer/problemdata/%s/%s.out" % (problem, filename), "r")
                outputdata = outputfile.read(400)
                tmpstr = outputfile.read(10)
                if tmpstr != "":
                    outputdata = outputdata + '\n......'
                outputfile.close()

                useroutputfile = open(judgername+"temp.out", "r")
                useroutputdata = useroutputfile.read(400)
                tmpstr = useroutputfile.read(10)
                if tmpstr != "":
                    useroutputdata = useroutputdata + '\n......'
                useroutputfile.close()
            except:
                ret["result"] = 5

        if ret["result"] != 0:
            if (ret["result"] == 4 and ret["exit_code"] == 127 and ret["signal"] == 0) or (ret["result"] == 4 and ret["exit_code"] == 0 and ret["signal"] == 31):

                if myresult == 100:
                    myresult = '3'
                    mytestcase = filename
                    mytime = ret["cpu_time"]
                    mymemory = ret["memory"]
                cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                    id,
                    username,
                    problem,
                    'Memory Limit Exceeded',
                    ret["cpu_time"],
                    ret["memory"]/1024/1024,
                    filename,
                    casedata,
                    outputdata,
                    useroutputdata
                ))
                db.commit()
            else:
                if myresult == 100:
                    myresult = str(ret['result'])
                    mytestcase = filename
                    mytime = ret["cpu_time"]
                    mymemory = ret["memory"]

                resultstr = "Unknow"
                if ret["result"] == 2 or ret["result"] == 1:
                    resultstr = 'Time Limit Exceeded'
                if ret["result"] == 3:
                    resultstr = 'Memory Limit Exceeded'
                if ret["result"] == 4:
                    resultstr = 'Runtime Error'
                if ret["result"] == 5:
                    resultstr = 'System Error'

                cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                    id,
                    username,
                    problem,
                    resultstr,
                    ret["cpu_time"],
                    ret["memory"]/1024/1024,
                    filename,
                    casedata,
                    outputdata,
                    useroutputdata
                ))

                db.commit()
            if contest is not 0:
                break
        else:
            file1 = open(judgername+"temp.out", "r")
            file2 = open("../DataServer/problemdata/%s/%s.out" %
                         (problem, filename), "r")

            result = 0  # 0 ac -3 wrong -5 presentation

            stdout = ""
            answer = ""

            while True:
                try:
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
                except:
                    result = -3
                    stdout = "1"
                    answer = "0"
                    break

            if stdout == answer and result == -3:
                result = -5

            file1.close()
            file2.close()

            if result != 0:
                if myresult == 100:
                    myresult = str(result)
                    mytestcase = filename
                    mytime = ret["cpu_time"]
                    mymemory = ret["memory"]

                resultstr = "Unknow"
                if result == -5:
                    resultstr = 'Presentation Error'
                if result == -3:
                    resultstr = 'Wrong Answer'

                cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                    id,
                    username,
                    problem,
                    resultstr,
                    ret["cpu_time"],
                    ret["memory"]/1024/1024,
                    filename,
                    casedata,
                    outputdata,
                    useroutputdata
                ))

                db.commit()
                if contest is not 0:
                    break
            else:
                cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                    id,
                    username,
                    problem,
                    'Accepted',
                    ret["cpu_time"],
                    ret["memory"]/1024/1024,
                    filename,
                    casedata,
                    outputdata,
                    useroutputdata
                ))
                db.commit()

    if myresult == 100:
        cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = 0  WHERE id = '%s'" % (
            maxmemory/1024/1024, maxtime, id))
        cursor.execute(
            "UPDATE problem_problemdata SET ac = ac+1 WHERE problem = '%s'" % problem)
        if acscore == False:
            cursor.execute(
                "UPDATE user_userdata SET score = score+%d WHERE username = '%s'" % (score, username))
            cursor.execute(
                "UPDATE user_userdata SET ac = ac+1 WHERE username = '%s'" % username)
            cursor.execute(
                "UPDATE user_userdata SET acpro = concat(acpro,'|%s') WHERE username = '%s'" % (str(problem),username))

        if contest is not 0:
            cursor.execute(
                "UPDATE contest_contestboard SET type =1 WHERE submitid = '%s'" % id)
            if acornot == False:
                li[contestproblem] = str(
                    submittime)+"$" + str(li[contestproblem])
                sta = '|'.join(str(i) for i in li)
                cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (
                    sta, username, contest))
    else:
        cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s'  WHERE id = '%s'" % (
            mymemory/1024/1024, mytime, myresult, mytestcase, id))

        if myresult == '2' or myresult == '1':
            cursor.execute(
                "UPDATE problem_problemdata SET tle = tle+1 WHERE problem = '%s'" % problem)
        if myresult == '3':
            cursor.execute(
                "UPDATE problem_problemdata SET mle = mle+1 WHERE problem = '%s'" % problem)
        if myresult == '4':
            cursor.execute(
                "UPDATE problem_problemdata SET rte = rte+1 WHERE problem = '%s'" % problem)
        if myresult == '5':
            cursor.execute(
                "UPDATE problem_problemdata SET se = se+1 WHERE problem = '%s'" % problem)
        if myresult == '-5':
            cursor.execute(
                "UPDATE problem_problemdata SET pe = pe+1 WHERE problem = '%s'" % problem)
        if myresult == '-3':
            cursor.execute(
                "UPDATE problem_problemdata SET wa = wa+1 WHERE problem = '%s'" % problem)

        if contest is not 0:
            cursor.execute(
                "UPDATE contest_contestboard SET type =0  WHERE submitid = '%s'" % id)
            if acornot == False:
                li[contestproblem] = int(li[contestproblem])
                li[contestproblem] = li[contestproblem]-1
                sta = '|'.join(str(i) for i in li)
                # print(contest)
                cursor.execute("UPDATE  contest_contestrank  SET statue = '%s' where username = '%s'  and contestid = %d" % (
                    sta, username, contest))

    db.commit()
    statue = True


while True:
    sleep(1)
    try:
        data = clientsocket.recv(1024)
        data = data.decode("utf-8")
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
                cursor.execute(
                    "SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                data = cursor.fetchone()

                try:
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET result = '-2',judger='%s' WHERE id = '%s'" % (judgername, tp[1]))
                    db.commit()
                    t = threading.Thread(target=judge, args=(
                        data[0], data[13], data[8], data[3], data[11], data[1], data[9], data[12]))
                    t.setDaemon(True)
                    t.start()
                except:
                    db.rollback()
                    statue = True
        else:
            reconnect()
    except socket.error:
        reconnect()
    except Exception as e:
        print(e)
        reconnect()


# #include<iostream>
# using namespace std;
# int main(){
# int a,b;
# cin>>a>>b;
# cout<<a+b<<endl;

# return 0;
# }
