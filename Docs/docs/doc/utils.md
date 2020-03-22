# 其他工具

## CrawlingServer

在管理员页面设置好爬虫信息后，可以启动爬虫机器人进行爬虫。
主要可以爬取的信息是 各OJ做题数，博客，和近期比赛列表

### 启动

```bash
python main.py
```
### 源码解析

[main.py](https://github.com/Linzecong/LPOJ/blob/master/CrawlingServer/main.py)


## Tools

这个文件夹中，包含了各种实用的工具！


### 查重脚本 duplication_checking.py

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


### HDUSpider.py

用于爬取杭电题目数据并保存到数据库中！

你需要这只你的管理员的用户名和密码来登录！

运行时，记得正确设置题目的编号和杭电上题目的编号，看清楚源码再运行！

### RaiseCheck.py

这个脚本用于检查用户的代码有多少个raise

因为Python的话，可以用过爆破数据库来找到正确答案

通过这个脚本我们能找到爆破的用户，当然你也可以检查其他东西。代码很简单

### RatingCalculator.py

用于计算rated的比赛的rating 变化！

就是每次Rated比赛完毕后，需要手动的更新所有参加比赛的用户的Rating！

就要运行这个脚本！具体规则请看LPOJ首页的规则说明

你可以自己修改代码，来改变Rating的计算规则！

### RecoverBoard.py

排行榜恢复器！有时候由于网络原因，排行榜可能会记录失败！（低概率事件）

排查后，如果的确有用户的排行榜错了，可以用这个脚本重新生成整个排行榜

修改source_contest为你的比赛ID

然后运行~

### SubmitExport.py

这个脚本可以把用户提交的代码导出

由于数据量太大！因此直接通过读取文件的方式

在运行前，你需要将judgestatus_judgestatus表中的数据导出！（如果只导出某个比赛的，请自行筛选！）

导出成JSON格式！网上很多教程

然后保存为data.json文件。然后运行即可！

详见代码！

### UserImporter.py

代码原理很简单！就是自动提交api。自己看代码！

