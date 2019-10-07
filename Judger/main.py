# coding=utf-8
import shutil
import paramiko
import MySQLdb
import socket
import json
from time import sleep
import threading
import _judger
import os
import zipfile
import time
import datetime
from VJudge.HDUVjudge import HDUVJudge


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


statue = True

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())
myjsonfile.close()

if os.environ.get("DB_USER"):
    judgerjson["db_ip"] = os.environ.get("DB_HOST")
    judgerjson["db_pass"] = os.environ.get("DB_PASSWORD")
    judgerjson["db_user"] = os.environ.get("DB_USER")
    judgerjson["db_port"] = os.environ.get("DB_PORT")

    judgerjson["server_ip"] = os.environ.get("SERVER_IP")
    judgerjson["sftp_ip"] = os.environ.get("SFTP_IP")
    judgerjson["sftp_port"] = os.environ.get("SFTP_PORT")
    judgerjson["sftp_username"] = os.environ.get("SFTP_USER")
    judgerjson["sftp_password"] = os.environ.get("SFTP_PASSWORD")
    judgerjson["backend_path"] = os.environ.get("BACKEND_PATH")

datajsonfile = open("./datatime.json", 'r')
datatimejson = json.loads(datajsonfile.read())
datajsonfile.close()

judgername = socket.gethostbyname(socket.gethostname())

host = judgerjson["server_ip"]
port = judgerjson["server_port"]
pythonpath = judgerjson["python_path"]

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')
cursor = db.cursor()


sftp_t = paramiko.Transport((judgerjson["sftp_ip"], 22))
sftp_t.connect(username=judgerjson["sftp_username"],
               password=judgerjson["sftp_password"])  # 登录远程服务器
sftp = paramiko.SFTPClient.from_transport(sftp_t)  # sftp传输协议


def specialjudge(problem,testin,testout,userout):

    result = os.system("timeout 10 g++ ./ProblemData/%s/spj.cpp -o spj.out -O2 -std=c++14" % str(problem))
    if result:
        return 5
    res = os.system("timeout 20 ./spj.out %s %s %s" % (testin, testout, userout))
    print(res)
    return res

def remote_scp(host_ip, remote_path, local_path, username, password, problem):
    global sftp, sftp_t
    try:
        if sftp_t.is_authenticated() == False:
            sftp_t.close()
            sftp_t = paramiko.Transport((host_ip, 22))
            sftp_t.connect(username=username, password=password)  # 登录远程服务器
            sftp = paramiko.SFTPClient.from_transport(sftp_t)  # sftp传输协议
        remt = 0
        try:
            remt = sftp.stat(remote_path).st_mtime
        except:
            sftp_t = paramiko.Transport((host_ip, 22))
            sftp_t.connect(username=username, password=password)  # 登录远程服务器
            sftp = paramiko.SFTPClient.from_transport(sftp_t)  # sftp传输协议
            remt = sftp.stat(remote_path).st_mtime

        if str(remt) == datatimejson.get(str(problem), "no"):
            return

        datatimejson[str(problem)] = str(remt)
        with open("./datatime.json", 'w', encoding='utf-8') as json_file:
            json.dump(datatimejson, json_file, ensure_ascii=False)
            json_file.close()
        print("download……"+remote_path+"……to……"+local_path)
        sftp.get(remote_path, local_path)  # 下载文件
        # 解压文件
        dirname = str(problem)
        try:
            shutil.rmtree("./ProblemData/" +
                          dirname+"/", ignore_errors=True)
            f = zipfile.ZipFile("./ProblemData/"+str(problem)+".zip", 'r')
            for file1 in f.namelist():
                f.extract(file1, "./ProblemData/"+dirname+"/")
            print("Extract Succeed！")
        except:
            shutil.rmtree("./ProblemData/" +
                          dirname+"/", ignore_errors=True)
            os.remove("./ProblemData/"+str(problem)+".zip")
            print("Extract Failed！")
    except IOError as e:
        print(e)


def getmem():
    with open('/proc/meminfo') as fd:
        for line in fd:
            if line.startswith('MemAvailable'):
                free = line.split()[1]
                fd.close()
                break
    return int(free)/1024.0


def reconnect():
    global statue, clientsocket, db, cursor
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


