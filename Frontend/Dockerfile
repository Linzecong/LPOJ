FROM node AS build

# for cn user yun can use below to speed up 
# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && apt-get clean

RUN apt-get update

MAINTAINER linzecong
ADD . ./Frontend
WORKDIR /Frontend

RUN npm install 
# for cn user yun can use below instead to speed up 
# RUN npm install --registry https://registry.npm.taobao.org

RUN npm run build

FROM nginx

COPY --from=build /Frontend /Frontend
WORKDIR /Frontend
RUN mkdir ../del &&\
    mv ./* ../del &&\
    mv ../del/dist ./ &&\
    mv ../del/nginx.conf ./ &&\
    rm -rf ../del

ADD nginx.conf /etc/nginx/nginx.conf