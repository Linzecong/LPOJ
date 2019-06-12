# 判题服务器开发

判题服务器非常的简单，几乎无需做任何修改。采用TCP技术来通知判题机。

## 架构详解
测评模块仅提供了安全稳定的程序运行稳定，但是并不能判断程序是否通过，因此还要自己完成许多的逻辑工作。本系统的测评模块分为两部分，一部分是测评服务器，负责分发测评任务，另一部分是测评机，负责运行程序和提交测评结果。程序在运行过程中难免会消耗系统资源，如果只有一个判题程序在判题，如果判题时间较长，会导致后面的题目无法得到及时的反馈，但是如果太多判题程序同时运行，会导致系统资源消耗过大，导致前端和后台系统可能无法正确运行，所以要设计一个能够在多个机器上运行的判题程序，实现均衡负载功能，因此本OJ测评模块示意图如下：

![测评模块示意图](/img/faq/db3.png)

利用了数据库的事务管理，可使得高并发得以实现。用户相当于生产者，不断地向数据库提交待测评列表，测评服务器相当于一个消费者，不断的从数据库中获取未判提交列表，然后将这些题目分发到准备就绪的判题机，判题机收到判题任务后会进入忙状态，此时判题服务器不再向该判题机发送判题任务。当判题机判题完毕，会告诉服务器，可以继续判题。服务器再将该判题机纳入空闲列表。这样我们就能实现多个判题机同时运行，且这些判题机可以在任意的机器上运行，只需要通过TCP协议，链接到服务器上即可。同时服务器被设计成多线程的形式，在通过资源锁去控制并发的资源访问，使得多个判题程序能同时判题。 测评服务器，测评服务器使用Python开发，运行时会循环监听9906端口，一旦有测评机连上服务器，会新建一个线程，专门处理该测评机的消息。该线程首先会向测评机发送getstatus信息，测评机收到消息后会向服务器发送ok信号，代表已准备好判题。此时服务器会将该测评机纳入空闲列表。然后不断地循环发送getstatus信号，如果是not ok，代表非空闲状态，会将该测评机纳入非空闲列表。同时会有一个线程专门负责向数据库获取未判题列表，然后将未判题发放给空闲的判题机进行判题。


## 额外功能

由于历史原因和出于安全性的考虑，需要通过额外的程序来实现将比赛中的题目的权限设置为**可访问**，即将比赛中的题目访问权限设置为**私密**，这里将这个功能集成到了判题服务器的代码里。实际上这一部分可以独立出来运行。

## 源码解析

```py
# coding=utf-8

mutex = threading.Lock()  # 队列资源锁
queue = Queue()

# 链接数据库
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
 

# 不断地从数据库中获取未判题列表
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


# 将未判题分发给每一个判题机
def deal_client(newSocket: socket, addr):
    global mutex, queue
    statue = False
    cursor = db.cursor()
    falsetime = 0
    while True:
        sleep(1)
        if mutex.acquire():
            try:
                if statue == True and queue.empty() is not True:
                    id = queue.get()
                    statue = False
                    cursor.execute(
                        "SELECT language from judgestatus_judgestatus where id = '%d'" % (id))
                    data = cursor.fetchall()
                    print(data[0][0])
                    newSocket.send(("judge|%d" % id).encode("utf-8"))
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
                        if falsetime >= 120: # 超时重启
                            newSocket.send("timeout".encode("utf-8"))
                            print(addr, "timeout!")
                            newSocket.close()
                            mutex.release()
                            return
                    print(addr, statue)

            except socket.error:
                newSocket.close()
                mutex.release()
                
                return
            except:
                print("error!")
                mutex.release()
                
                return
            mutex.release()


# 定义服务器
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", judgerjson["server_port"]))
server.listen(20)
print("server is running!")

# 开启一个线程来获取未判题
t = threading.Thread(target=getSubmition, args=())
t.setDaemon(True)
t.start()


# 自动设置比赛中的题目为auth=3，比赛结束自动设置auth=1，这一部分可以独立出来运行
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
            print("curcontest", curcontest)
            for eid in endcontest:
                cursor.execute(
                    "SELECT * from contest_contestproblem where contestid=%d" % eid)
                pros = cursor.fetchall()
                for pid in pros:
                    print(pid[2])
                    curpro.remove(pid[2])
                    curinpro.remove(pid[2])
                    cursor.execute(
                        "UPDATE  problem_problemdata SET auth = 1 WHERE problem = %s" % pid[2])
                    cursor.execute(
                        "UPDATE  problem_problem SET auth = 1 WHERE problem = %s" % pid[2])
                db.commit()
            curcontest = getcontest
            mutex.release()

# 开启一个线程来运行
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
```