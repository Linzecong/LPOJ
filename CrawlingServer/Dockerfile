FROM python:3.7.2
MAINTAINER linzecong
ADD . .
WORKDIR /
RUN pip install feedparser
RUN apt-get install libmysqlclient-dev -y && pip install mysqlclient
CMD ["python", "main.py"]
