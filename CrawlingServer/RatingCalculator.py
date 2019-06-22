import MySQLdb
import json


myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')

contestid = int(input("请输入比赛编号："))

cursor = db.cursor()

cursor.execute(
    "SELECT UNIX_TIMESTAMP(begintime)*1000,title from contest_contestinfo where id = %d" % contestid)

a = cursor.fetchone()

ContestBeginTime = int(a[0])
contestname = str(a[1])

cursor.execute(
    "SELECT * from contest_contestboard where contestid = %d" % contestid)


userdata = []

nameset = set()
namevis = dict()

datas = cursor.fetchall()

for data in datas:
    nameset.add(data[2])
    namevis[data[2]] = 0

FB = []
FBTime = []
for i in range(0, 26):
    FB.append("!!!")
    FBTime.append(5552304570991)
for name in nameset:
    username = name
    if namevis[username] == 1:
        continue
    namevis[username] = 1

    PaticipantData = {
        "user": username,
        "score": 0
    }

    Score = 0

    ProblemDataList = []
    for i in range(0, 26):
        ProblemDataList.append([5552304570991, 0])

    for res in datas:
        if res[2] == username:
            if int(res[5]) == 1:
                if int(res[6]) < ProblemDataList[res[4]][0]:
                    ProblemDataList[res[4]][0] = int(res[6])

    for res in datas:
        if res[2] == username:
            if int(res[5]) == 0:
                if int(res[6]) < ProblemDataList[res[4]][0]:
                    ProblemDataList[res[4]][1] = ProblemDataList[res[4]][1] - 1

    for ii in range(0, 26):

        ProblemScore = 0
        if ii == 0:
            ProblemScore = 200
        elif ii == 1:
            ProblemScore = 500
        else:
            ProblemScore = (ii-1)*500

        if ProblemDataList[ii][0] != 5552304570991:

            ACTime = ProblemDataList[ii][0]
            FaShiNum = ProblemDataList[ii][1]

            if ACTime < FBTime[ii]:
                FBTime[ii] = ACTime
                FB[ii] = username

            cha = (ACTime - ContestBeginTime)/1000

            Score += ProblemScore - ((cha/60.0*(0.7/(ii+1)))/100.0*ProblemScore)

            Score += 20 * FaShiNum

    PaticipantData["score"] = max(0, Score)
    userdata.append(PaticipantData)

for i in range(0, 26):
    ProblemScore = 0
    if i == 0:
        ProblemScore = 200
    elif i == 1:
        ProblemScore = 500
    else:
        ProblemScore = (i-1)*500

    if FB[i] != "!!!":
        for ii, d in enumerate(userdata):
            if d["user"] == FB[i]:
                userdata[ii]["score"] += ProblemScore/10
                break

userdata = sorted(userdata, key=lambda a: a["score"], reverse=True)

scoreava = 0
for d in userdata:
    scoreava = scoreava + d["score"]
scoreava = scoreava / len(userdata)

lastdata = []
for d in userdata:
    cursor.execute(
        "SELECT rating from user_userdata where username = '%s'" % d["user"])
    lastdata.append({"user": d["user"], "rating": int(cursor.fetchone()[0])})

lastdata = sorted(lastdata, key=lambda a: a["rating"], reverse=True)

scorerank = dict()

for index, i in enumerate(lastdata):
    if scorerank.get(i["rating"], '~') == '~':
        scorerank[i["rating"]] = index + 1

for i, data in enumerate(lastdata):
    lastdata[i]["rank"] = scorerank[data["rating"]]


D = []
for i, data in enumerate(userdata):

    S = len(userdata) * (data["score"]-userdata[-1]["score"])/(
        userdata[0]["score"] - userdata[-1]["score"])

    E = 0
    score = 0

    for d in lastdata:
        if d["user"] == data["user"]:
            score = float(d["rating"])

    for d in lastdata:
        if d["user"] == data["user"]:
            continue
        E = E + (1.0/(1.0 + pow(10, float(d["rating"]-score)/400)))

    K = (data["score"] / scoreava)

    lastrank = 0
    lastscore = 0

    for da in lastdata:
        if da["user"] == data["user"]:
            lastrank = da["rank"]
            lastscore = da["rating"]

    P = (lastrank/len(userdata))

    # print(K+P,S,E,S-E)

    D.append(20*(K+P+S-E))
    print(data["user"]+" 本次比赛得分： "+str(int(data["score"]))+"  Raiting变化："+str(round(20*(K+P+S-E))) + "  ......  " +
          str(lastscore)+" ---> " + str(round(lastscore+20*(K+P+S-E))))

    if str(round(lastscore+20*(K+P+S-E))) == "1500":
        lastscore = lastscore +1
    cursor.execute("UPDATE  user_userdata  SET rating = %s where username = %s", (
     str(round(lastscore+20*(K+P+S-E))), data["user"]))
    cursor.execute("INSERT INTO contest_contestratingchange(contestid,contestname,contesttime,user,lastrating,ratingchange,currentrating) VALUES('%s','%s','%s','%s','%s','%s','%s') " % (
     str(contestid), str(contestname), str(ContestBeginTime), data["user"],str(lastscore),str(round(20*(K+P+S-E))),str(round(lastscore+20*(K+P+S-E)))))


db.commit()
