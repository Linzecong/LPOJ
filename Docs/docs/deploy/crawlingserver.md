# 爬虫机器人部署

主要用于爬取学生的博客和大OJ的做题数

## 一般部署

``` 
cd CrawlingServer
nano setting.json
# 修改对应的数据库IP和端口保存退出
pip install feedparser
pip install mysqlclient
sudo python main.py
```


## Docker部署

首先修改配置文件，setting.json里的东西都要修改为你的ip
``` 
cd CrawlingServer
nano setting.json
```
接着运行容器
```
docker build -t lpojcrawlingserver .
docker run -d lpojcrawlingserver