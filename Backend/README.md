# 后端与数据库部署
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

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
```