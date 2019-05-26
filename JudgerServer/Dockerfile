FROM python:3.7.2
MAINTAINER linzecong
ADD . ./JudgerServer
WORKDIR /JudgerServer
RUN pip install -r requirements.txt
EXPOSE 9906
CMD ["python", "main.py"]
