FROM swift:5.1
MAINTAINER linzecong
ADD . ./Judger
WORKDIR /Judger
RUN apt-get update
RUN mv /usr/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages
RUN ln -s dist-packages /usr/lib/python2.7/site-packages
RUN apt-get install python2.7 -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get install mysql-server -y 
RUN apt-get install mysql-client -y
RUN apt-get install libatomic1 -y
RUN apt-get install libssl-dev -y
RUN apt-get install libz-dev -y
RUN apt install pkg-config -y
RUN apt install net-tools -y
RUN apt install nano -y
RUN apt-get install iputils-ping -y
RUN apt-get install libmysqlclient-dev -y
RUN pip3 install -r requirements.txt
RUN apt-get install time -y
RUN apt-get install cmake -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install libseccomp-dev -y && mkdir build && cd build && cmake /Judger && make && make install && cd .. && cd JudgerCore && python3 setup.py install
CMD ["python3", "main.py"]
