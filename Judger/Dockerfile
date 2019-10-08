FROM swift:5.1
MAINTAINER linzecong
ADD . ./Judger
WORKDIR /Judger
RUN apt-get update
RUN apt-get install python3 -y
RUN alias python=python3
RUN alias pip=pip3
RUN apt-get install python3-pip -y
RUN apt-get install time -y
RUN apt-get install cmake -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install libseccomp-dev -y && mkdir build && cd build && cmake /Judger && make && make install && cd .. && cd JudgerCore && python3 setup.py install
RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]
