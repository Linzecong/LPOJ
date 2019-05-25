# LPOJ
[![Python](https://img.shields.io/badge/python-3.7.2-success.svg?style=flat-round)](https://www.python.org/downloads/release/python-372/)
[![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-3.9.1-success.svg?style=flat-round)](http://www.django-rest-framework.org/)
[![vue](https://img.shields.io/badge/vue-2.5.2-success.svg?style=flat-round)](https://github.com/vuejs/vue)
[![travis-ci](https://travis-ci.org/Linzecong/LPOJ.svg?branch=master)](https://travis-ci.org/Linzecong/LPOJ)

> 一个基于Vue.js和Django的轻量级在线评测系统
>
> 目前应用于广东外语外贸大学
## Demo地址：[www.lpoj.cn](http://www.lpoj.cn)
## 说明文档：[docs.lpoj.cn](http://docs.lpoj.cn)
## 简述
+ 轻量级，易于部署和自定义定制
+ 前后端分离，提高服务器性能
+ 支持多机器多进程判题，判题更高效
+ 支持 C/C++/Java和Python3语言
+ 丰富的API，开放的源代码
+ 实时爬取用户的博客和其他OJ的做题数
+ 丰富的算法知识和体系化的套题训练
+ 一键保存和导出代码模板
+ 包含类CF的积分体系和比赛机制

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
docker-compose up -d
```
根据网速和配置情况，大约10到20分钟就可以自动搭建完成，全程无需人工干预。

等命令执行完成，然后运行 **docker ps -a** 当看到所有的容器的状态均为 Up 就代表 OJ 已经启动成功。

> 安装成功后，先通过IP:80访问OJ，注册一个用户
> 
> 然后进入 IP:8000/admin 以用户名admin 密码admin 登录后台（请及时修改后台密码）
> 
> 修改User表中，你注册的超级用户的type为3，使得你注册的用户变为超级管理员

**容易运行时产生的数据会保存在对应的文件夹中，如数据库文件，题目数据等**

### 一般部署

#### 前端部署
```
cd Frontend
npm install
npm run build
```
编译完毕后，网站文件保存在dist目录中，接下来部署到服务器中
+ 推荐使用Nginx
```
sudo apt-get install nginx
```
将dist文件夹中的文件复制到Web服务器目录中（默认根目录 **/var/www/html/**）
接下来修改Nginx配置文件（不同版本可能在不同的地方）
```
sudo nano /etc/nginx/nginx.conf
```
主要修改如下几个配置
1. 路由重定向
2. API重定向

将如下配置复制到http{}中
```
server{
    listen 80;
    server_name www.lpoj.cn;  # 此处填写你的域名或IP地址
    root /var/www/html;   # 此处填写你的网页根目录
    location /api {  # 将API重定向到后台服务器（如果你修改了前端中的代理配置，这里需要对应的修改）
        rewrite ^.*api/?(.*)$ /$1 break;
        proxy_pass http://localhost:8000; # 填写你的后端地址和端口
    }
    location / {  # 路由重定向以适应Vue中的路由
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```
其他配置请自行参考Nginx配置

至此，前端部署完毕。**如要进行OJ二次开发，请参阅[文档](http://docs.lpoj.cn)**

#### 后端与数据库部署

1. 首先安装Django
```
pip install django

pip install djangorestframework

pip install django-filter

sudo apt-get install python-django

pip install django-cors-headers

pip install mysqlclient
```
2. 安装数据库，已安装的可跳过
```
sudo apt-get install mysql-server 

mysql -uroot -p
mysql > CREATE DATABASE LPOJ DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
mysql > USE mysql
mysql > GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'  IDENTIFIED BY 'your_password'  WITH GRANT OPTION;
mysql > ALTER user 'root'@'%' IDENTIFIED WITH mysql_native_password by 'your_password';
mysql > flush privileges;

sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf 

#修改bind-address 为 0.0.0.0
```
3. 部署后端
```
cd Backend

cd Backend

sudo nano setting.py
# 修改数据库配置为你自己的数据库IP和用户名密码

cd ..

python manage.py makemigrations

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.filter(email=\"admin@example.com\").delete(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")" | python manage.py shell

python manage.py runserver 0.0.0.0:8000
```
4. 安装sftp服务（不安装无法判题,一般云服务器会自动安装）
```
sudo apt-get install openssh-server
sftp yourusername@localhost # 验证是否安装成功！
```
5. 添加管理员
> 安装成功后，先通过IP:80访问OJ，注册一个用户
> 
> 然后进入 IP:8000/admin 以用户名admin 密码admin 登录后台（请及时修改后台密码）
> 
> 修改User表中，你注册的超级用户的type为3，使得你注册的用户变为超级管理员


#### 部署判题服务器
首先修改配置文件
``` 
cd JudgeServer
nano setting.json
```
修改对应的数据库IP和端口保存退出
```
pip install mysqlclient
sudo python main.py
```

#### 部署判题机
首先修改配置文件，setting.json里的东西都要修改为你的ip，其中sftp应配置为你的后端服务器的用户名和密码和ip
``` 
cd Judger
nano setting.json
```

##### 安装步骤
    1. sudo apt-get install libseccomp-dev
    2. mkdir build && cd build && cmake .. && make && sudo make install
    3. cd ..
    4. cd JudgerCore
    5. sudo python setup.py install
    6. pip install paramiko
    7. pip install mysqlclient

##### 运行
    1. sudo python main.py

#### 爬虫机器人（可选）
主要用于爬取学生的博客和大OJ的做题数
``` 
cd CrawlingServer
nano setting.json
# 修改对应的数据库IP和端口保存退出
pip install feedparser
pip install mysqlclient
sudo python main.py
```

## 如无意外，部署成功！
具体使用，请参阅使用[文档](http://docs.lpoj.cn)

## 浏览器支持

Modern browsers(chrome, firefox)

## 特别感谢

+ 广东外语外贸大学ACM集训队所有成员
+ 广东外语外贸大学集训队所有老师
+ [青岛大学在线评测系统](https://github.com/QingdaoU/OnlineJudge)
+ [24OI/OI-wiki](https://github.com/24OI/OI-wiki)



## 许可

The [MIT](http://opensource.org/licenses/MIT) License