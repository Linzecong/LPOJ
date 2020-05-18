
# 感谢 QingdaoU/Judger

# 原项目链接 https://github.com/QingdaoU/Judger


## Docker部署
非专业用户不推荐使用Docker单独部署

首先修改配置文件，setting.json里的东西都要修改为你的ip
``` 
cd Judger
nano setting.json
```
接着运行容器
```
docker build -t lpojjudger .
docker run -d lpojjudger
```

## 一般部署

首先修改配置文件，setting.json里的东西都要修改为你的ip

如果你需要Python判题，那么请注意修改python_path 

你可以使用 whereis python 命名查看python路径


``` 
cd Judger
nano setting.json
```

##### 安装步骤
    1. sudo apt-get install libseccomp-dev
    2. mkdir build && cd build && cmake .. && make && sudo make install
    3. cd ..
    4. cd JudgerCore
    5. sudo python setup.py install
    6. pip install paramiko
    7. pip install mysqlclient

###### 运行
    1. sudo python main.py

# 详细测试
    参考 https://github.com/QingdaoU/Judger 中的 unittest

# 参数解释

## result 
    WAITING = -6
    PRESENTATION_ERROR = -5
    COMPILE_ERROR = -4
    WRONG_ANSWER = -3
    PENDING = -1
    JUDGINNG = -2
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5

## error 
    SUCCESS = 0
    INVALID_CONFIG = -1
    FORK_FAILED = -2
    PTHREAD_FAILED = -3
    WAIT_FAILED = -4
    ROOT_REQUIRED = -5
    LOAD_SECCOMP_FAILED = -6
    SETRLIMIT_FAILED = -7
    DUP2_FAILED = -8
    SETUID_FAILED = -9
    EXECVE_FAILED = -10
    SPJ_ERROR = -11 (judger module will never return this value, it's used for awswer checker)