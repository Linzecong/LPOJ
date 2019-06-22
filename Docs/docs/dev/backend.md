# 后端开发

后端的开发比前端的开发要简单很多，因为开发者只需专注于数据的呈现即可，不必关心显示的逻辑。在众多后端框架中，我选择了开发和学习成本较低的Python语言中的Django框架，同时Python语言与我们的判题程序又相辅相成，因此是一个很好的选择。Django是一个开源的Web框架，整体采用MVC的设计模式。但是在本系统中，我们并不需要构建自己的前端页面，我们只关心有哪些数据要交付给前端，因此本系统采用Django中的REST框架来快速构建自己的数据API。其中REST是RESTful的简称。RESTful是一种软件架构风格，它采用http协议，非常简单，任意客户端都能运行。因此我们只需要关心有哪些数据要交付给前端即可。其中REST框架主要分为三个部分，分别是Model,Serializer和View。Model即数据层，定义了数据在数据库中的形式。Serializer即序列化器，其中定义了各种数据库的操作，相当于一个中间层，最后View层决定了哪些数据可以呈现给用户，怎么呈现给用户等等。所以当开发者编写API时，只要着重于实现这三层即可。因为有了RESTful框架，这一切都变得非常简单便利。

![RESTful 示意图](/img/faq/db2.png)

## Django REST framework 介绍
现在越来越多的网站采用前后端分离技术。在前后端分离的应用模式中，后端仅返回前端所需要的数据，不再渲染HTML页面，不再控制前端的效果。前端用户想要看到什么效果，从后端请求的数据如何加载到前端中，都由前端浏览器自己决定。在前后端分离的应用模式中,前端与后端的耦合度相对较低，我们通常将后端开发的每一视图都成为一个接口,或者API,前端通过访问接口来对数据进行增删改查。因此我们采用它进行我们的后端开发，同时他配套有各种各样的服务，如权限管理，路由管理，限流等等，这些在我们的判题系统中尤为重要。

因此本系统采用Django REST framework 开发，接下来跟着我的步伐，一步一步了解Django是如何在LPOJ中运作的！

## 安装Python3.7
整个开发在Ubuntu 18.10环境下进行，接下来所有教程均在此环境下进行，如果是Windows，请自行查阅安装方法。

Ubuntu自带Python3.6，经测试3.6一样适合本环境。但是Ubuntu中，Python命令默认是Python2，所以我们可以通过如下命令改变默认值，当然你也可以不改变，然后每次执行Python命令时使用的命令应该是Python3

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 100
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150
```

如果要还原到Python2，执行：
```bash
sudo update-alternatives --config python
```

接下来我们安装 pip ，pip是Python的一个包管理工具，可以使你很方便的下载Python的一些包，我们通过如下命令即可安装

```bash
sudo apt install python3-pip
```

## 安装必要环境

如若你要二次开发本OJ，首先要配置环境。

本后端主要用了如下几个库

1. Django==2.2.1
2. djangorestframework==3.9.3
3. django-filter==2.1.0
4. django-cors-headers==2.5.3
5. mysqlclient==1.4.2.post1

其中第一个是整个Django框架所需的库，第二个是我们的REST Framework，第三个是用于实现过滤功能的一个框架，第四个是用于实现跨域访问的框架，第五个是访问Mysql所需要的库。

我们进入到Backend目录并执行如下命令即可。

```bash
pip3 install -r requirements.txt
```

如果在安装过程中出现错误，请自行百度错误信息并解决。
如果安装mysqlclient出现 **/bin/sh: 1: mysql_config: not found**错误，请执行如下语句：
```bash
sudo apt-get install libmysqlclient-dev
```

如无意外，应该会安装成功！

## 安装Mysql

其他操作请自行百度。

```bash
sudo apt-get install mysql-server
```
安装成功后我们新建一下数据库和修改一些配置。我们登录到数据库中然后执行如下语句。

```SQL
mysql -uroot -p
mysql > CREATE DATABASE LPOJ DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
mysql > USE mysql
mysql > GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'  IDENTIFIED BY 'your_password'  WITH GRANT OPTION;
mysql > ALTER user 'root'@'%' IDENTIFIED WITH mysql_native_password by 'your_password';
mysql > flush privileges;
mysql > exit;
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf 
```
具体内容的意思就是新建一个名为LPOJ的数据库，并给予root用户所有权限。

## 编辑setting.py

接下来我们修改一下配置文件，我们进入到Backend/Backend目录下，并修改setting.py文件
```bash
cd Backend
cd Backend
nano setting.py
```

我们主要修改数据库的配置信息，我们找到如下语句并修改else后面的内容为你的数据库信息。
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LPOJ',
        'USER': os.environ.get("DB_USER")  if os.environ.get("DB_USER") else 'root' , # 修改root为你的数据库用户
        'PASSWORD':os.environ.get("DB_PASSWORD")  if os.environ.get("DB_PASSWORD") else 'lpojdatabase', # 修改lpojdatabase为你的数据库密码
        'HOST': os.environ.get("DB_HOST")  if os.environ.get("DB_HOST") else 'lpojdatabase',# 修改lpojdatabase为你的数据库IP地址，如localhost
        'PORT': os.environ.get("DB_PORT")  if os.environ.get("DB_PORT") else 3306,
    }
}
```

