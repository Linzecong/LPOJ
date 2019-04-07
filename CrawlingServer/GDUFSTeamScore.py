# coding=utf-8

import MySQLdb
import json

myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')


cursor = db.cursor()
cursor.execute("SELECT * from board_teamboard")
datas = cursor.fetchall()

lastteamdata = []

for data in datas:
    lastteamdata.append({"name": data[1], "score": data[2], "rank": 0})


lastteamdata = sorted(lastteamdata, key=lambda a: a["score"], reverse=True)

for i, data in enumerate(lastteamdata):
    lastteamdata[i]["rank"] = i+1

# print(lastteamdata)

problemcount = int(input("请输入本次比赛的题目总数："))

newteamdata = []

for data in lastteamdata:
    aclist = []
    actime = []
    walist = []
    watime = []

    for i in range(problemcount):
        wa = input(data["name"]+"组："+chr(i+ord('A')) +
                   " 题WA（包括任何算罚时的错误）了吗？没有输入0，有则输入WA的数量：")
        ac = input(data["name"]+"组："+chr(i+ord('A')) +
                   " 题AC了吗？没有输入0，有则输入00:10:10格式的时间：")
        if ac != "0":
            aclist.append(chr(i+ord('A')))
            actime.append(ac)
            if wa != "0":
                walist.append(chr(i+ord('A')))
                watime.append(int(wa))

    newteamdata.append({"name": data["name"], "aclist": aclist,
                        "walist": walist, "actime": actime, "watime": watime})

    cursor.execute("INSERT INTO board_dailycontestboard(contestdate,teammember,problemcount,wronglist,wrongtime,aclist,actime) VALUES(%s,%s,%s,%s,%s,%s,%s) ", ("2019-04-04",data["name"], str(
        problemcount), '|'.join(str(i) for i in walist), '|'.join(str(i) for i in watime), '|'.join(str(i) for i in aclist), '|'.join(str(i) for i in actime)))


# print(newteamdata)

# 这里开始是积分算法
problemscore = []
problemac = []

# print(len(newteamdata))

for i in range(problemcount):
    count = 0
    for data in newteamdata:
        if chr(i+ord('A')) in data["aclist"]:
            count = count + 1
    # print(count)
    problemac.append(count)
    print(chr(i+ord('A'))+" 题分数为：", 500+500*(len(newteamdata)-count))
    problemscore.append(500+500*(len(newteamdata)-count))

# print(problemac)
# print(problemscore)


teamscore = dict()
for data in newteamdata:
    teamscore[data["name"]] = 0

# 计算每一道题每个人的得分
for i in range(problemcount):

    if problemac[i] == 0:
        continue

    acrank = []  # ac顺序

    for data in newteamdata:
        if chr(i+ord('A')) in data["aclist"]:
            for j, d in enumerate(data["aclist"]):
                if d == chr(i+ord('A')):
                    acrank.append(
                        {"name": data["name"], "time": data["actime"][j]})

    acrank = sorted(acrank, key=lambda a: a["time"])
    # print(acrank)

    for index, d in enumerate(acrank):
        teamscore[d["name"]] = teamscore[d["name"]] + \
            (problemscore[i] - (problemscore[i]/problemac[i]/2.0)*index)
        # print(teamscore[d["name"]])
        if index == 0:  # 一血加分
            teamscore[d["name"]] = teamscore[d["name"]] + problemscore[i]/100


# 计算每一道题每个人的扣分
for i in range(problemcount):

    for data in newteamdata:
        if chr(i+ord('A')) in data["walist"]:
            for j, d in enumerate(data["walist"]):
                if d == chr(i+ord('A')):
                    teamscore[data["name"]] = teamscore[data["name"]
                                                        ] - 50 * min(data["watime"][j], 10)


teamscorefinal = []
teamscoreava = 0.0

for i in teamscore.keys():
    teamscorefinal.append({"name": i, "score": teamscore[i]})
    teamscoreava = teamscoreava + teamscore[i]

teamscoreava = float(teamscoreava) / float(len(teamscorefinal))

teamscorefinal = sorted(teamscorefinal, key=lambda a: a["score"], reverse=True)

# print(teamscorefinal)
# print(teamscoreava)


D = []
for i, data in enumerate(teamscorefinal):

    S = len(teamscorefinal) * (data["score"]-teamscorefinal[-1]["score"])/(
        teamscorefinal[0]["score"] - teamscorefinal[-1]["score"])

    E = 0
    score = 0

    for d in lastteamdata:
        if d["name"] == data["name"]:
            score = float(d["score"])

    for d in lastteamdata:
        if d["name"] == data["name"]:
            continue
        E = E + (1.0/(1.0 + pow(10, float(d["score"]-score)/400)))

    K = (data["score"] / teamscoreava)

    lastrank = 0
    lastscore = 0

    for da in lastteamdata:
        if da["name"] == data["name"]:
            lastrank = da["rank"]
            lastscore = da["score"]

    P = (lastrank/len(teamscorefinal))

    # print(K+P,S,E,S-E)

    D.append(20*(K+P+S-E))
    print(data["name"]+" 本次比赛得分： "+str(int(data["score"]))+"  Raiting变化："+str(round(20*(K+P+S-E))) + "  ......  " +
          str(lastscore)+" ---> " + str(round(lastscore+20*(K+P+S-E))))

    cursor.execute("UPDATE  board_teamboard  SET score = %s where teammember = %s", (
        str(round(lastscore+20*(K+P+S-E))), data["name"]))

db.commit()
