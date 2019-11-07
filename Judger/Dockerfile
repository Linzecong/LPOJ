FROM swift:5.1
MAINTAINER linzecong
ADD . ./Judger
WORKDIR /Judger
RUN apt-get update
RUN apt-get install python -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get install mysql-server -y 
RUN apt-get install mysql-client -y
RUN apt-get install libmysqlclient-dev -y
RUN pip3 install -r requirements.txt
RUN apt-get install time -y
RUN apt-get install cmake -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install libseccomp-dev -y && mkdir build && cd build && cmake /Judger && make && make install && cd .. && cd JudgerCore && python setup.py install
CMD ["python3", "main.py"]