## 运行后端

在Backend根目录中的manager.py是Django非常重要的一个文件，通过它我们可以实现很多操作，比较常用的操作如下：

**makemigrations** 将你编写的代码变成sql语句
**migrate** 将你编写的sql语句同步到数据库中
**runserver** 运行你的后端

首先将LPOJ的后端代码生成mysql语句，然后我们再同步到数据库中
```bash
python manager.py makemigrations
python manager.py migrate
```
执行完毕后查看数据库，会发现你的LPOJ数据库中多了若干表格，这些都是Django运行所需要的表格。


在运行之前让我们先制作一个超级用户，这在部署文档里面有写
```bash
echo "from django.contrib.auth.models import User; User.objects.filter(email=\"admin@example.com\").delete(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin\")" | python manage.py shell
```

最后我们再执行运行语句，以后如果对后端有任何修改，只需先执行
```bash
python manager.py makemigrations
python manager.py migrate
```
将修改同步到数据库中，然后再通过如下命令运行

```bash
python manage.py runserver 0.0.0.0:8000
```

意思是将后端暴露到8000端口中，并监听所有地址的访问。

接下来，我们就可以通过在浏览器中通过**localhost:8000**访问你的后端了。

如果能访问，证明你的后端已部署成功！

## 模块说明与开发

在阅读如下教程时，请先自行学习Django REST Framework的一些基本教程

接下在会对一些模块做简单介绍

1. Backend 保存整个后台的配置文件和路由
2. blog 博客模块
3. board 排行榜相关模块
4. contest 比赛相关模块
5. judgestatus 提交信息模块
6. problem 题目模块
7. user 用户相关模块
8. wiki Wiki模块
9. ProblemData 存放题目数据的文件夹

本教程不会对每个模块都做详细介绍，但是会列出各文件的功能，和点出一些自己的实现方法。

### Backend

#### setting.py

此处添加你自己的模块
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'judgestatus',
    'corsheaders',
    'problem',
    'user',
    'contest',
    'board',
    'blog',
    'wiki'
]
```

此处填写一下你使用的框架的设置，比如限流设置就是在此处实现。
```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '300/m',
        'judge': '300/m',
        'post': '2000/m',
    }

}
```

此处是一下数据库的设置

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LPOJ',
        'USER': os.environ.get("DB_USER")  if os.environ.get("DB_USER") else 'root' ,
        'PASSWORD':os.environ.get("DB_PASSWORD")  if os.environ.get("DB_PASSWORD") else 'lpojdatabase',
        'HOST': os.environ.get("DB_HOST")  if os.environ.get("DB_HOST") else 'lpojdatabase',
        'PORT': os.environ.get("DB_PORT")  if os.environ.get("DB_PORT") else 3306,
    }
}
```

此处是跨域访问的设置
```py
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
```

