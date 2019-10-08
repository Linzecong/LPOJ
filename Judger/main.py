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
from JudgeHDU.JudgeHDU import JudgeHDU

# 全局变量类，用于保存全局变量
class GlobalVar:
    statue = True 
    datatimejson = {}
    judgerjson = {}
    judgername = "Unknow"
    host = "172.10.0.1"
    port = 22
    pythonpath = "/usr/bin/python"
    cursor = None
    db = None
    sftp_t = None
    sftp = None
    clientsocket = None

    @staticmethod 
    def initGlobalVar():
        GlobalVar.statue = True
        myjsonfile = open("./setting.json", 'r')
        GlobalVar.judgerjson = json.loads(myjsonfile.read())
        myjsonfile.close()

        if os.environ.get("DB_USER"):
            GlobalVar.judgerjson["db_ip"] = os.environ.get("DB_HOST")
            GlobalVar.judgerjson["db_pass"] = os.environ.get("DB_PASSWORD")
            GlobalVar.judgerjson["db_user"] = os.environ.get("DB_USER")
            GlobalVar.judgerjson["db_port"] = os.environ.get("DB_PORT")

            GlobalVar.judgerjson["server_ip"] = os.environ.get("SERVER_IP")
            GlobalVar.judgerjson["sftp_ip"] = os.environ.get("SFTP_IP")
            GlobalVar.judgerjson["sftp_port"] = os.environ.get("SFTP_PORT")
            GlobalVar.judgerjson["sftp_username"] = os.environ.get("SFTP_USER")
            GlobalVar.judgerjson["sftp_password"] = os.environ.get("SFTP_PASSWORD")
            GlobalVar.judgerjson["backend_path"] = os.environ.get("BACKEND_PATH")

        datajsonfile = open("./datatime.json", 'r')
        GlobalVar.datatimejson = json.loads(datajsonfile.read())
        datajsonfile.close()

        GlobalVar.judgername = socket.gethostbyname(socket.gethostname())

        GlobalVar.host = GlobalVar.judgerjson["server_ip"]
        GlobalVar.port = GlobalVar.judgerjson["server_port"]
        GlobalVar.pythonpath = GlobalVar.judgerjson["python_path"]

        GlobalVar.db = MySQLdb.connect(GlobalVar.judgerjson["db_ip"], GlobalVar.judgerjson["db_user"], GlobalVar.judgerjson["db_pass"],
                            GlobalVar.judgerjson["db_database"], int(GlobalVar.judgerjson["db_port"]), charset='utf8')
        GlobalVar.cursor = GlobalVar.db.cursor()

        GlobalVar.sftp_t = paramiko.Transport((GlobalVar.judgerjson["sftp_ip"], 22))
        GlobalVar.sftp_t.connect(username=GlobalVar.judgerjson["sftp_username"],
                    password=GlobalVar.judgerjson["sftp_password"])  # 登录远程服务器
        GlobalVar.sftp = paramiko.SFTPClient.from_transport(GlobalVar.sftp_t)  # sftp传输协议

        GlobalVar.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        GlobalVar.clientsocket.connect((GlobalVar.host, GlobalVar.port))

