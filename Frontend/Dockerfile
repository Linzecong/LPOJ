FROM node:13.10-slim
MAINTAINER linzecong
ADD . ./Frontend
WORKDIR /Frontend
RUN apt-get update
RUN npm install
RUN npm run build
RUN apt-get install nginx -y

RUN rm -rf /Frontend/node_modules

EXPOSE 80
ADD nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]