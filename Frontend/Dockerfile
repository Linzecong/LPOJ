FROM node
MAINTAINER linzecong
ADD . ./Frontend
WORKDIR /Frontend
RUN apt-get update
ADD default.conf /etc/nginx/conf.d/default.conf
RUN npm install
RUN npm run-script build
RUN apt-get install nginx -y
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]