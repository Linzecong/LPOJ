import urllib.request
import urllib.parse
import json
def get_VJ_data(name):
    try:
        api_url="https://vjudge.net/user/data"
        test_data = {'username':name,"draw":1,"start":0,"length":20,"nickname":"","school":"","statRange":3}
        aaa = urllib.parse.urlencode(test_data).encode('utf-8')
        req = urllib.request.Request(url = api_url,data = aaa)

        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode('utf-8')
        res = json.loads(res)
        if len(res["data"]) == 0:
            return [0,0]
        return [int(res["data"][0][4]),int(res["data"][0][5])]
    except:
        return [-1,-1]

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_VJ_data(name))