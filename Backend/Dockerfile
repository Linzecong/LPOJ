FROM python:3.7.2
MAINTAINER linzecong
ADD . .
WORKDIR /
RUN pip install django && pip install djangorestframework && pip install django-filter && apt-get install python-django -y && install django-cors-headers
RUN apt-get install libmysqlclient-dev -y && pip install mysqlclient
EXPOSE 8000-8000
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
