FROM python:3.7.2
MAINTAINER linzecong
ADD . ./Judger
WORKDIR /Judger
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install tar -y
RUN apt-get install clang -y
RUN apt-get install python3 -y
RUN apt-get install time -y
RUN apt-get install cmake -y
RUN apt-get install openjdk-8-jdk -y
RUN apt-get install libseccomp-dev -y && mkdir build && cd build && cmake /Judger && make && make install && cd .. && cd JudgerCore && python setup.py install
RUN pip install -r requirements.txt
RUN wget https://swift.org/builds/swift-5.1-release/ubuntu1804/swift-5.1-RELEASE/swift-5.1-RELEASE-ubuntu18.04.tar.gz
RUN tar xzf swift-5.1-RELEASE-ubuntu18.04.tar.gz -C /
RUN echo "export PATH=/swift-5.1-RELEASE-ubuntu18.04/usr/bin:"${PATH}"" >> /profile
RUN /bin/bash -c "source /profile"
CMD ["python", "main.py"]
