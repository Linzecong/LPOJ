# 部署判题机

判题机支持多个且异地部署

## 一般部署
修改配置文件
``` 
cd Judger
nano setting.json
```
修改对应的数据库IP和端口，用户名和密码

修改server_ip为你的判题服务器的IP地址

修改sftp_ip为你的后端IP地址，同时修改登录的用户名和密码为你的后端服务器的用户名和密码

修改backend_path为你的后端文件夹地址（用于下载数据）

需要数据库模块支持！如已安装可跳过

```
pip install mysqlclient
```
 安装依赖库
```
sudo apt-get install libseccomp-dev
mkdir build && cd build && cmake .. && make && sudo make install
cd ..
cd JudgerCore
sudo python setup.py install
cd ..
pip install paramiko
sudo apt install time
```

 安装Java环境
```
sudo apt install openjdk-8-jdk
```


最后运行
```
sudo python main.py
```

## Docker 部署

非专业用户不推荐使用Docker单独部署

首先修改配置文件，setting.json里的东西都要修改为你的ip，其中sftp应配置为你的后端服务器的用户名和密码和ip
``` 
cd Judger
nano setting.json
```
接着运行容器
```
docker build -t lpojjudger .
docker run -d lpojjudger
```