def minganci(ci):

    if ci.find("thread") >= 0:
        return "thread"
    if ci.find("process") >= 0:
        return "process"
    if ci.find("resource") >= 0:
        return "resource"
    if ci.find("ctypes") >= 0:
        return "ctypes"
    if ci.find(" os") >= 0:
        return " os"
    if ci.find("__import__") >= 0:
        return "__import__"
    if ci.find("getattr") >= 0:
        return "getattr"
    if ci.find("eval") >= 0:
        return "eval"
    if ci.find("exec") >= 0:
        return "exec"
    if ci.find("__") >= 0:
        return "__"
    if ci.find("globals") >= 0:
        return "globals"
    if ci.find("locals") >= 0:
        return "locals"
    if ci.find("raise") >= 0:
        return "raise"
    if ci.find("compile") >= 0:
        return "compile"
    if ci.find("frame") >= 0:
        return "frame"
    return "0"


def judgePython(timelimit, memorylimit, inputpath, outputpath, errorpath, id):
    com1 = "/usr/bin/time -f '"+"%"+"U' -o %stime.txt " % (judgername)
    com2 = "timeout %s python3  %s.py 1>%s 2>%s<%s" % (
        str(timelimit/1000.0), judgername, outputpath, errorpath, inputpath)
    com = com1 + com2
    result = os.system(com)

    ret = dict()

    if result == 0:
        tf = open(judgername+"time.txt", "r")
        time = tf.read()
        time = float(str(time).strip())*1000
        ret["cpu_time"] = int(time)
        ret["memory"] = 5201314
        ret["result"] = 0
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()
    elif result == 31744:
        ret["cpu_time"] = timelimit
        ret["memory"] = 5201314
        ret["result"] = 1
        ret["exit_code"] = result
        ret["signal"] = 0
    else:
        tf = open(errorpath, "r")
        sttr = tf.read()
        if sttr.find("MemoryError") >= 0:
            ret["cpu_time"] = 0
            ret["memory"] = memorylimit*1024*1024
            ret["result"] = 3
            ret["exit_code"] = result
            ret["signal"] = 0
        else:
            tf = open(errorpath, "r")
            msg = tf.read()
            msg = "Python language does not support viewing runtime error message"
            cursor.execute(
                "UPDATE judgestatus_judgestatus SET message=%s WHERE id = %s", (msg, id))
            db.commit()

            ret["cpu_time"] = 0
            ret["memory"] = 0
            ret["result"] = 4
            ret["exit_code"] = result
            ret["signal"] = 0
            tf.close()

    return ret


def judgeJava(timelimit, memorylimit, inputpath, outputpath, errorpath, id):

    com1 = "/usr/bin/time -f '"+"%"+"U' -o %stime.txt " % (judgername)
    com2 = "timeout %s java -cp %s -Djava.security.manager -Djava.security.policy==policy -Djava.awt.headless=true Main 1>%s 2>%s<%s" % (
        str(timelimit/1000.0), judgername, outputpath, errorpath, inputpath)
    com = com1 + com2
    result = os.system(com)

    ret = dict()

    if result == 0:
        tf = open(judgername+"time.txt", "r")
        time = tf.read()
        time = float(str(time).strip())*1000
        ret["cpu_time"] = int(time)
        ret["memory"] = 5201314
        ret["result"] = 0
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()
    elif result == 31744:
        ret["cpu_time"] = timelimit
        ret["memory"] = 5201314
        ret["result"] = 1
        ret["exit_code"] = result
        ret["signal"] = 0
    else:
        tf = open(errorpath, "r")
        msg = tf.read()
        cursor.execute(
            "UPDATE judgestatus_judgestatus SET message=%s WHERE id = %s", (msg, id))
        db.commit()
        ret["cpu_time"] = 0
        ret["memory"] = 5201314
        ret["result"] = 4
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()

    return ret


