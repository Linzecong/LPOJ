
import MySQLdb
import json
from time import sleep

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')

data = open("./contest.json", 'r',encoding='UTF-8')
datajson = json.loads(data.read())

cursor = db.cursor()

cursor.execute("truncate table contest_contestcominginfo")
db.commit()

for d in datajson["data"]:
    print(d)
    cursor.execute("INSERT INTO contest_contestcominginfo(ojName,link,startTime,endTime,contestName) SELECT %s, %s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT * FROM contest_contestcominginfo WHERE contestName= %s)",
                        (d["ojName"], d['link'], d['startTime'], d['endTime'], d['contestName'], d['contestName']))

db.commit()