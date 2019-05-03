FROM python:3.7.2
MAINTAINER linzecong
ADD . .
WORKDIR /
RUN pip install mysqlclient
EXPOSE 9906
CMD ["python", "main.py"]