def judge(id, code, lang, problem, contest, username, submittime, contestproblem, oj,ojpro):
    global statue, cursor, pythonpath
    contest = int(contest)
    contest = contest + 1
    contest = contest - 1

    acscore = False
    cursor.execute(
        "SELECT * from judgestatus_judgestatus where user = '%s'  and problem = '%s' and result = 0" % (username, problem))
    r = cursor.fetchall()
    if len(r) > 0:
        acscore = True

    if contest is not 0:
        cursor.execute(
            "UPDATE contest_contestboard SET type = -1 WHERE submitid = '%s'" % id)

    def date_time_milliseconds(date_time_obj):
        return int(time.mktime(date_time_obj.timetuple()) * 1000)
    submittime = date_time_milliseconds(submittime)

    cursor.execute(
        "UPDATE problem_problemdata SET submission = submission+1 WHERE problem = '%s'" % problem)
    if acscore == False:
        cursor.execute(
            "UPDATE user_userdata SET submit = submit+1 WHERE username = '%s'" % username)
    db.commit()

    cursor.execute(
        "SELECT * from problem_problem where problem = '%s' " % problem)
    datat = cursor.fetchone()

    timelimit = int(datat[11])
    memorylimit = int(datat[12])

    cursor.execute(
        "SELECT * from problem_problemdata where problem = '%s' " % problem)
    datat = cursor.fetchone()
    score = int(datat[13])

    if oj != "LPOJ":
        if oj == "HDU":
            try:
                jr = HDUVJudge(ojpro, lang, code)
                if jr[0] == "-4":
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (jr[3], id))
                    cursor.execute(
                        "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                    db.commit()
                    statue = True
                    return
                if jr[0] == "0":
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = 0,message='%s'  WHERE id = '%s'" % (
                        int(jr[2]), int(jr[1]),jr[3], id))
                    cursor.execute(
                        "UPDATE problem_problemdata SET ac = ac+1 WHERE problem = '%s'" % problem)
                    if acscore == False:
                        cursor.execute(
                            "UPDATE user_userdata SET score = score+%d WHERE username = '%s'" % (score, username))
                        cursor.execute(
                            "UPDATE user_userdata SET ac = ac+1 WHERE username = '%s'" % username)
                        cursor.execute(
                            "UPDATE user_userdata SET acpro = concat(acpro,'|%s') WHERE username = '%s'" % (str(problem), username))

                    if contest is not 0:
                        cursor.execute(
                            "UPDATE contest_contestboard SET type =1 WHERE submitid = '%s'" % id)
                        
                    db.commit()
                    statue = True
                else:
                    myresult = jr[0]
                    cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s',message='%s'  WHERE id = '%s'" % (
                        int(jr[2]), int(jr[1]), myresult, "?",jr[3], id))

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

                    db.commit()
                    statue = True
            except Exception as e:
                cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s',message='%s'  WHERE id = '%s'" % (
                    0, 0, "5", "?", str(e).replace('\'',"").replace("\"",""), id))
                cursor.execute(
                    "UPDATE problem_problemdata SET se = se+1 WHERE problem = '%s'" % problem)
                db.commit()
                statue = True
        return
    else:
        try:

            if lang == "C":
                file = open("%s.c" % judgername, "w")
                file.write(code)
                file.close()
                result = os.system("timeout 10 gcc %s.c -fmax-errors=3 -o %s.out -O2 -std=c11 2>%sce.txt" %
                                   (judgername, judgername, judgername))
                if result:
                    try:
                        filece = open("%sce.txt" % judgername, "r")
                        msg = str(filece.read())
                        if msg == "":
                            msg = "Compile timeout! Maybe you define too big arrays!"
                        filece.close()
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    except:
                        msg = str("Fatal Compile error!")
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    return

            elif lang == "C++":
                file = open("%s.cpp" % judgername, "w")
                file.write(code)
                file.close()
                result = os.system("timeout 10 g++ %s.cpp -fmax-errors=3 -o %s.out -O2 -std=c++14 2>%sce.txt" %
                                   (judgername, judgername, judgername))
                if result:
                    try:
                        filece = open("%sce.txt" % judgername, "r")
                        msg = str(filece.read())
                        if msg == "":
                            msg = "Compile timeout! Maybe you define too big arrays!"
                        filece.close()
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    except:
                        msg = str("Fatal Compile error!")
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    return

            elif lang == "Python3":

                wo = minganci(code)
                if wo != "0":
                    try:
                        cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s",
                                       ("Your code has sensitive words "+wo, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    except:
                        db.rollback()
                        statue = True
                    return

                file = open("%s.py" % judgername, "w")
                file.write("import sys\nblacklist = ['importlib','traceback','os','sys']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel sys\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['exec']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
                file.close()

            elif lang == "Java":
                file = open("Main.java", "w")
                file.write(code)
                file.close()

                isExists = os.path.exists(judgername)
                if not isExists:
                    os.makedirs(judgername)

                result = os.system("javac Main.java -d %s 2>%sce.txt" %
                                   (judgername, judgername))

                if result:
                    try:
                        filece = open("%sce.txt" % judgername, "r")
                        msg = str(filece.read())
                        filece.close()
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
                        statue = True
                    except:
                        msg = str("Fatal Compile error!")
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (msg, id))
                        cursor.execute(
                            "UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
                        db.commit()
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
        except:
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

        # 尝试下载数据

        remote_scp(judgerjson["sftp_ip"], judgerjson["backend_path"]+"ProblemData/"+str(problem)+".zip", "./ProblemData/" +
                   str(problem)+".zip", judgerjson["sftp_username"], judgerjson["sftp_password"], problem)

        # 判断有无数据
        try:
            files = os.listdir("./ProblemData/%s/" % problem)
        except:
            cursor.execute(
                "UPDATE judgestatus_judgestatus SET memory =0, time=0, result = '5',testcase='0'  WHERE id = '%s'" % (id))
            db.commit()
            statue = True
            return

        tempset = set()  # 用于判读数据是否都有in,out
        newfiles = set()
        casedes = dict()
        for s in files:
            s = s.replace(".in", "")
            s = s.replace(".out", "")
            if s == "casedes.txt":
                file3 = open("./ProblemData/%s/casedes.txt"%problem,"r");
                while file3.readable() is True:
                    des = str(file3.readline()).strip()
                    # print(des)
                    if des.find("|")!=-1:
                        casedes[des.split("|")[0]]=des.split("|")[1]
                    if des == "":
                        break

                file3.close()
                continue
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
            try:
                waittime = 0
                while True:
                    memo = getmem()
                    # print(memo, memorylimit)
                    if memo >= memorylimit/2:
                        break
                    waittime = waittime + 1
                    if waittime > 15:
                        print("memory error!")
                        cursor.execute(
                            "UPDATE judgestatus_judgestatus SET memory =0, time=0, result = '5',testcase='0'  WHERE id = '%s'" % (id))
                        db.commit()
                        statue = True
                        return
                    sleep(1)
            except Exception as e:
                print(e)
                cursor.execute(
                    "UPDATE judgestatus_judgestatus SET memory =0, time=0, result = '5',testcase='0'  WHERE id = '%s'" % (id))
                db.commit()
                statue = True
                return

            if lang == "Java":
                ret = judgeJava(timelimit*3, memorylimit, "./ProblemData/%s/%s.in" % (
                                problem, filename), judgername+"temp.out", judgername+"error.out", id)
            elif lang == "Python3":
                # ret = judgePython(timelimit*2, memorylimit, "./ProblemData/%s/%s.in" % (
                #     problem, filename), judgername+"temp.out", judgername+"error.out", id)
                ret = _judger.run(max_cpu_time=timelimit,
                                      max_real_time=timelimit*10,
                                      max_memory=memorylimit * 1024 * 1024,
                                      max_process_number=200,
                                      max_output_size=32 * 1024 * 1024,
                                      max_stack=32 * 1024 * 1024,
                                      # five args above can be _judger.UNLIMITED
                                      exe_path=pythonpath,
                                      input_path="./ProblemData/%s/%s.in" % (
                                          problem, filename),
                                      output_path=judgername+"temp.out",
                                      error_path=judgername+"error.out",
                                      args=[judgername+".py"],
                                      # can be empty list
                                      env=[],
                                      log_path=judgername+"judger.log",
                                      # can be None
                                      seccomp_rule_name="general",
                                      uid=0,
                                      gid=0
                                      )
            else:
                try:
                    ret = _judger.run(max_cpu_time=timelimit,
                                      max_real_time=timelimit*10,
                                      max_memory=memorylimit * 1024 * 1024,
                                      max_process_number=200,
                                      max_output_size=32 * 1024 * 1024,
                                      max_stack=32 * 1024 * 1024,
                                      # five args above can be _judger.UNLIMITED
                                      exe_path=judgername+".out",
                                      input_path="./ProblemData/%s/%s.in" % (
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
                except:
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET message='Judger Fatal Error!' memory =0, time=0, result = '5',testcase='0'  WHERE id = '%s'" % (id))
                    db.commit()
                    statue = True
                    return

            print(ret)
            maxmemory = max(ret["memory"], maxmemory)
            maxtime = max(ret["cpu_time"], maxtime)

            useroutputdata = ""
            outputdata = ""
            casedata = ""
            if contest is 0:
                try:
                    # 计算case
                    inputfile = open("./ProblemData/%s/%s.in" %
                                     (problem, filename), "r")
                    casedata = inputfile.read(300)
                    tmpstr = inputfile.read(5)
                    if tmpstr != "":
                        casedata = casedata + '\n......'
                    inputfile.close()

                    outputfile = open(
                        "./ProblemData/%s/%s.out" % (problem, filename), "r")
                    outputdata = outputfile.read(300)
                    tmpstr = outputfile.read(5)
                    if tmpstr != "":
                        outputdata = outputdata + '\n......'
                    outputfile.close()

                    useroutputfile = open(judgername+"temp.out", "r")
                    useroutputdata = useroutputfile.read(300)
                    tmpstr = useroutputfile.read(5)
                    if tmpstr != "":
                        useroutputdata = useroutputdata + '\n......'
                    useroutputfile.close()
                    # if lang == "Python3":
                    #     useroutputdata = "Python language does not support viewing output"
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
                        filename+" ("+casedes.get(filename,filename)+")",
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
                        filename+" ("+casedes.get(filename,filename)+")",
                        casedata,
                        outputdata,
                        useroutputdata
                    ))

                    db.commit()
                if contest is not 0:
                    break
            else:
                isspj = ""
                result = 0  # 0 ac -3 wrong -5 presentation
                # specialjudge，如果spj.cpp存在，则判定为特判问题
                if os.path.isfile("./ProblemData/%s/spj.cpp" %problem):
                    isspj = " (This test case is Special Judge) "
                    r = specialjudge(problem,"./ProblemData/%s/%s.in" %(problem, filename), "./ProblemData/%s/%s.out" % (problem, filename), judgername+"temp.out")
                    if r == 256: result = -3
                    elif r == 0: result = 0
                    else: result = 5

                else:
                    file1 = open(judgername+"temp.out", "r")
                    file2 = open("./ProblemData/%s/%s.out" %
                                (problem, filename), "r")
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
                    del stdout
                    del answer

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
                    if result == 5:
                        resultstr = 'System Error'

                    cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                        id,
                        username,
                        problem,
                        resultstr,
                        ret["cpu_time"],
                        ret["memory"]/1024/1024,
                        filename+isspj+" ("+casedes.get(filename,filename)+")",
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
                        filename+isspj+" ("+casedes.get(filename,filename)+")",
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
                    "UPDATE user_userdata SET acpro = concat(acpro,'|%s') WHERE username = '%s'" % (str(problem), username))

            if contest is not 0:
                cursor.execute(
                    "UPDATE contest_contestboard SET type =1 WHERE submitid = '%s'" % id)
                
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

        db.commit()
        statue = True


cur = 1
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
            elif data == "timeout":
                print("timeout!")
                cursor.execute(
                    "UPDATE judgestatus_judgestatus SET memory =0, time=0, result = '5',testcase='0'  WHERE id = '%s'" % (cur))
                db.commit()
                break
            elif data.find("judge") != -1:
                statue = False
                tp = data.split("|")
                cur = tp[1]
                try:
                    cursor.execute(
                        "SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                except:
                    reconnect()
                    cursor.execute(
                        "SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                data = cursor.fetchone()
                try:
                    cursor.execute(
                        "UPDATE judgestatus_judgestatus SET result = '-2',judger='%s' WHERE id = '%s'" % (judgername, tp[1]))
                    db.commit()
                    t = threading.Thread(target=judge, args=(
                        data[0], data[13], data[8], data[3], data[11], data[1], data[9], data[12], data[2],data[15]))
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