此处是Session过期设置
```py
SESSION_COOKIE_AGE = 60 * 60 * 24  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

#### urls.py

这个文件主要是用来填写路由信息

### Blog

此模块主要用来实现博客相关的API

**models.py**


| model | 功能 |
| :--  | :-- |
| Banner | 首页新闻 | 
| OJMessage | 留言板信息 | 
| Blog | 爬虫得到的博客条目 | 

**Banner**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| msg | 新闻内容 | CharField |  |
| time | 新闻时间 | DateField | auto_now |

**OJMessage**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 留言用户 | CharField |  |
| msg | 留言内容 | CharField |  |
| time | 留言时间 | DateField | auto_now |
| rating | 用户留言时的Rating | IntegerField | 用于实现前端改变颜色 |

**Blog**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 博客所属用户 | CharField |  |
| title | 博客标题 | CharField |  |
| url | 博客地址 | CharField |  |
| summary | 博客的摘要 | CharField |  |
| time | 博客的爬取时间 | CharField | 爬虫机器人直接保存时间字符串 |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| UserRatingOnly | 有 | 仅用户或为管理员，并且不能修改Rating |
| ManagerOnly | 有 | 仅管理员 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| BannerSerializer | ALL |
| OJMessageSerializer | ALL |
| BlogSerializer | ALL | 


**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| BannerView | ID倒序  | ('time') |  ManagerOnly | 是 | 否 |
| OJMessageView | ID倒序  | ('username', 'time') |  UserRatingOnly | 是 | 否 |
| BlogView | ID倒序  | ('username', 'time') |  ManagerOnly | 是 | 否 |

**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| BannerView | http://localhost:8000/banner/  | 
| OJMessageView | http://localhost:8000/ojmessage/  | 
| BlogView | http://localhost:8000/blog/ |  


### Board

此模块主要用来实现排行榜和设置相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| SettingBoard | 保存OJ的设置 | 
| Board | 用户爬虫需要的一些信息 | 
| DailyBoard | 用户每天的AC题目数统计 | 
| TeamBoard | 队伍Rating信息（该功能暂时弃用） | 
| DailyContestBoard | 队伍排位赛的一些信息，用于备份，作用不大 | 

**SettingBoard**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| schoolname | 学校名称 | CharField | 用于显示在排行榜上的学校名字 |
| ojname | OJ名称 | CharField | OJ左上角的标题 |

**Board**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | Primary_key |
| classes | 班级 | CharField |  |
| number | 学号 | CharField |  |
| OJCount | 爬虫的OJ数 | IntegerField | 无用的字段（历史遗留） |
| OJ | 爬虫的OJ | CharField | 爬虫机器人识别每个账号对应的OJ用，中间用竖线隔开 |
| account | 爬虫的账号 | CharField | 该用户OJ的账号名称，中间用竖线隔开，与OJ字段一一对应 |
| acnum | 每个OJ的AC数 | CharField | 中间用竖线隔开，与OJ字段一一对应 |
| submitnum | 每个OJ的提交数 | CharField | 中间用竖线隔开，与OJ字段一一对应 |
| blogaddress | 爬虫用的博客地址 | CharField | 用的是RSS地址 |


**DailyBoard**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField |  |
| account | 当天的总AC数量 | IntegerField | 每天仅统计一次，用于生成表格 |
| collecttime | 采集时间 | DateField |  |

**TeamBoard**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| teammember | 队伍名称 | CharField |  |
| score | 该队伍得分 | IntegerField | 由爬虫模块计算并更新 |
| collecttime | 采集时间 | DateField |  |

**DailyContestBoard**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestdate | 比赛日期 | DateField |  |
| teammember | 队伍名称 | CharField |  |
| problemcount | 题目数量 | IntegerField |  |
| wronglist | 错误的题目 | CharField | 中间用竖线隔开，如 A\|B |
| wrongtime | 错误的次数 | CharField | 与wronglist对应，如 1\|2 |
| aclist | AC的题目 | CharField | 中间用竖线隔开，如 A\|B |
| actime | AC的时间 | CharField | 与aclist对应，格式为00:00:00 |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| ManagerOnly | 有 | 仅管理员 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| SettingBoardSerializer | ALL |
| BoardSerializer | ALL | 
| DailyBoardSerializer | ALL |
| TeamBoardSerializer | ALL | 
| DailyContestBoardSerializer | ALL |

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| SettingBoardView | ALL  | 无 |  ManagerOnly | 否 | 否 |
| BoardView | ALL  | ('username',) |  ManagerOnly | 是 | 否 |
| DailyBoardView | 最近10天，正序  | ('username', 'collecttime') |  ManagerOnly | 是 | 否 |
| TeamBoardView | ALL  | ('teammember', 'collecttime') |  ManagerOnly | 是 | 否 |
| DailyContestBoardView | ALL  | ('contestdate', 'teammember') |  ManagerOnly | 是 | 否 |

**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| SettingBoardView | http://localhost:8000/settingboard/  | 
| BoardView | http://localhost:8000/board/ |  
| DailyBoardView |http://localhost:8000/dailyboard/  | 
| TeamBoardView | http://localhost:8000/teamboard/  |
| DailyContestBoardView | http://localhost:8000/dailycontestboard/  | 

### Contest

此模块主要用来实现比赛相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| ContestInfo | 比赛的基本信息 | 
| ContestAnnouncement | 比赛中的通知 | 
| ContestProblem | 比赛包含的题目 | 
| ContestBoard | 比赛排行榜信息 | 
| ContestComment | 比赛提问 | 
| ContestTutorial | 比赛题解 | 
| ContestRegister | 比赛注册的用户 | 
| ContestRatingChange | 比赛的积分变化信息 | 
| ContestComingInfo | 各大OJ近期的比赛汇总，由爬虫机器人收集 |

**ContestInfo**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| creator | 比赛举办者 | CharField |  |
| oj | 举办的OJ | CharField | 一般都是LPOJ |
| title | 比赛标题 | CharField |  |
| level | 比赛难度 | IntegerField | 1~5 |
| des | 比赛说明 | CharField |  |
| note | 比赛提示 | CharField |  |
| begintime | 比赛开始时间 | DateTimeField |  |
| lasttime | 比赛持续时间 | IntegerField | 以秒为单位 |
| type | 比赛类型 | CharField | ACM/Rated等等 |
| auth | 比赛权限 | IntegerField | 1 公开 2 私有 0 保护(需注册) |
| clonefrom | 是否属于克隆 | IntegerField | 非克隆的为-1，否则保存的是克隆的ID |


**ContestAnnouncement**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| announcement | 比赛提示信息 | CharField |  |


**ContestProblem**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| problemid | 题目ID | CharField |  |
| problemtitle | 题目标题 | CharField | 用于显示在比赛中的题目标题 |
| rank | 题目顺序 | IntegerField | 用数字表示本题目顺序 |

**ContestBoard**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| username | 该提交的用户名 | CharField |  |
| user | 该提交的用户昵称 | CharField |  |
| problemrank | 提交的题目序号ID | IntegerField | 是题目顺序的编号 |
| type | 该提交最终的结果 | IntegerField | 1 AC， 0没AC算罚时，-1没AC不算罚时 |
| submittime | 提交时间 | BigIntegerField | 提交时间，以豪秒为单位 |
| submitid | 该提交的ID | IntegerField | 用于rejudge |
| rating | 该提交用户的Rating | IntegerField | 用于前端改变颜色 |

**ContestComment**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| user | 该提交的用户名 | CharField |  |
| title | 提问标题 | CharField |  |
| problem | 提问的题目 | CharField |  |
| message | 提问的信息 | CharField |  |
| huifu | 回复的信息 | CharField | default="No respones" |
| time | 提问的时间 | DateTimeField | auto_now |
| rating | 该回复用户的Rating | IntegerField | 用于前端改变颜色 |

**ContestTutorial**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| value | 题解内容 | TextField | 支持MarkDown |

**ContestRegister**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| user | 注册的用户名 | CharField |  |
| rating | 该回复用户的Rating | IntegerField | 用于前端改变颜色 |

**ContestRatingChange**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| contestid | 比赛ID | IntegerField |  |
| contestname | 比赛标题 | CharField |  |
| contesttime | 比赛的时间 | CharField |  |
| user | 本次变化的用户名 | CharField |  |
| lastrating | 上次Rating | IntegerField |  |
| ratingchange | Rating变化量 | IntegerField |  |
| currentrating | 当前Rating | IntegerField |  |

**ContestRatingChange**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| ojName | 比赛所在的OJ | CharField |  |
| link | 比赛链接 | CharField |  |
| startTime | 比赛开始时间 | BigIntegerField | 毫秒为单位 |
| endTime | 比赛结束时间 | BigIntegerField | 毫秒为单位 |
| contestName | 比赛名称 | CharField |  |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| ManagerOnly | 有 | 仅管理员或clone的比赛已结束 |
| UserRatingOnly | 有 | 仅用户（username）或为管理员，或为PUT |
| UserRatingOnly2 | 有 | 仅用户（user）或为管理员，或为PUT |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| ContestAnnouncementSerializer | ALL |
| ContestTutorialSerializer | ALL | 
| ContestBoardSerializer | ALL |
| ContestCommentSerializer | ALL | 
| ContestInfoSerializer | ALL |
| ContestProblemSerializer | ALL | 
| ContestRegisterSerializer | ALL |
| ContestRatingChangeSerializer | ALL | 
| ContestComingInfoSerializer | ALL |

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| ContestAnnouncementView | ALL  | ("contestid",) |  ManagerOnly | 是 | 否 |
| ContestTutorialView | ALL  | ('contestid',) |  ManagerOnly | 是 | 否 |
| ContestBoardView | ALL  | ("contestid","username","problemrank","type",) |  UserRatingOnly | 否 | 否 |
| ContestCommentView | ALL  | ("contestid","problem",) |  UserRatingOnly2 | 是 | 否 |
| ContestInfoView | ID倒序  | ("begintime", "level", "type","title",) |  ManagerOnly | 是 | ('title',) |
| ContestComingInfoView | 开始时间正序  | 无 |  ManagerOnly | 是 | 否 |
| ContestProblemView | rank字段正序  | ('contestid',) |  ManagerOnly | 是 | 否 |
| ContestRegisterView | ALL  | ('user', "contestid") |  UserRatingOnly2 | 是 | 否 |
| ContestRatingChangeView | 比赛时间倒序  | ('user', "contestid") |  ManagerOnly | 是 | 否 |
| CurrentTimeView | 当前时间 | 无 |  无 | 否 | 否 |


**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| ContestAnnouncementView | http://localhost:8000/contestannouncement/  | 
| ContestTutorialView | http://localhost:8000/contesttutorial/  | 
| ContestBoardView | http://localhost:8000/settingboard/  | 
| ContestCommentView | http://localhost:8000/contestcomment/  | 
| ContestInfoView | http://localhost:8000/contestinfo/  | 
| ContestComingInfoView | http://localhost:8000/contestcominginfo/  | 
| ContestProblemView | http://localhost:8000/contestproblem/  | 
| ContestRegisterView | http://localhost:8000/contestregister/  |
| ContestRatingChangeView | http://localhost:8000/contestratingchange/  | 
| CurrentTimeView | http://localhost:8000/currenttime/ |


### Judgestatus

此模块主要用来实现提交信息相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| JudgeStatus | 提交判题的信息 | 
| CaseStatus | 每一个case的情况 | 


**JudgeStatus**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| user | 提交的用户 | CharField |  |
| oj | 提交的OJ | CharField | 用于VJudge |
| problem | 提交的题目 | CharField |  |
| result | 提交的结果 | IntegerField | 具体内容查阅Judger文档 |
| time | 时间占用 | IntegerField |  |
| memory | 内存占用 | IntegerField |  |
| length | 代码长度 | IntegerField |  |
| language | 提交语言 | CharField |  |
| submittime | 提交时间 | DateTimeField | auto_now |
| judger | 判题的判题机 | CharField |  |
| contest | 该提交所属的比赛 | IntegerField |  |
| contestproblem | 该提交所属的比赛的题目 | IntegerField |  |
| code | 提交的代码 | TextField |  |
| testcase | 在哪个样例出错 | CharField |  |
| message | 额外信息 | TextField | 保存编译错误信息，运行时错误信息等，同时也作为其他OJ的题目ID，用于VJudge |
| problemtitle | 提交的标题 | CharField |  |
| rating | 用户留言时的Rating | IntegerField | 用于实现前端改变颜色 |

**CaseStatus**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| statusid | 所属的提交ID | IntegerField |  |
| username | 所属的用户 | CharField |  |
| problem | 所属的题目 | CharField |  |
| result | 该样例的判题结果 | CharField |  |
| time | 该样例所花时间 | IntegerField |  |
| memory | 该样例所花内存 | IntegerField |  |
| testcase | 样例名称 | CharField |  |
| casedata | 样例输入截取 | CharField | 非比赛才能查看，Judger中控制 |
| outputdata | 样例输出截取 | CharField | 非比赛才能查看，Judger中控制 |
| useroutput | 用户输出截取 | CharField | 非比赛才能查看，Judger中控制 |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| ManagerOnly | 有 | 仅管理员 |
| UserRatingOnly | 无 | 仅用户或为管理员，并且不能修改Rating |
| NoContestOnly | 仅用户或比赛结束 | 有 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| JudgeStatusSerializer | 不包括代码 |
| JudgeStatusCodeSerializer | ALL | 
| CaseStatusSerializer | ALL | 

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| JudgeStatusView | ID倒序  | ('user', 'result', "contest", "problem", "language") |  ManagerOnly | 是 | 否 |
| JudgeStatusPutView | 仅用于提交代码  | 无 |  UserRatingOnly | 否 | 否 |
| JudgeStatusCodeView | ALL  | ('user', 'result', "contest", "problem") |  NoContestOnly | 是 | 否 |
| CaseStatusView | ALL  | ('username', 'problem', "statusid") |  ManagerOnly | 是 | 否 |
| RejudgeAPIView | 用于实现Rejudge  | 无 |  ManagerOnly | 否 | 否 |

**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| JudgeStatusView | http://localhost:8000/judgestatus/  | 
| JudgeStatusPutView | http://localhost:8000/judgestatusput/ |  
| JudgeStatusCodeView | http://localhost:8000/judgestatuscode/  | 
| CaseStatusView | http://localhost:8000/casestatus/ |  
| RejudgeAPIView | http://localhost:8000/rejudge/ |

### Problem

此模块主要用来实现题目相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| Problem | 题目的详细信息 | 
| ProblemData | 题目的简要信息 | 
| ProblemTag | 题目的标签 | 

**Problem**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| problem | 题目编号 | CharField | primary_key |
| author | 题目作者 | CharField |  |
| addtime | 题目添加时间 | DateTimeField | auto_now |
| oj | 题目的OJ | CharField | Vjudge用，一般是LPOJ |
| title | 题目的标题 | CharField |  |
| des | 题目的介绍 | TextField | 支持网页格式 |
| input | 输入介绍 | TextField | 支持网页格式 |
| output | 输出介绍 | TextField | 支持网页格式 |
| sinput | 样例输入 | TextField | 多个样例间用\|#)隔开 |
| soutput | 样例输出 | TextField | 多个样例间用\|#)隔开 |
| source | 题目来源 | TextField | 如果是Vjudge，填的是OJ对应的题号 |
| time | 题目限时 | IntegerField |  |
| memory | 题目内存限制 | IntegerField |  |
| hint | 提示 | TextField | 支持网页格式 |
| auth | 题目权限 | IntegerField | 1公开 2私密 3 比赛中的题 |

**ProblemData**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| problem | 题目编号 | CharField | primary_key |
| title | 题目标题 | CharField |  |
| level | 题目难度 | IntegerField | 1~5 |
| submission | 题目提交数 | IntegerField |  |
| ac | 该类型的数量 | IntegerField |  |
| mle | 该类型的数量 | IntegerField |  |
| tle | 该类型的数量 | IntegerField |  |
| rte | 该类型的数量 | IntegerField |  |
| pe | 该类型的数量 | IntegerField |  |
| ce | 该类型的数量 | IntegerField |  |
| wa | 该类型的数量 | IntegerField |  |
| se | 该类型的数量 | IntegerField |  |
| tag | 题目标签 | TextField | 中间用竖线隔开 |
| score | 题目分数 | IntegerField |  |
| auth | 题目权限 | IntegerField | 1公开 2私密 3 比赛中的题 |
| oj | 题目所在OJ | CharField |  |

**ProblemTag**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| tagname | 标签名字 | CharField | unique |
| count | 该标签的数量 | IntegerField | 暂时弃用 |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| ManagerOnly | 有 | 仅管理员 |
| AuthOnly | 仅比赛中或公开 | 仅管理员 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| ProblemSerializer | ALL |
| ProblemDataSerializer | ALL | 
| ProblemTagSerializer | ALL | 

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| ProblemView | 仅单个查询  | ('auth',) |  AuthOnly | 否 | 否 |
| ProblemDataView | ID倒序  | ('auth','oj',) |  ManagerOnly | 是 | ('tag', 'title') |
| ProblemTagView | ALL  | 无 |  ManagerOnly | 否 | 否 |
| UploadFileAPIView | 用于上传测试数据  | 无 |  仅管理员 | 否 | 否 |

**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| ProblemView | http://localhost:8000/problem/  | 
| ProblemDataView | http://localhost:8000/problemdata/ |  
| ProblemTagView | http://localhost:8000/problemtag/  | 
| UploadFileAPIView | http://localhost:8000/uploadfile/ |  

### User

此模块主要用来实现用户相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| User | 用户的详细信息 | 
| UserData | 用户的简要信息 | 
| UserLoginData | 用户的登录信息 | 

**User**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | primary_key |
| password | 密码 | CharField | MD5加密后的 |
| name | 昵称 | CharField |  |
| regtime | 注册时间 | DateTimeField | auto_now |
| logintime | 上次登录时间 | DateTimeField | auto_now（暂时弃用，见userlogindata表） |
| school | 学校 | CharField |  |
| course | 专业 | CharField |  |
| classes | 班级 | CharField |  |
| number | 学号 | CharField |  |
| realname | 真实姓名 | CharField |  |
| qq | QQ | CharField |  |
| email | 邮箱 | CharField |  |
| type | 权限 | IntegerField | 1 普通 2 管理员 3 超级管理员 |

**UserData**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | primary_key |
| ac | 用户AC数 | IntegerField |  |
| submit | 用户提交数 | IntegerField |  |
| score | 用户总得分 | IntegerField |  |
| des | 用户介绍 | CharField |  |
| rating | 用户的Rating | IntegerField |  |
| acpro | 用户AC的题目 | TextField | 中间用竖线隔开 |

**UserLoginData**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField |  |
| ip | 用户登录的IP | CharField |  |
| logintime | 登录的时间 | DateTimeField |  |
| msg | 其他额外信息，如浏览器版本等 | TextField |  |


**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| ManagerOnly | 有 | 仅POST或为管理员 |
| UserSafePostOnly | 有 | 仅不修改敏感信息或管理员 |
| UserPUTOnly | 无 | 仅用户 |
| AuthPUTOnly | 无 | 仅管理员 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| UserSerializer | ALL |
| UserNoPassSerializer | 不包括密码 | 
| UserNoTypeSerializer | 不包括权限 | 
| UserDataSerializer | ALL | 
| UserLoginDataSerializer | ALL | 

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| UserDataView | rating倒序 | ('username',) |  UserSafePostOnly | 否 | 否 |
| UserView | ID倒序  | ('username',) |  UserSafePostOnly | 是 | 否 |
| UserChangeView | ALL  | 无 |  UserPUTOnly | 否 | 否 |
| UserChangeAllView | ALL  | 无 |  AuthPUTOnly | 否 | 否 |
| UserLoginAPIView | 用于登陆  | 无 |  AllowAny | 否 | 否 |
| UserUpdateRatingAPIView | 用于更新本地Rating  | 无 |  AllowAny | 否 | 否 |
| UserLogoutAPIView | 用于登出  | 无 |  AllowAny | 否 | 否 |
| UserRegisterAPIView | 用于注册  | 无 |  AllowAny | 否 | 否 |
| UserLoginDataView | ID倒序  | ('username','ip',) |  ManagerOnly | 是 | 是 |

**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| UserDataView | http://localhost:8000/problem/  | 
| UserView | http://localhost:8000/problemdata/ |  
| UserChangeView | http://localhost:8000/problemtag/  | 
| UserChangeAllView | http://localhost:8000/uploadfile/ | 
| UserRegisterAPIView | http://localhost:8000/problemtag/  | 
| UserLoginAPIView | http://localhost:8000/uploadfile/ | 
| UserLogoutAPIView | http://localhost:8000/problemtag/  | 
| UserUpdateRatingAPIView | http://localhost:8000/uploadfile/ | 
| UserLoginDataView | http://localhost:8000/userlogindata/ | 

### Wiki

此模块主要用来实现Wiki相关的API

**models.py**

| model | 功能 |
| :--  | :-- |
| Wiki | 算法详情 | 
| MBCode | 模板介绍 | 
| MBCodeDetail | 模板详细代码 | 
| TrainningContest | 试炼谷的内容 | 

**Wiki**
| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | 发布人姓名 |
| type | 发布的算法 | CharField | 发布了哪一篇算法 |
| value | 具体内容 | TextField |  |
| time | 发表时间 | DateTimeField | auto_now |
| group | 所属分组 | CharField | 新添加的算法的分类，仅std=1时有效 |
| std | 是否是标准算法 | IntegerField | 0代表是，1代表新添加的算法 |
| title | 新添加的算法标题 | CharField | 仅std=1时有效 |

**MBCode**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | primary_key |
| des | 模板介绍 | CharField |  |
| time | 添加时间 | DateTimeField | auto_now |

**MBCodeDetail**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| username | 用户名 | CharField | 发布人姓名 |
| title | 模板标题 | CharField |  |
| des | 模板介绍 | DateTimeField |  |
| group | 模板所属分组 | CharField |  |
| code | 模板代码 | CharField |  |
| time | 添加时间 | DateTimeField | auto_now |

**TrainningContest**

| 属性 | 功能 | 类型 | 说明 |
| :--  | :-- | :-- | :-- |
| title | 试炼名称 | CharField |  |
| des | 试炼介绍 | CharField |  |
| tips | 试炼提示 | DateTimeField | 对应Wiki中的type，用竖线隔开 |
| group | 试炼分组 | CharField | 第几章 |
| num | 试炼关卡 | CharField | 第几关 |
| problem | 试炼题目 | DateTimeField | 中间用竖线隔开 |

**permission.py**

| permission | 读权限 | 写权限 |
| :--  | :--: | :--: |
| WikiUserOnly | 有 | 仅用户或管理员 |
| UserOnly | 有 | 仅用户或管理员 |
| ManagerOnly | 有 | 仅管理员 |

**serializers.py**

| serializers | 序列化字段 |
| :--  | :--: | :--: |
| WikiSerializer | ALL |
| WikiCountSerializer | 不包括内容 | 
| MBCodeSerializer | ALL | 
| MBCodeDetailSerializer | ALL | 
| MBCodeDetailNoCodeSerializer | 不包括代码 | 
| TrainningContestSerializer | ALL |

**views.py**

| 视图 | 查询集合  | 可过滤字段 | 权限 | 可分页 | 可搜索 |
| :--  | :--: |:--: |  :--: | :--: | :--: |
| WikiView | ALL | ('username', 'type', 'group', 'std',) |  WikiUserOnly | 否 | 否 |
| WikiCountView | ALL  | ('username', 'type') |  UserOnly | 否 | 否 |
| MBCodeView | ALL  | ('username',) |  UserOnly | 否 | 否 |
| MBCodeDetailView | ALL  | ('username', 'group', 'des', 'title') |  UserOnly | 否 | 否 |
| MBCodeDetailNoCodeView | ALL  | ('username', 'group', 'des', 'title') |  UserOnly | 否 | 否 |
| TrainningContestView | ALL  | ('group', 'title',) |  ManagerOnly | 否 | 否 |


**urls.py**

| 视图 | 访问路由  | 
| :--  | :-- |
| WikiView | http://localhost:8000/wiki/  | 
| WikiCountView | http://localhost:8000/wikicount/ |  
| MBCodeView | http://localhost:8000/mbcode/  | 
| MBCodeDetailView | http://localhost:8000/mbcodedetail/ | 
| MBCodeDetailNoCodeView | http://localhost:8000/mbcodedetailnocode/  | 
| TrainningContestView | http://localhost:8000/trainning/ | 


## 修改后端

已存在的接口可以根据需要修改，这里将以添加一个模块为例，展示如何添加一个自己的后台模块或者在已有模块中添加一个API

### 在已有模块中添加一个API

现在我们假定要在Blog模块中添加一个博客回复功能

1. 添加你的model

修改models.py文件，在文件最后添加

```py
class BlogComment(models.Model):
    # 此处编写你的字段
    username = models.CharField(max_length=50)
    msg = models.CharField(max_length=1000)
    time = models.DateField(auto_now=True)

    # 复制粘贴即可
    objects = models.Manager()
