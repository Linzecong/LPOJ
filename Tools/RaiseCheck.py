



import MySQLdb
from queue import Queue
import socket
import json
from time import sleep
import threading
import os


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


cursor = db.cursor()

cursor.execute("SELECT user, code from judgestatus_judgestatus")
data = cursor.fetchall()

raisenum = {}

for d in data:
    id = str(d[0])
    code = str(d[1])
    raisenum[id] = 0 

for d in data:
    id = str(d[0])
    code = str(d[1])
    raisenum[id] = max(raisenum[id], code.count("raise"))

li = sorted(raisenum.items(), key=lambda item:item[1],reverse=True)

file = open("raisenum.txt", "w")

for l in li:
    file.write(l[0]+"  "+str(l[1])+'\n')
    print(l[0]+"  "+str(l[1]))
    

            
