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