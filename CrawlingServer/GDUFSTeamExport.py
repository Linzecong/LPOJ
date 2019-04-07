import xlrd


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
cursor.execute( "SELECT * from board_teamboard where collecttime='2019-04-04'")
datas = cursor.fetchall()
lastteamdata = []

for data in datas:
    lastteamdata.append({"name":data[1],"score":data[2],"rank":0})

lastteamdata = sorted(lastteamdata,key=lambda a:a["score"],reverse=True)

for i,data in enumerate(lastteamdata):
    lastteamdata[i]["rank"]=i+1

print(lastteamdata)

file = open("1.in","w")

problemcount = xls.SheetDatas[0]["col"]-1

file.write(str(problemcount)+'\n')

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
        file.write(str(wacount)+'\n')

        actime = 0
        if text.find(":") >=0:
            actime = text[0:8]
        file.write(str(actime)+'\n')

file.close()




