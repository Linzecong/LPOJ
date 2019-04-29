# LPOJ     （先点个赞呗）
[![Python](https://img.shields.io/badge/python-3.7.2-green.svg?style=flat-square)](https://www.python.org/downloads/release/python-372/)
[![Django](https://img.shields.io/badge/django-2.1.5-green.svg?style=flat-square)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/django_rest_framework-3.9.1-green.svg?style=flat-square)](http://www.django-rest-framework.org/)
> 一个基于Vue.js和Django的轻量级在线评测系统

> 目前应用于广东外语外贸大学
## Demo地址：[www.lpoj.cn](http://www.lpoj.cn)
## 说明文档：[docs.lpoj.cn](http://docs.lpoj.cn)
## 简述
+ 轻量级，易于部署和自定义定制
+ 前后端分离，提高服务器性能
+ 支持多进程判题，判题更高效
+ 支持 C/C++和Java语言
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

## 部署（判题程序仅能部署在Linux系统，推荐将所有东西部署在同一个服务器中）
#### 前端部署
```
cd Frontend
npm install
npm run-script build
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
    server_name www.lpoj.cn;  # 此处填写你的域名或IP
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

至此，前端部署完毕。**如要进行OJ二次开发，请参阅[文档](http://docs.lpoj.cn)**

#### 后端与数据库部署
首先安装Mysql数据库
然后以UTF-8编码新建数据库 lpoj 
然后按顺序安装Django，如已安装，可跳过

1. 首先安装Django
```
pip install django

pip install djangorestframework

pip install django-filter

sudo apt-get install python-django

pip install django-cors-headers
```
2. 安装数据库，已安装的可跳过
```
sudo apt-get install libmysqlclient-dev

pip install mysqlclient

sudo apt-get install mysql-server 

为了能公网访问，可以执行以下数据库语句
CREATE DATABASE LPOJ DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'  IDENTIFIED BY 'you_password'  WITH GRANT OPTION;
flush privileges;

然后
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf 
修改bind-address 为 0.0.0.0
```
3. 部署后端
```
cd Backend

cd Backend

sudo nano setting.py
//修改数据库配置为你自己的数据库IP和用户名密码

cd ..

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
```
4. 安装sftp服务（不安装无法判题,一般云服务器会自动安装）
```
sudo apt-get install openssh-server
sftp user@ip //验证是否安装成功！
```
然后添加sftp账户和密码等，具体操作自行查阅sftp相关信息.


#### 部署判题服务器
首先修改配置文件
``` 
cd JudgeServer
nano setting.json
```
修改对应的数据库IP和端口保存退出
```
sudo python main.py
```

#### 部署判题机
首先修改配置文件，setting,json里的东西都要修改为你的ip，其中sftp应配置为你的后端服务器
``` 
cd Judger
nano setting.json

//然后运行判题机，支持多个运行
sudo python main.py
//必须添加sudo，然后不同判题机，必须要用不同的名字命名。
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