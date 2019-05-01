# 后端与数据库部署

## 一般部署

### 部署数据库

首先安装Mysql数据库

> 如果自己已经安装了数据库的，可以跳过本步骤

```
sudo apt-get install mysql-server
```
然后新建数据库
```
CREATE DATABASE LPOJ DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
如果要公网访问，可以执行以下数据库语句
```
mysql -uroot -p

mysql > GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'  IDENTIFIED BY 'you_password'  WITH GRANT OPTION;
mysql > flush privileges;
然后修改配置文件（不同系统可能在不同地方）
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf 
修改bind-address 为 0.0.0.0
```

### 部署后端

按顺序安装Django，如已安装，可跳过

1. 首先安装Django
```
pip install django

pip install djangorestframework

pip install django-filter

sudo apt-get install python-django

pip install django-cors-headers
```
2. 安装python数据库操作类
```
sudo apt-get install libmysqlclient-dev

pip install mysqlclient
```

3. 部署后端
```
cd Backend

cd Backend

sudo nano setting.py
```

**修改数据库配置为你自己的数据库IP端口和用户名密码**

```
cd ..

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
```

### 添加超级用户
```
# 首先在前端中注册一个普通账户，然后进入数据库
mysql -uroot -p

mysql > UPDATE user_user SET type=3 WHERE username = yourusername;
```


### 部署SFTP服务
不安装无法判题,一般云服务器会自动安装

```
sudo apt-get install openssh-server
sftp user@ip //验证是否安装成功！
```
然后添加sftp账户和密码等，具体操作自行查阅SFTP相关信息.

## Docker 部署
一键部署，更加方便快捷！以后再写！