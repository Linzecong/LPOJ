FROM node
MAINTAINER linzecong
ADD . ./Frontend
WORKDIR /Frontend
RUN apt-get update
RUN npm install
RUN npm run build
RUN apt-get install nginx -y
EXPOSE 80
ADD nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]