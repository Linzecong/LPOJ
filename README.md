
# GDUFS OJ

# 我的毕业设计

# 项目架构

## 服务器1

**前端采用** vue.js

**后端采用** django RESTful framework

## 服务器2 (可部署多个以提高性能)

**JudgerServer** python tcp + docker

**DataServer** django + docker

**Judger** python tcp + docker

## 服务器3

**数据库** mysql




后端直接向数据库提交数据和获取数据

JudgerServer不断的从数据库中(通过后端)获取未判题的列表（使用TCP通讯）（仅进行通知操作）

并通知各个Judger进行判题并将结果通过后端保存到数据库

文件数据保存在DataServer,前端将数据文件发送到DataServer



