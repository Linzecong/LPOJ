# 前端部署

## Docker部署
非专业用户不推荐使用Docker单独部署
修改nginx.conf中proxy_pass的地址为你的后端地址，如有需要，可以修改其他配置

```
docker build -t lpojfrontend .
docker run -d -p 80:80 lpojfrontend
```

## 一般部署

```
cd Frontend
npm install
npm run build
```
编译完毕后，网站文件保存在dist目录中，接下来部署到服务器中
+ 推荐使用Nginx
```
sudo apt-get install nginx
```
将dist文件夹中的文件复制到Web服务器目录中（默认根目录 **/var/www/html/**）
接下来修改Nginx配置文件（不同版本可能在不同的地方）
```
sudo nano /etc/nginx/nginx.conf
```
主要修改如下几个配置
1. 路由重定向
2. API重定向

将如下配置复制到http{}中
```
server{
    listen 80;
    server_name www.lpoj.cn;  # 此处填写你的域名或IP地址
    root /var/www/html;   # 此处填写你的网页根目录
    location /api {  # 将API重定向到后台服务器（如果你修改了前端中的代理配置，这里需要对应的修改）
        rewrite ^.*api/?(.*)$ /$1 break;
        proxy_pass http://localhost:8000; # 填写你的后端地址和端口
    }
    location / {  # 路由重定向以适应Vue中的路由
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```
其他配置请自行参考Nginx配置

至此，前端部署完毕。**如要进行OJ二次开发，请参阅[文档](http://docs.lpoj.cn)**