# LPOJ
[![Python](https://img.shields.io/badge/python-3.7.2-success.svg?style=flat-round)](https://www.python.org/downloads/release/python-372/)
[![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-3.9.1-success.svg?style=flat-round)](http://www.django-rest-framework.org/)
[![vue](https://img.shields.io/badge/vue-2.5.2-success.svg?style=flat-round)](https://github.com/vuejs/vue)
[![travis-ci](https://travis-ci.org/Linzecong/LPOJ.svg?branch=master)](https://travis-ci.org/Linzecong/LPOJ)
[![Join-QQ-Group](https://img.shields.io/badge/Join_QQ_Group-875136693-blue.svg?style=flat-round)](https://shang.qq.com/wpa/qunwpa?idkey=dcc9d5c63a744d5c09eda5dd7f4b208451e66b42ba633ea23ec6fa4d49135825)

> 一个基于Vue.js和Django的轻量级在线评测系统
>
> 目前应用于广东外语外贸大学
## Demo地址：[www.lpoj.cn](https://www.lpoj.cn)
## 说明文档：[docs.lpoj.cn](https://docs.lpoj.cn)

## 简述
+ 轻量级，易于部署和自定义定制
+ 前后端分离，提高服务器性能
+ 支持多机器多进程判题，判题更高效
+ 支持 C/C++/Java和Python3语言
+ 支持 Special Judge
+ 丰富的API，开放的源代码
+ 实时爬取用户的博客和其他OJ的做题数
+ 丰富的算法知识和体系化的套题训练
+ 一键保存和导出代码模板
+ 包含类CF的积分体系和比赛机制
+ 现代化的界面

## 模块列表
+ [前端 Vue.js](https://github.com/Linzecong/LPOJ/tree/master/Frontend)
+ [后端 Djangorestframework](https://github.com/Linzecong/LPOJ/tree/master/Backend)
+ [判题服务器 Python](https://github.com/Linzecong/LPOJ/tree/master/JudgerServer)
+ [判题程序 Python](https://github.com/Linzecong/LPOJ/tree/master/Judger)
+ [爬虫程序 Python](https://github.com/Linzecong/LPOJ/tree/master/CrawlingServer)

## 部署（两种方式）

### 使用Docker部署
#### 环境准备
1. 安装必要的依赖
```
sudo apt-get update
sudo apt-get install -y git
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt-get install openssh-server -y
sftp yourusername@localhost # 验证是否安装成功！
```
2. 开始安装
```
git clone https://github.com/Linzecong/LPOJ.git && cd LPOJ
# 如有需要，修改docker-compose.yml中的数据库密码（DB_PASSWORD，MYSQL_ROOT_PASSWORD）
# 必须修改docker-compose.yml中的BACKEND_PATH,SFTP_USER,SFTP_PASSWORD为你的LPOJ/Backend文件夹的绝对路径和服务器的用户名密码
sudo docker-compose up -d
```
根据网速和配置情况，大约10到20分钟就可以自动搭建完成，全程无需人工干预。

等命令执行完成，然后运行 **docker ps -a** 当看到所有的容器的状态均为 Up 就代表 OJ 已经启动成功。

> 安装成功后，先通过IP:8080访问OJ，注册一个用户
> 
> 然后进入 IP:8000/admin 以用户名admin 密码admin 登录后台（请及时修改后台密码）
> 
> 修改User表中，你注册的超级用户的type为3，使得你注册的用户变为超级管理员

3. 更新OJ

如要更新OJ只需在LPOJ目录下执行如下步骤
```
sudo docker stop $(sudo docker ps -aq)
git pull
sudo docker-compose pull
sudo docker-compose up -d
```

**容易运行时产生的数据会保存在对应的文件夹中，如数据库文件，题目数据等**

### 一般部署

+ [后端](https://github.com/Linzecong/LPOJ/tree/master/Backend)
+ [前端](https://github.com/Linzecong/LPOJ/tree/master/Frontend)
+ [判题服务器](https://github.com/Linzecong/LPOJ/tree/master/JudgerServer)
+ [判题机](https://github.com/Linzecong/LPOJ/tree/master/Judger)
+ [爬虫机器人](https://github.com/Linzecong/LPOJ/tree/master/CrawlingServer)

## 如无意外，部署成功！
具体使用，请参阅使用[文档](https://docs.lpoj.cn)

## 部分截图

![image1](https://www.lpoj.cn/githubimage/image1.png)

![image2](https://www.lpoj.cn/githubimage/image2.png)

![image3](https://www.lpoj.cn/githubimage/image3.png)

![image4](https://www.lpoj.cn/githubimage/image4.png)

![image5](https://www.lpoj.cn/githubimage/image5.png)

![image6](https://www.lpoj.cn/githubimage/image6.png)

或者你可以直接访问我们  [www.lpoj.cn](https://www.lpoj.cn)

## 浏览器支持

Modern browsers(chrome, firefox)

## 特别感谢

+ 广东外语外贸大学ACM集训队所有成员
+ 广东外语外贸大学集训队所有老师
+ [青岛大学在线评测系统](https://github.com/QingdaoU/OnlineJudge)
+ [24OI/OI-wiki](https://github.com/24OI/OI-wiki)



## 许可

The [MIT](http://opensource.org/licenses/MIT) License