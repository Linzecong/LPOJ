


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


curcontest = set()
curpro = set()
curinpro = set()
cursor = db.cursor()

cursor.execute(
    "SELECT * from contest_contestinfo where type <> 'Personal' and TO_SECONDS(NOW()) - TO_SECONDS(begintime) <= lasttime")
data = cursor.fetchall()
getcontest = set()
for d in data:
    id = int(d[0])  # 用于求结束的比赛
    
    

            
