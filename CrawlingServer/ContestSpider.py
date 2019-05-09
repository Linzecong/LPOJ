
import MySQLdb
import json
from time import sleep
from urllib import request
import datetime
import time

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')


cursor = db.cursor()

cursor.execute("truncate table contest_contestcominginfo")
db.commit()


for i in range(3):
    ss = (datetime.datetime.now()+datetime.timedelta(days=30*i)).strftime('%Y-%m')

    url = 'https://ac.nowcoder.com/acm/calendar/contest?token=&month='+ ss
    head = {}
        #写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.168 Safari/537.36'
    req = request.Request(url, headers=head)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')

    datajson = json.loads(html)

    for d in datajson["data"]:
        print(d)
        cursor.execute("INSERT INTO contest_contestcominginfo(ojName,link,startTime,endTime,contestName) SELECT %s, %s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT * FROM contest_contestcominginfo WHERE contestName= %s)",
                            (d["ojName"], d['link'], d['startTime'], d['endTime'], d['contestName'], d['contestName']))

    db.commit()