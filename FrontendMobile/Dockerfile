FROM node
MAINTAINER linzecong
ADD . ./FrontendMobile
WORKDIR /FrontendMobile
RUN apt-get update
RUN npm install
RUN npm run build
RUN apt-get install nginx -y
EXPOSE 8081
ADD default.conf /etc/nginx/sites-available/default
CMD ["nginx", "-g", "daemon off;"]