```

2. 添加你的序列化器

修改serializers.py文件来

```py
from .models import BlogComment # 记得import
class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment # 设置为你的model
        fields = '__all__'
```

具体的修改参考Django教程，这里使用REST Framework模块，使得这一切都如此简单

3. 添加视图类

修改views.py来添加

```py
from .models import BlogComment
from .serializers import BlogCommentSerializer
class BlogCommentView(viewsets.ModelViewSet): # 得益于rest_framework，构建一个视图变得很方便
    queryset = BlogComment.objects.all() # 查询集合，具体功能和修改，参考Django文档
    serializer_class = BlogCommentSerializer # 你的序列化器
    filter_fields = ('username', 'time') # 过滤字段，使得你可以在http请求中过滤，如 /?username=123456
    pagination_class = LimitOffsetPagination # 分页器，使得你的http请求支持分页，具体自行百度
    permission_classes = (ManagerOnly,) # 权限过滤器，具体参考Django文档

    throttle_scope = "post" # 限流类，直接复制粘贴即可
    throttle_classes = [ScopedRateThrottle, ]
```

4. 添加路由信息

我们修改urls.py文件在 **urlpatterns = [url('', include(routers.urls)),]** 上方添加

```py
routers.register('blogcomment', views.BlogCommentView) # 第一个参数为你的路由，第二个参数为你的视图
```

至此，我们成功的添加了一个自己的API

现在只需要同步你的数据库

```bash
python manager.py makemigrations blog
python manager.py migrate blog
```

现在可以通过**http://localhost:8000/blogcomment/**来访问你的API了

我们可以通过POST请求来添加一个数据，用PUT请求来修改一个数据
用DELETE请求来删除一个数据，用GET请求来获取所有数据

具体自行阅读HTTP请求的相关教程。

我们可以通过primary_key来获取单个数据，如

**http://localhost:8000/blogcomment/1/**

Django会默认的生成一个ID字段作为primary_key，当然你也可以自己制定，具体自行参阅Django教程。

我们可以通过limit和offset来实现分页，如

**http://localhost:8000/blogcomment/?limit=50&offset=10**

我们可以直接过滤设定好的字段，如

**http://localhost:8000/blogcomment/?username=123&time=2019-5-29**


这样一个普通的API很不安全，因此要做权限认证，自行编辑一个权限类，然后添加到**permission_classes**中，具体代码编写自行参考Django教程

### 新建一个模块

我们可以直接新建一个模块，这非常简单，首先我们先执行如下命令

```bash
python manage.py startapp yourappname
```

这样就成功新建一个模块了，我们查看目录会发现多了一个yourappname的文件夹

然后我们要注册我们的模块，我们先修改Backend/Backend/setting.py文件

在**INSTALLED_APPS**中添加你的模块名字

然后我们就可以参阅上面的**在已有模块中添加一个API**的教程来添加你的API

如果文件不存在，自行新建对应的文件在目录里即可。

我们添加完毕后要在Backend中注册你的路由信息。

我们修改**Backend/Backend/urls.py**在**urlpatterns**中添加

**url(r'', include('yourappname.urls'))**

这样就可以了。

不要忘了同步你的数据库

```bash
python manager.py makemigrations yourappname
python manager.py migrate yourappname
```

以上就是后端开发教程
