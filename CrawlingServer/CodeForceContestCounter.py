import urllib.request
import datetime
import json

# 返回一个月内的cf场数和上/掉分情况
def get_CF_ContestCount(name):
    apiUrl = "https://codeforces.com/api/user.rating?handle=" + name

    try:
        page = urllib.request.urlopen(apiUrl, timeout=2000)
        s = page.read().decode('utf-8')
        contestsData = json.loads(s)['result']

        # 改为直接用rating变化的时间当做比赛时间
        # 由于rating变化时间一般延迟一天，放宽到32天
        lastTime=(datetime.timedelta(days=-32) +
           datetime.datetime.now()).timestamp()

        sum=0
        cnt=0
        for contest in contestsData:
            if contest['ratingUpdateTimeSeconds'] < lastTime:
                continue
            cnt += 1
            sum += contest['newRating'] - contest['oldRating']
        return [cnt, sum]
        
    except Exception as e:
        print(str(e))
        return [-1, -1]

if __name__ == "__main__":
    while(True):
        name=input("请输入要爬的ID:")
        print(get_CF_ContestCount(name))
