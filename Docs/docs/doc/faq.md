
# OJ常见问题

## 不想使用SFTP

如果你不想使用SFTP咋办？

因为有的服务器不支持或者觉得不安全！

那么你可以修改docker-comopse.yml中的 NO_DOWNLOAD 为yes，

yes则不使用sftp


但是你就需要手动将数据压缩包放到Judger/ProblemData中

注意！！每一个判题机所以在的服务器都要放！这样就不能分布式判题了~！因为每次更改数据文件，都需要对每一个判题机的数据进行更新。当然，如果你只有一个判题机，那还是很方便的

这里可用Rsync服务优化！但是作者真的太懒了！

## OJ判题安全吗？

使用的都是青岛大学提供的沙箱！这个要问他们了~！

## 添加题目失败

可能是数据库不一致导致的！自行进入数据库，检查problem_problem表和problem_peoblemdata表的题目数据是否一致！

目前这个bug已经修复，但是仍有触发的可能~

如果真的遇到，可以加群咨询

## 注册提示已注册，但是登录不了

可能是数据库不一致导致的！自行进入数据库，检查user_user表和user_userdata表的用户数据是否一致！

目前这个bug已经修复，但是仍有触发的可能~

如果真的遇到，可以加群咨询


## 支持封榜吗？

准备支持了！！


## 提交数据卡住怎么办

在浏览器按F12，刷新页面，然后重新提交，看看报什么错误

一般来说不会卡住，如果一直上传失败，可以自行把数据文件放到后台的数据文件夹中

/Backend/ProblemData 中

限500M大小，太大了请减少体积

## 测评机卡住了怎么办

一般不会卡住！

检查是不是数据太多的原因！

如果开启了OI模式，会对所有样例都判一次。假如你设置5S超时，刚好有个人提交一份超时的代码。假设你有100组数据。那么你就要跑500S！！！！所以要精简数据量，或者在比赛中关闭OI模式

如果使用Docker部署的话，崩了会自动重启的

## OJ太慢了怎么办？

后台是异步多进程多线程的！如果是数据库太慢，请使用自己的数据库，自行修改数据库地址等！

或者加大设备！在不同设备上跑Judger

## 我想独立部署多个Judger怎么办

把docker-compose.yml文件中除judger以外的内容全部删除。

然后修改各种参数即可

如可参考如下

```yml
version: '2'
services:
  
  judger:
    image: ccr.ccs.tencentyun.com/lpoj/judger
    command: >
      /bin/bash -c '
      sleep 65 ;
      python3 main.py
      '

    environment:
      DB_PASSWORD: "123456" # 必须修改！！
      DB_HOST: "111.111.111.111" # 必须修改！！
      DB_USER: 'root' # 必须修改！！
      DB_PORT: 3306 # 必须修改！！

      SERVER_IP: "111.111.111.112" # 必须修改！！
      SFTP_PORT: 22

      
      SFTP_IP: "172.17.0.1" # 必须修改，不能写127.0.0.1或localhost，必须写你的局域网地址或者公网地址
      SFTP_USER: 'ubuntu' # 必须修改
      SFTP_PASSWORD: 'ubuntuubuntu' # 必须修改
      BACKEND_PATH: "/home/ubuntu/LPOJ/Backend/" # 必须修改
      NO_DOWNLOAD: "no" # 设为yes，则不使用sftp，需要手动将数据压缩包放到Judger/ProblemData中

    restart: always
    volumes:
        - "./Judger/ProblemData:/Judger/ProblemData"
    
```


## 前端加载太慢怎么办

自行优化！我已经优化不动了！

或者使用CDN

自己申请域名

自己做个代理转发




