# 部署判题服务器

## 一般部署
首先修改配置文件
``` 
cd JudgeServer
nano setting.json
```
修改对应的数据库IP和端口，用户名和密码保存退出

需要数据库模块支持！如已安装可跳过

```
sudo apt-get install libmysqlclient-dev

pip install mysqlclient
```
最后运行
```
sudo python main.py
```

## Docker 部署

非专业用户不推荐使用Docker单独部署

首先修改配置文件，setting.json
``` 
cd JudgerServer
nano setting.json
```
接着运行容器
```
docker build -t lpojjudgerserver .
docker run -d -p 9906:9906 lpojjudgerserver
```