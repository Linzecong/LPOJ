
# GDUFS OJ

# 我的毕业设计

# 项目架构

## 服务器1

**前端采用** vue.js

**后端采用** django RESTful framework

**数据库** mysql

## 服务器2 (可部署多个以提高性能)

**JudgerServer** python tcp + docker


## 服务器3  (可部署多个以提高性能)
**Judger** python tcp + docker



后端直接向数据库提交数据和获取数据

JudgerServer不断的从数据库中获取未判题的列表（使用TCP通讯）（仅进行通知操作）

并通知各个Judger进行判题并将结果通过后端保存到数据库

文件数据保存在DataServer目录,后端将数据文件保存到DataServer，然后解压缩！


