import xlrd
import time

def subString(template):
    template = template.strip()
    copy = False
    finished = False
    slotList = []
    str = ""
    for s in template:
        if s=='(':
            copy = True
        elif s==')':
            copy = False
            finished = True
        elif copy:
            str = str+s
        if finished:
            slotList.append(str)
            str = ""
            finished = False
    return slotList[0]

class MyXlsx:
    
    def __init__(self,file):
        self.ExcelFile=xlrd.open_workbook(file)
        self.ExcelSheetNames=self.ExcelFile.sheet_names()
        self.ExcelSheets = self.ExcelFile.sheets()
        self.SheetDatas = []
        for sheet in self.ExcelSheets:
            
            rows = sheet.nrows
            cols = sheet.ncols
            data = {}
            data["row"]=rows
            data["col"]=cols
            data["merged"]=sheet.merged_cells
            data["name"]=sheet.name
            data["data"]=[]
            
            for i in range(rows):
                data["data"].append(sheet.row(i))

            self.SheetDatas.append(data)


wenjian = input("请输入文件路径：") # C:\Users\50460\Desktop\2.xls
xls = MyXlsx(wenjian)

#print(xls.SheetDatas[0])

import MySQLdb
import json


myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')


cursor = db.cursor()
cursor.execute( "SELECT * from board_teamboard")
datas = cursor.fetchall()
lastteamdata = []

for data in datas:
    lastteamdata.append({"name":data[1],"score":data[2],"rank":0})

lastteamdata = sorted(lastteamdata,key=lambda a:a["score"],reverse=True)

for i,data in enumerate(lastteamdata):
    lastteamdata[i]["rank"]=i+1

print(lastteamdata)



problemcount = xls.SheetDatas[0]["col"]-1

inputstr = []
inputstr.append(str(problemcount))


for data in lastteamdata:
    for d in range(xls.SheetDatas[0]["row"]):
        print(str(d)+" : "+xls.SheetDatas[0]["data"][d][0].value)
    row = int(input(data["name"]+" 对应的序号为："))

    for j in range(problemcount):
        coldata = xls.SheetDatas[0]["data"][row]
        wacount = 0
        text = str()
        text = str(coldata[j+1].value)
        if text.find("(") >=0 and text.find(":") >=0:
            wacount = subString(text)
            wacount = int(wacount)
            wacount = -wacount
        inputstr.append(str(wacount))

        actime = 0
        if text.find(":") >=0:
            actime = text[0:8]
        inputstr.append(str(actime))

cursor.execute("SELECT * from board_teamboard")
datas = cursor.fetchall()

lastteamdata = []

for data in datas:
    lastteamdata.append({"name": data[1], "score": data[2], "rank": 0})


lastteamdata = sorted(lastteamdata, key=lambda a: a["score"], reverse=True)

scorerank = dict()

for index,i in enumerate(lastteamdata):
    if scorerank.get(i["score"],'~') == '~':
        scorerank[i["score"]] = index + 1

for i, data in enumerate(lastteamdata):
    lastteamdata[i]["rank"] = scorerank[data["score"]]


# print(lastteamdata)

ini = 0
problemcount = int(inputstr[ini])
ini =ini +1

newteamdata = []

for data in lastteamdata:
    aclist = []
    actime = []
    walist = []
    watime = []

    for i in range(problemcount):
        wa = int(inputstr[ini])
        ini=ini+1
        ac = inputstr[ini]
        ini=ini+1
        if ac != "0":
            aclist.append(chr(i+ord('A')))
            actime.append(ac)
            if wa != 0:
                walist.append(chr(i+ord('A')))
                watime.append(int(wa))

    newteamdata.append({"name": data["name"], "aclist": aclist,
                        "walist": walist, "actime": actime, "watime": watime})

    cursor.execute("INSERT INTO board_dailycontestboard(contestdate,teammember,problemcount,wronglist,wrongtime,aclist,actime) VALUES(%s,%s,%s,%s,%s,%s,%s) ", (time.strftime('%Y-%m-%d',time.localtime(time.time())),data["name"], str(
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

