# 前端部署

## 一般部署

首先要先安装 npm ，具体安装教程，自行百度（要先安装node.js）

安装完毕后，依次执行以下命令（以LPOJ文件夹为根目录）
由于需要安装依赖，可能会话比较多的时间。

```
cd Frontend
npm install
npm run-script build
```

等待npm编译前端，编译成功后可以在前端中的dist文件夹找到编译成功后的静态文件。接下来我们只要把那些文件，扔到Web服务器中即可。Web服务器随意，我这里使用的是Nginx，也推荐使用Nginx。首先让我们先安装Nginx

```
sudo apt-get install nginx
```
这样就安装成功了
我们将编译成功的dist文件夹下的所有内容，拖到Nginx的默认网站根目录中（通常是/var/www/html）

Win下推荐使用WinSCP进行拖放操作！

接下来我们要修改Nginx的配置文件（不同版本可能在不同的地方）
```
sudo nano /etc/nginx/nginx.conf
```

主要修改如下几个配置

1. 路由重定向
2. API重定向


将如下配置复制到 **http{}** 中
```
server{
    listen 80;
    server_name www.lpoj.cn;  # 此处填写你的域名或IP
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

Nginx的配置多种多样，比如说开启Gzip支持等等，这些东西大家随意配置就好，具体的配置可以自行百度。

修改完后记得重启服务
```
sudo systemctl restart nginx
```

如无意外，可以在浏览器中访问你的前端了。试一试localhost~

## Docker 部署

以后更新！