class Controller:

    @staticmethod
    def addProSubmitNum(problem):
        GlobalVar.cursor.execute("UPDATE problem_problemdata SET submission = submission+1 WHERE problem = '%s'" % problem)
        GlobalVar.db.commit()
    
    @staticmethod
    def getIsHaveDoneProblem(username, problem):
        acscore = False # 是否增加AC的积分，用于判断是否已经AC过，AC过就不再增加用户积分
        GlobalVar.cursor.execute(
            "SELECT * from judgestatus_judgestatus where user = '%s'  and problem = '%s' and result = 0" % (username, problem))
        r = GlobalVar.cursor.fetchall()
        if len(r) > 0:
            acscore = True
        return acscore

    @staticmethod
    def setBoard(id,statue):
        GlobalVar.cursor.execute("UPDATE contest_contestboard SET type = %d WHERE submitid = %s" , (statue, str(id)))
        GlobalVar.db.commit()
    
    @staticmethod
    def getProblemTimeMemory(problem):
        GlobalVar.cursor.execute("SELECT * from problem_problem where problem = '%s' " % problem)
        datat = GlobalVar.cursor.fetchone()
        timelimit = int(datat[11])
        memorylimit = int(datat[12]) 
        return timelimit,memorylimit
    
    @staticmethod
    def getProblemScore(problem):
        GlobalVar.cursor.execute("SELECT * from problem_problemdata where problem = '%s' " % problem)
        return GlobalVar.cursor.fetchone()[13]

    @staticmethod
    def compileError(id,problem,message):
        print(id,message,problem)
        GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET result = '-4',message=%s WHERE id = %s", (message, id))
        GlobalVar.cursor.execute("UPDATE problem_problemdata SET ce = ce+1 WHERE problem = '%s'" % problem)
        GlobalVar.db.commit()
    
    @staticmethod
    def acProblem(id,problem,message,memory,time,username,proscore,isac,contest):
        if message != "":
            GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = 0,message='%s'  WHERE id = '%s'" % (memory, time,message, id))
        else:
            GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = 0 WHERE id = '%s'" % (memory, time, id))
        
        GlobalVar.cursor.execute("UPDATE problem_problemdata SET ac = ac+1 WHERE problem = '%s'" % problem)
        if isac == False:
            GlobalVar.cursor.execute("UPDATE user_userdata SET score = score+%d WHERE username = '%s'" % (proscore, username))
            GlobalVar.cursor.execute("UPDATE user_userdata SET ac = ac+1 WHERE username = '%s'" % username)
            GlobalVar.cursor.execute("UPDATE user_userdata SET acpro = concat(acpro,'|%s') WHERE username = '%s'" % (str(problem), username))
        if contest != 0:
            GlobalVar.cursor.execute("UPDATE contest_contestboard SET type =1 WHERE submitid = '%s'" % id)
        GlobalVar.db.commit()
    
    @staticmethod
    def doneProblem(id,problem,message,memory,time,username,contest,result,testcase):
        if message != "":
            GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s',testcase='%s',message='%s'  WHERE id = '%s'" % (memory, time, result, testcase,message, id))
        else:
            GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET memory =%d, time=%d, result = '%s' WHERE id = '%s'" % (memory, time, result, id))
        
        if result == '2' or result == '1':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET tle = tle+1 WHERE problem = '%s'" % problem)
        if result == '3':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET mle = mle+1 WHERE problem = '%s'" % problem)
        if result == '4':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET rte = rte+1 WHERE problem = '%s'" % problem)
        if result == '5':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET se = se+1 WHERE problem = '%s'" % problem)
        if result == '-5':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET pe = pe+1 WHERE problem = '%s'" % problem)
        if result == '-3':
            GlobalVar.cursor.execute("UPDATE problem_problemdata SET wa = wa+1 WHERE problem = '%s'" % problem)
        if contest != 0:
            GlobalVar.cursor.execute("UPDATE contest_contestboard SET type =0  WHERE submitid = '%s'" % id)
        GlobalVar.db.commit()

    @staticmethod
    def doneCase(statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput):
        GlobalVar.cursor.execute("INSERT into judgestatus_casestatus (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (statusid,username,problem,result,time,memory,testcase,casedata,outputdata,useroutput))
        GlobalVar.db.commit()

    

# SPJ函数，首先编译，然后运行，然后返回程序运行结果
def specialjudge(problem,testin,testout,userout):
    result = os.system("timeout 10 g++ ./ProblemData/%s/spj.cpp -o spj.out -O2 -std=c++14" % str(problem))
    if result:
        return 5
    res = os.system("timeout 20 ./spj.out %s %s %s" % (testin, testout, userout))
    print(res)
    return res

# 用于远程下载数据文件，首先判断数据文件有没有更新，有的话就更新
def remote_scp(host_ip, remote_path, local_path, username, password, problem):
    try:
        if GlobalVar.sftp_t.is_authenticated() == False:
            GlobalVar.sftp_t.close()
            GlobalVar.sftp_t = paramiko.Transport((host_ip, 22))
            GlobalVar.sftp_t.connect(username=username, password=password)  # 登录远程服务器
            GlobalVar.sftp = paramiko.SFTPClient.from_transport(GlobalVar.sftp_t)  # sftp传输协议
        remt = 0
        try:
            remt = GlobalVar.sftp.stat(remote_path).st_mtime
        except:
            GlobalVar.sftp_t = paramiko.Transport((host_ip, 22))
            GlobalVar.sftp_t.connect(username=username, password=password)  # 登录远程服务器
            GlobalVar.sftp = paramiko.SFTPClient.from_transport(GlobalVar.sftp_t)  # sftp传输协议
            remt = GlobalVar.sftp.stat(remote_path).st_mtime

        if str(remt) == GlobalVar.datatimejson.get(str(problem), "no"):
            return

        GlobalVar.datatimejson[str(problem)] = str(remt)
        with open("./datatime.json", 'w', encoding='utf-8') as json_file:
            json.dump(GlobalVar.datatimejson, json_file, ensure_ascii=False)
            json_file.close()

        print("download……"+remote_path+"……to……"+local_path)
        GlobalVar.sftp.get(remote_path, local_path)  # 下载文件
        # 解压文件
        dirname = str(problem)
        try:
            shutil.rmtree("./ProblemData/" +
                          dirname+"/", ignore_errors=True)
            f = zipfile.ZipFile("./ProblemData/"+str(problem)+".zip", 'r')
            for file1 in f.namelist():
                f.extract(file1, "./ProblemData/"+dirname+"/")
            print("Extract Succeed！")
            return True
        except:
            shutil.rmtree("./ProblemData/" +
                          dirname+"/", ignore_errors=True)
            os.remove("./ProblemData/"+str(problem)+".zip")
            print("Extract Failed！")
            return False
    except IOError as e:
        print(e)
        return True

# 获取系统内存，返回MB，用于判断内存是否足够用于判题，否则，等待内存足够
def getmem():
    with open('/proc/meminfo') as fd:
        for line in fd:
            if line.startswith('MemAvailable'):
                free = line.split()[1]
                fd.close()
                break
    return int(free)/1024.0

# 敏感词列表，用于Python安全机制
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


def judgePython(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                        max_real_time=timelimit*10,
                        max_memory=memorylimit * 1024 * 1024,
                        max_process_number=200,
                        max_output_size=32 * 1024 * 1024,
                        max_stack=32 * 1024 * 1024,
                        # five args above can be _judger.UNLIMITED
                        exe_path=GlobalVar.pythonpath,
                        input_path=inputpath,
                        output_path=outputpath,
                        error_path=errorpath,
                        args=[judgername+".py"],
                        # can be empty list
                        env=[],
                        log_path=judgername+"judger.log",
                        # can be None
                        seccomp_rule_name="general",
                        uid=0,
                        gid=0
                        )

def judgeC(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                        max_real_time=timelimit*10,
                        max_memory=memorylimit * 1024 * 1024,
                        max_process_number=200,
                        max_output_size=32 * 1024 * 1024,
                        max_stack=32 * 1024 * 1024,
                        # five args above can be _judger.UNLIMITED
                        exe_path=judgername+".out",
                        input_path=inputpath,
                        output_path=outputpath,
                        error_path=errorpath,
                        args=[],
                        # can be empty list
                        env=[],
                        log_path=judgername+"judger.log",
                        # can be None
                        seccomp_rule_name="c_cpp",
                        uid=0,
                        gid=0
                        )

def judgeCPP(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                        max_real_time=timelimit*10,
                        max_memory=memorylimit * 1024 * 1024,
                        max_process_number=200,
                        max_output_size=32 * 1024 * 1024,
                        max_stack=32 * 1024 * 1024,
                        # five args above can be _judger.UNLIMITED
                        exe_path=judgername+".out",
                        input_path=inputpath,
                        output_path=outputpath,
                        error_path=errorpath,
                        args=[],
                        # can be empty list
                        env=[],
                        log_path=judgername+"judger.log",
                        # can be None
                        seccomp_rule_name="c_cpp",
                        uid=0,
                        gid=0
                        )

def judgeJava(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):

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
        GlobalVar.cursor.execute(
            "UPDATE judgestatus_judgestatus SET message=%s WHERE id = %s", (msg, id))
        GlobalVar.db.commit()
        ret["cpu_time"] = 0
        ret["memory"] = 5201314
        ret["result"] = 4
        ret["exit_code"] = result
        ret["signal"] = 0
        tf.close()

    return ret

def judgeSwift(timelimit, memorylimit, inputpath, outputpath, errorpath, id, judgername):
    return _judger.run(max_cpu_time=timelimit,
                        max_real_time=timelimit*10,
                        max_memory=memorylimit * 1024 * 1024,
                        max_process_number=200,
                        max_output_size=32 * 1024 * 1024,
                        max_stack=32 * 1024 * 1024,
                        # five args above can be _judger.UNLIMITED
                        exe_path=judgername+".out",
                        input_path=inputpath,
                        output_path=outputpath,
                        error_path=errorpath,
                        args=[],
                        # can be empty list
                        env=[],
                        log_path=judgername+"judger.log",
                        # can be None
                        seccomp_rule_name="c_cpp",
                        uid=0,
                        gid=0
                        )

def compileC(id,code,judgername,problem):
    file = open("%s.c" % judgername, "w")
    file.write(code)
    file.close()
    result = os.system("timeout 10 gcc %s.c -fmax-errors=3 -o %s.out -O2 -std=c11 2>%sce.txt" % (judgername, judgername, judgername))
    if result:
        try:
            filece = open("%sce.txt" % judgername, "r")
            msg = str(filece.read())
            if msg == "": msg = "Compile timeout! Maybe you define too big arrays!"
            filece.close()
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        except:
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        return False
    return True

def compileCPP(id,code,judgername,problem):
    file = open("%s.cpp" % judgername, "w")
    file.write(code)
    file.close()
    result = os.system("timeout 10 g++ %s.cpp -fmax-errors=3 -o %s.out -O2 -std=c++14 2>%sce.txt" %(judgername, judgername, judgername))
    if result:
        try:
            filece = open("%sce.txt" % judgername, "r")
            msg = str(filece.read())
            if msg == "": msg = "Compile timeout! Maybe you define too big arrays!"
            filece.close()
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        except:
            msg = str("Fatal Compile error!")
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        return False
    return True

def compilePython(id,code,judgername,problem):
    wo = minganci(code)
    if wo != "0":
        Controller.compileError(id,problem,"Your code has sensitive words "+wo)
        GlobalVar.statue = True
        return False
    file = open("%s.py" % judgername, "w")
    file.write("import sys\nblacklist = ['importlib','traceback','os','sys']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel sys\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['exec']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
    file.close()
    return True

def compileJava(id,code,judgername,problem):
    file = open("Main.java", "w")
    file.write(code)
    file.close()

    isExists = os.path.exists(judgername)
    if not isExists:
        os.makedirs(judgername)

    result = os.system("javac Main.java -d %s 2>%sce.txt" % (judgername, judgername))

    if result:
        try:
            filece = open("%sce.txt" % judgername, "r")
            msg = str(filece.read())
            filece.close()
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        except:
            msg = str("Fatal Compile error!")
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        return False
    return True

def compileSwift(id,code,judgername,problem):
    file = open("%s.swift" % judgername, "w")
    file.write(code)
    file.close()
    result = os.system("~/swift-5.1-RELEASE-ubuntu18.04/usr/bin/swiftc %s.swift -o %s.out 2>%sce.txt" %(judgername, judgername, judgername))
    if result:
        try:
            filece = open("%sce.txt" % judgername, "r")
            msg = str(filece.read())
            if msg == "": msg = "Compile timeout! Maybe you define too big arrays!"
            filece.close()
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        except:
            msg = str("Fatal Compile error!")
            Controller.compileError(id,problem,msg)
            GlobalVar.statue = True
        return False
    return True



def judge(id, code, lang, problem, contest, username, submittime, contestproblem, oj, ojpro):
    """
        id: 提交的ID
        code: 提交的代码
        lang: 提交的语言
        problem: 提交的题目ID（LPOJ里的ID）
        contest: 属于哪个比赛的提交，为0时，不属于任何比赛的提交
        username: 提交的用户ID
        submittime: 提交时间，用于比赛的排行榜逻辑
        contestproblem: 如果是比赛中的提交，那么是比赛中的第几题，用于比赛的排行榜逻辑
        oj: 提交的是哪一个OJ，用于VJudge
        ojpro: 其实是提交中的message字段，用于保存VJudge中提交的是远程OJ的哪一题
    """

    contest = int(contest)
    contest = contest + 1 # 迷之Bug
    contest = contest - 1

    if contest != 0: Controller.setBoard(id,-1) # 把比赛排行榜该提交设为 不计算罚时

    HaveAC = Controller.getIsHaveDoneProblem(username,problem) # 获取是否已经AC

    if HaveAC == False: Controller.addProSubmitNum(problem) # 没有AC过，则该题目增加1次提交数
        
    # 转换成unix时间的毫秒
    def date_time_milliseconds(date_time_obj):
        return int(time.mktime(date_time_obj.timetuple()) * 1000)
    submittime = date_time_milliseconds(submittime)

    timelimit,memorylimit = Controller.getProblemTimeMemory(problem)
    score = Controller.getProblemScore(problem)


    if oj != "LPOJ":
        if oj == "HDU":
            try:
                jr = JudgeHDU(ojpro, lang, code)
                if jr[0] == "-4":
                    Controller.compileError(id,problem,jr[3])
                    GlobalVar.statue = True
                    return
                if jr[0] == "0":
                    Controller.acProblem(id,problem,jr[3],int(jr[2]), int(jr[1]),username,score,HaveAC,contest)
                    GlobalVar.statue = True
                else:
                    Controller.doneProblem(id,problem,jr[3],int(jr[2]), int(jr[1]),username,contest,jr[0],"?")
                    GlobalVar.statue = True
            except Exception as e:
                Controller.doneProblem(id,problem,str(e).replace('\'',"").replace("\"",""),0, 0,username,contest,"5","?")
                GlobalVar.statue = True
        return
    else:

        if lang == "C": 
            if compileC(id,code,GlobalVar.judgername,problem) == False: 
                return

        elif lang == "C++": 
            if compileCPP(id,code,GlobalVar.judgername,problem) == False: 
                return

        elif lang == "Python3": 
            if compilePython(id,code,GlobalVar.judgername,problem) == False: 
                return
        
        elif lang == "Swift5.1": 
            if compileSwift(id,code,GlobalVar.judgername,problem) == False: 
                return

        elif lang == "Java": 
            if compileJava(id,code,GlobalVar.judgername,problem) == False: 
                return

        else:
            Controller.compileError(id,problem,"Unknow Language!")
            GlobalVar.statue = True
            return

        # 最终的结果，用于判完所有数据！
        maxmemory = 0
        maxtime = 0

        myresult = 100
        mytestcase = ""
        mytime = 0
        mymemory = 0

        # 尝试下载数据

        isdone = remote_scp(GlobalVar.judgerjson["sftp_ip"], GlobalVar.judgerjson["backend_path"]+"ProblemData/"+str(problem)+".zip", "./ProblemData/" +
                    str(problem)+".zip", GlobalVar.judgerjson["sftp_username"], GlobalVar.judgerjson["sftp_password"], problem)

        # 判断有无数据
        if isdone == False: 
            Controller.doneProblem(id,problem,"unzip error!",0,0,username,contest,"5","?")
            return
        try:
            files = os.listdir("./ProblemData/%s/" % problem)
        except:
            Controller.doneProblem(id,problem,"download error!",0,0,username,contest,"5","?")
            GlobalVar.statue = True
            return

        tempset = set()  # 用于判读数据是否都有in,out
        newfiles = set()
        casedes = dict()
        for s in files:
            s = s.replace(".in", "")
            s = s.replace(".out", "")
            try:
                if s == "casedes.txt":
                    file3 = open("./ProblemData/%s/casedes.txt" % problem,"r",encoding='utf-8')
                    while file3.readable() is True:
                        des = str(file3.readline()).strip()
                        # print(des)
                        if des.find("|")!=-1:
                            casedes[des.split("|")[0]]=des.split("|")[1]
                        if des == "":
                            break

                    file3.close()
                    continue
            except Exception as e:
                print(e)
                casedes = dict()
            if s in tempset:
                newfiles.add(s)
            else:
                tempset.add(s)

        import re
        def sort_key(s):
            if s:
                try:
                    c = re.findall('^\d+', s)[0]
                except:
                    c = -1
                return int(c)
        newfiles = list(newfiles)
        newfiles.sort(key=sort_key) # 将数据排个序

        for filename in newfiles:
            print("judging!!!", id, "/%s/%s.in" % (problem, filename))
            try:
                waittime = 0
                while True:
                    memo = getmem()
                    if memo >= memorylimit/5: # 5倍差不多了
                        break
                    waittime = waittime + 1
                    if waittime > 15:
                        print("memory error!")
                        Controller.doneProblem(id,problem,"system memory low!!!",0,0,username,contest,"5","?")
                        GlobalVar.statue = True
                        return
                    sleep(1)
            except Exception as e:
                Controller.doneProblem(id,problem,"memory error!",0,0,username,contest,"5","?")
                GlobalVar.statue = True
                return
            ret = []

            if lang == "Java": ret = judgeJava(timelimit*3, memorylimit, "./ProblemData/%s/%s.in" % (problem, filename), GlobalVar.judgername+"temp.out", GlobalVar.judgername+"error.out", id,GlobalVar.judgername)
            
            elif lang == "Python3": ret = judgePython(timelimit, memorylimit, "./ProblemData/%s/%s.in" % (problem, filename), GlobalVar.judgername+"temp.out", GlobalVar.judgername+"error.out", id, GlobalVar.judgername)
            
            elif lang == "C": ret = judgeC(timelimit, memorylimit, "./ProblemData/%s/%s.in" % (problem, filename), GlobalVar.judgername+"temp.out", GlobalVar.judgername+"error.out", id, GlobalVar.judgername)

            elif lang == "C++": ret = judgeCPP(timelimit, memorylimit, "./ProblemData/%s/%s.in" % (problem, filename), GlobalVar.judgername+"temp.out", GlobalVar.judgername+"error.out", id, GlobalVar.judgername)
            
            elif lang == "Swift5.1": ret = judgeSwift(timelimit, memorylimit, "./ProblemData/%s/%s.in" % (problem, filename), GlobalVar.judgername+"temp.out", GlobalVar.judgername+"error.out", id, GlobalVar.judgername)

            else:
                Controller.compileError(id,problem,"Unknow Language!")
                GlobalVar.statue = True
                return
                    

            print(ret)

            maxmemory = max(ret["memory"], maxmemory)
            maxtime = max(ret["cpu_time"], maxtime)

            useroutputdata = ""
            outputdata = ""
            casedata = ""
            if contest == 0:
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

                    useroutputfile = open(GlobalVar.judgername+"temp.out", "r")
                    useroutputdata = useroutputfile.read(300)
                    tmpstr = useroutputfile.read(5)
                    if tmpstr != "":
                        useroutputdata = useroutputdata + '\n......'
                    useroutputfile.close()
                    # if lang == "Python3":
                    #     useroutputdata = "Python language does not support viewing output"
                except:
                    ret["result"] = 5

            # 单组样例，程序执行结束，判断是否超时等！
            if ret["result"] != 0:

                # 青岛大学判 Memory Exceed的一个迷之Bug，所以要特判一下

                if (ret["result"] == 4 and ret["exit_code"] == 127 and ret["signal"] == 0) or (ret["result"] == 4 and ret["exit_code"] == 0 and ret["signal"] == 31):

                    # 更新最终结果为第一次错误的样例
                    if myresult == 100:
                        myresult = '3'
                        mytestcase = filename
                        mytime = ret["cpu_time"]
                        mymemory = ret["memory"]

                    Controller.doneCase(id,username,problem,'Memory Limit Exceeded',ret["cpu_time"],ret["memory"]/1024/1024,filename+" ("+casedes.get(filename,filename)+")",casedata,outputdata,useroutputdata)

                else:
                    # 更新最终结果为第一次错误的样例
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


                    Controller.doneCase(
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
                    )

                # 比赛中的提交，不需要判完所有样例
                if contest !=0:
                    break

            else:

                isspj = ""
                result = 0  # 0 ac -3 wrong -5 presentation
                # specialjudge，如果spj.cpp存在，则判定为特判问题
                if os.path.isfile("./ProblemData/%s/spj.cpp" %problem):
                    isspj = " (This test case is Special Judge) "
                    r = specialjudge(problem,"./ProblemData/%s/%s.in" %(problem, filename), "./ProblemData/%s/%s.out" % (problem, filename), GlobalVar.judgername+"temp.out")
                    if r == 256: result = -3
                    elif r == 0: result = 0
                    else: result = 5

                else:
                    # 比较输出文件是否一致！
                    file1 = open(GlobalVar.judgername+"temp.out", "r")
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

                # 单组样例评判完毕，保存单组样例评判结果
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

                    Controller.doneCase(
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
                    )

                    if contest != 0:
                        break

                else:
                    Controller.doneCase(
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
                    )

        # 所有样例评判结束，汇总结果！
        if myresult == 100:
            Controller.acProblem(id,problem,"",maxmemory/1024/1024,maxtime,username,score,HaveAC,contest)
                
        else:
            Controller.doneProblem(id,problem,"",mymemory/1024/1024, mytime,username,contest,myresult,mytestcase)

        GlobalVar.statue = True


def reconnect():
    GlobalVar.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        GlobalVar.db = MySQLdb.connect(GlobalVar.judgerjson["db_ip"], GlobalVar.judgerjson["db_user"], GlobalVar.judgerjson["db_pass"],
                            GlobalVar.judgerjson["db_database"], int(GlobalVar.judgerjson["db_port"]), charset='utf8')
        GlobalVar.cursor = GlobalVar.db.cursor()
        GlobalVar.clientsocket.connect((GlobalVar.host, GlobalVar.port))
        GlobalVar.statue = True
    except Exception as e:
        print(e)
        print("connect error!")
        pass

def MainLoop():
    while True:
        sleep(1)
        cur = 1
        try:
            data = GlobalVar.clientsocket.recv(1024)
            data = data.decode("utf-8")
            if data:
                if data == "getstatue":
                    if GlobalVar.statue == True:
                        GlobalVar.clientsocket.send("ok".encode("utf-8"))
                    else:
                        GlobalVar.clientsocket.send("notok".encode("utf-8"))
                elif data == "timeout":
                    print("timeout!")
                    GlobalVar.cursor.execute(
                        "UPDATE judgestatus_judgestatus SET memory =0, time=0, result = '5', message='Judger out of time', testcase='0'  WHERE id = '%s'" % (cur))
                    GlobalVar.db.commit()
                    break
                elif data.find("judge") != -1:
                    GlobalVar.statue = False
                    tp = data.split("|")
                    cur = tp[1]
                    try:
                        GlobalVar.cursor.execute("SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                    except:
                        print("too long no submit")
                        reconnect()
                        GlobalVar.cursor.execute("SELECT * from judgestatus_judgestatus where id = '%s'" % tp[1])
                    data = GlobalVar.cursor.fetchone()
                    try:
                        GlobalVar.cursor.execute("UPDATE judgestatus_judgestatus SET result = '-2',judger='%s' WHERE id = '%s'" % (GlobalVar.judgername, tp[1]))
                        GlobalVar.db.commit()
                        t = threading.Thread(target=judge, args=(
                            data[0], data[13], data[8], data[3], data[11], data[1], data[9], data[12], data[2],data[15]))
                        t.setDaemon(True)
                        t.start()
                    except:
                        GlobalVar.db.rollback()
                        GlobalVar.statue = True
            else:
                reconnect()
        except socket.error:
            reconnect()
        except Exception as e:
            print(e)
            reconnect()

if __name__ == "__main__":
    GlobalVar.initGlobalVar()
    MainLoop()