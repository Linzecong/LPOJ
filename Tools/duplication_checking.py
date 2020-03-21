#!/usr/bin/env python3

# 自行查看攻略！ https://dickgrune.com/Programs/similarity_tester/

import MySQLdb
import sys
import os

args = sys.argv
if len(args) == 2:
    contestid = args[1]
else:
    print("usage: %s <ContestId>" % args[0])
    exit(-1)

###############################################################################
db = MySQLdb.connect(
     host="localhost",    # 主机名
     user="root",         # 数据库用户名
     passwd="",           # 数据库密码
     db="LPOJ")           # 数据库名称
###############################################################################

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
	else:
		print ("There is this folder ----> contest_{0}".format(contestid))

#创建比赛文件夹
pwd  = os.getcwd()
# folder_name = pwd + '/' + 'contest_duplication_checking' #总文件夹
folder_name = './' + 'contest_duplication_checking' #总文件夹
if not os.path.exists(folder_name):
    mkdir(folder_name)
# filename =  pwd + '/' + 'contest_duplication_checking' + '/' + 'contest_' + contestid
filename =  './' + 'contest_duplication_checking' + '/' + 'contest_' + contestid
mkdir(filename) #每个比赛分开


# 查询前，必须先获取游标
cur = db.cursor()

#每个参赛者创建代码文件夹
cur.execute("SELECT * FROM judgestatus_judgestatus WHERE result = '0'")
namelist = []
for row in cur.fetchall():
    if row[1] not in namelist:
        namelist.append(row[1])
        user_code_file = filename + '/' + row[1]
        mkdir(user_code_file)

#把代码写成txt
for names in namelist:
    cur.execute("SELECT * FROM judgestatus_judgestatus WHERE result = '0' AND user = '{0}'".format(names))
    cnt = 0
    for row in cur.fetchall():
        code_file = filename + '/' + row[1] + '/' + row[1] + '_' + str(cnt)
        cnt = cnt + 1
        # if(os.path.exists(folder_name)):
        #     print ("There is this file ----> ",row[1] + '_' + str(cnt))
        # else :
        f = open(code_file + ".txt","w")
        f.write(row[13])

#查重
for names in namelist:
    present_code_list = []
    others_code_list = []
    nameindex = namelist.index(names) + 1


    command = 'ls -l '+ filename + '/' + names + '| wc -l'
    filecount = os.popen(command).read()
    filecount = int(filecount) - 1
    for num in range(0,filecount):
        present_code_list.append(filename + '/' + names + '/' + names + '_' + str(num))

    for names2 in namelist[nameindex:]:
        command2 = 'ls -l '+ filename + '/' + names2 + '| wc -l'
        filecount2 = os.popen(command).read()
        filecount2 = int(filecount) - 1

        for num2 in range(0,filecount):
            others_code_list.append(filename + '/' + names2 + '/' + names2 + '_' + str(num2))

    for first_code in present_code_list:
        for second_code in others_code_list:
            dc = 'sim_c.exe -p ' + first_code +'.txt '+ second_code + '.txt'
            dc_result = os.popen(dc).read()
            b = dc_result.split()
            if "%" in b:
                first_name = b[1].split("/")
                second_name = b[9].split("/")
                print(first_name[4],'与',second_name[4],'相似度',b[29]+"%")


db.close()
