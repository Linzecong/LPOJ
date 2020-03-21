FROM python:3.7.2
MAINTAINER linzecong
ADD . ./Backend
WORKDIR /Backend
ENV DB_HOST "lpojdatabase"
ENV DB_PASSWORD "lpojdatabase"
ENV DB_USER 'root'
ENV DB_PORT 3306
RUN apt-get update && apt-get install python-django -y
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py makemigrations && python manage.py makemigrations judgestatus item problem user contest board blog wiki classes && python manage.py migrate  && echo "from django.contrib.auth.models import User; User.objects.filter(email=\"admin@example.com\").delete(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")" | python manage.py shell && gunicorn -w 5 --bind 0.0.0.0:8000 -k 'gevent' Backend.wsgi:application
 
