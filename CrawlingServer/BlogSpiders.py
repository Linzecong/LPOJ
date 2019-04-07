# coding=utf-8

import feedparser
import MySQLdb
import json
from time import sleep

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')


while True:
    cursor = db.cursor()
    cursor.execute("SELECT * from board_board")
    datas = cursor.fetchall()

    users = dict()
    print("Start!!")
    for d in datas:
        if d[8] != "":
                users[d[0]] = d[8]

    for user in users.items():
        username = user[0]
        address = user[1]
        fp = feedparser.parse(address)
        for e in fp.entries:
                title = e.title
                url = e.links[0].href
                summary = e.summary
                time = e.published
                cursor.execute("INSERT INTO blog_blog(username,title,url,summary,time) SELECT %s, %s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT * FROM blog_blog WHERE username = %s and title= %s)",
                        (username, title, url, summary, time, username, title))
        db.commit()
        print(user, " Done!")
    sleep(3600)
