# LPOJ
[![Python](https://img.shields.io/badge/python-3.7.2-success.svg?style=flat-round)](https://www.python.org/downloads/release/python-372/)
[![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-3.9.1-success.svg?style=flat-round)](http://www.django-rest-framework.org/)
[![vue](https://img.shields.io/badge/vue-2.5.2-success.svg?style=flat-round)](https://github.com/vuejs/vue)
[![travis-ci](https://travis-ci.org/Linzecong/LPOJ.svg?branch=master)](https://travis-ci.org/Linzecong/LPOJ)
[![Join-QQ-Group](https://img.shields.io/badge/Join_QQ_Group-875136693-blue.svg?style=flat-round)](https://shang.qq.com/wpa/qunwpa?idkey=dcc9d5c63a744d5c09eda5dd7f4b208451e66b42ba633ea23ec6fa4d49135825)

> 一个基于Vue.js和Django的轻量级在线评测系统
>
> 目前应用于广东外语外贸大学
## 演示地址：[oj.lpoj.cn](https://oj.lpoj.cn)
## 说明文档：[docs.lpoj.cn](https://docs.lpoj.cn)

## 简述
+ 轻量级，易于部署和自定义定制
+ 前后端分离，提高服务器性能
+ 支持多机器多进程判题，判题更高效
+ 支持 C/C++/Java/Python2/Python3和Swift5.1语言
+ 支持 Special Judge和选择题判题
+ 丰富的API，开放的源代码
+ 一键保存和导出代码模板
+ **支持类似LeetCode的模板题判题功能**
+ **新增班级管理与布置作业功能**
+ 现代化的界面 + 手机适配
+ 实时爬取自定义用户的博客和其他OJ的做题数
+ 丰富的算法知识和体系化的套题训练

## 模块列表
+ [前端 Vue.js](https://github.com/Linzecong/LPOJ/tree/master/Frontend)
+ [手机前端 Vue.js](https://github.com/Linzecong/LPOJ/tree/master/FrontendMobile)
+ [后端 Djangorestframework](https://github.com/Linzecong/LPOJ/tree/master/Backend)
+ [判题服务器 Python](https://github.com/Linzecong/LPOJ/tree/master/JudgerServer)
+ [判题程序 Python](https://github.com/Linzecong/LPOJ/tree/master/Judger)
+ [爬虫程序 Python](https://github.com/Linzecong/LPOJ/tree/master/CrawlingServer)


## 使用Docker部署

### 环境准备

### 1. 安装必要的依赖
```
sudo apt-get update
sudo apt-get install -y git
sudo apt install docker.io -y
sudo apt install docker-compose -y
```
### 2. 开始安装

```
git clone https://github.com/Linzecong/LPOJ.git && cd LPOJ
```

**请修改docker-compose.yml中的数据库密码（所有的 DB_PASSWORD，MYSQL_ROOT_PASSWORD 字段）和一些你认为必要的设置**


```
sudo docker-compose up -d --scale judger=3
```

以上命令默认开启3个判题机，可以自行修改数量


根据网速和配置情况，大约10到20分钟就可以自动搭建完成，全程无需人工干预。

等命令执行完成，然后运行 **sudo docker ps -a** 当看到所有的容器的状态均为 Up 就代表 OJ 已经启动成功。

### 3. 准备工作

1. 安装成功后，先通过IP:8080访问OJ，注册一个用户

2. 然后进入 IP:8000/admin 以用户名admin 密码admin 登录后台（请及时修改后台密码，这个后台作用仅用于修改管理员权限，因此没有样式）

3. 修改User表中，你注册的超级用户的type为3，使得你注册的用户变为超级管理员

4. 以管理员登录，右上角进入管理员页面，然后在网站设置标签，提交一次设置

### 4. 更新OJ

如要更新OJ只需在LPOJ目录下执行如下步骤
```
git pull # 如果你修改了代码，自行解决merge得到情况
sudo docker-compose stop
sudo docker-compose pull
sudo docker-compose up -d --scale judger=3
```

**容器运行时产生的数据会保存在对应的文件夹中，如数据库文件，题目数据等**

## 自定义OJ

首先先下载源代码
```
git clone https://github.com/Linzecong/LPOJ.git && cd LPOJ
```

然后随意修改你要修改的地方，修改完毕后，使用如下命令重新部署

```
sudo docker-compose -f docker-compose-build.yml up -d --build --scale judger=3
```

同样的，您需要修改**docker-compose-build.yml**中的配置，详见**开始安装**

由于会重新构建整个系统，而不是拉去已构建好的镜像，所以花的时间会比较长~请耐心等待

网站的静态文件可以放在 ./Frontend/dist/img中，比如存放题目所用的图片


## 如无意外，部署成功！
具体使用，请参阅使用[文档](https://docs.lpoj.cn)

## 更新日志

3.3 更新类似LeetCode的模板题功能

3.4 更新班级管理和布置作业功能，可以在比赛中添加选择题

## 代办功能

1. 封榜功能
2. 更优秀的排行榜显示（现在人数多了会卡）

## 部分截图

![image1](https://www.lpoj.cn/githubimage/image1.png)

![image2](https://www.lpoj.cn/githubimage/image2.png)

![image3](https://www.lpoj.cn/githubimage/image3.png)

![image4](https://www.lpoj.cn/githubimage/image4.png)

![image5](https://www.lpoj.cn/githubimage/image5.png)

![image6](https://www.lpoj.cn/githubimage/image6.png)

或者你可以直接访问我们  [oj.lpoj.cn](https://oj.lpoj.cn)

## 浏览器支持

Modern browsers(chrome, firefox)

## 特别感谢

+ 广东外语外贸大学ACM集训队所有成员
+ 广东外语外贸大学集训队所有老师
+ [青岛大学在线评测系统](https://github.com/QingdaoU/OnlineJudge)
+ [24OI/OI-wiki](https://github.com/24OI/OI-wiki)



## 许可

The [MIT](http://opensource.org/licenses/MIT) License