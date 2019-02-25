# 记得把mysql设置成支持中文

# 安装步骤
pip install django

pip install djangorestframework

pip install django-filter

sudo apt-get install python-django

pip install django-cors-headers

sudo apt-get install libmysqlclient-dev

pip install mysqlclient

**可选** sudo apt-get install mysql-server 
**可选**  登录数据库后执行 CREATE DATABASE LPOJ DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

 python manage.py makemigrations

python manage.py migrate

**可选** python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000