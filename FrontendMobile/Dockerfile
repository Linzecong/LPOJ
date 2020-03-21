FROM node:13.10-slim
MAINTAINER linzecong
ADD . ./FrontendMobile
WORKDIR /FrontendMobile
RUN apt-get update
RUN npm install
RUN npm run build
RUN apt-get install nginx -y
RUN rm -rf /Frontend/node_modules

EXPOSE 8081
ADD nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]