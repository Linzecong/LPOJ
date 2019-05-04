FROM python:3.7.2
MAINTAINER linzecong
ADD . ./Backend
WORKDIR /Backend
ENV DB_PASSWORD "lpojdatabase"
ENV DB_HOST "lpojdatabase"
ENV DB_USER 'root'
ENV DB_PORT 3306
RUN apt-get update && pip install django && pip install djangorestframework && pip install django-filter && apt-get install python-django -y && pip install django-cors-headers
RUN pip install mysqlclient
EXPOSE 8000
CMD python manage.py makemigrations && python manage.py makemigrations judgestatus problem user contest board blog wiki  && python manage.py migrate  && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell && python manage.py runserver 0.0.0.0:8000 
