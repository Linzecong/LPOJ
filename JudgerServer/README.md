# 判题服务器部署

## Docker部署
非专业用户不推荐使用Docker单独部署

首先修改配置文件，setting.json里的东西都要修改为你的ip
``` 
cd JudgerServer
nano setting.json
```
接着运行容器
```
docker build -t lpojjudgerserver .
docker run -d -p 9906:9906 lpojjudgerserver
```

## 一般部署
首先修改配置文件
``` 
cd JudgeServer
nano setting.json
```
修改对应的数据库IP和端口保存退出
```
pip install mysqlclient
sudo python main.py
```