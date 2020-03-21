# 其他工具

## 爬虫机器人

在管理员页面设置好爬虫信息后，可以启动爬虫机器人进行爬虫。
主要可以爬取的信息是 各OJ做题数，博客，和近期比赛列表

### 启动

```bash
python main.py
```
### 源码解析

[main.py](https://github.com/Linzecong/LPOJ/blob/master/CrawlingServer/main.py)

## Rating计算器

每场比赛结束后，可以调用 [RatingCalculator.py](https://github.com/Linzecong/LPOJ/blob/master/CrawlingServer/main.py) 来计算某场比赛的Rating变化。记得设置**setting.json**里的数据库配置信息

## 查重脚本 duplication_checking.py

此脚本基于SIM工具查重


自行查看攻略！ https://dickgrune.com/Programs/similarity_tester/

修改其中的数据库信息
```py
db = MySQLdb.connect(
     host="localhost",    # 主机名
     user="root",         # 数据库用户名
     passwd="",           # 数据库密码
     db="LPOJ")           # 数据库名称
```
用法
```py
sudo python duplication_checking.py <ContestId>
```
脚本将会在脚本所在的目录下生成一个contest_duplication_checking的文件夹用于存放AC代码，子文件夹为contest_i分别存放了每一场比赛的AC代码，AC代码按用户名存放
