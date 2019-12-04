import urllib.request
import re
import datetime


def getLastDate():
    lastDate = datetime.datetime.now() + datetime.timedelta(days=-31)
    return [lastDate.year, lastDate.month, lastDate.day]


def timeCmp(a, b):
    mouths = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cut = a.split('/')
    if(int(cut[2]) > b[0]):
        return True
    for i in range(len(mouths)):
        if cut[0] == mouths[i]:
            cut[0] = str(i)
            break
    if(int(cut[0]) > b[1]):
        return True
    if(int(cut[1]) >= b[2]):
        return True
    return False


def getContestsTimeLine():
    api_url = "https://codeforces.com/contests"
    tar = r'<td>\r\n(.*?)<br/>\r\n.*?<a style="font-size: 0.8em;" href="/contest/[0-9]{1,6}">'
    tar2 = '<span class="format-date" data-locale="en">(.*?) .*?</span>'
    try:
        page = urllib.request.urlopen(api_url, timeout=1000)
        page_data = page.read().decode('utf-8')
        page_data = page_data[1000: len(page_data) // 2]
        contests = re.findall(tar, page_data)
        times = re.findall(tar2, page_data)

        lastDate = getLastDate()
        contestsTimeLine = set()
        for i in range(len(contests)):
            if not timeCmp(times[i], lastDate):
                break
            contestsTimeLine.add(re.sub(' ', '', contests[i]))

        return contestsTimeLine
    except Exception as e:
        print(str(e))
        return {}


#返回一个月内的cf场数和上/掉分情况
def get_CF_ContestCount(name, contestsTimeLine):
    if not contestsTimeLine:
        return [-1, -1]

    api_url = "https://codeforces.com/contests/with/" + name
    tar = '<a href="/contest/[0-9]{1,6}" title="(.*?)">'
    tar2 = '<span style="color:.*?;font-weight:bold;">(.*?)</span>'
    try:
        page = urllib.request.urlopen(api_url, timeout=2000)
        page_data = page.read().decode('utf-8')

        contests = re.findall(tar, page_data)
        off = re.findall(tar2, page_data)

        sum = 0
        cnt = 0
        for i in range(len(contests)):
            if re.sub(' ', '', contests[i]) in contestsTimeLine:
                cnt += 1
                sum += int(off[i])

        return [cnt, sum]
    except Exception as e:
        print(str(e))
        return [-1, -1]


if __name__ == "__main__":
    contestsTimeLine = getContestsTimeLine()
    # print(contestsTimeLine)
    while(True):
        name = input("请输入要爬的ID:")
        print(get_CF_ContestCount(name, contestsTimeLine))
