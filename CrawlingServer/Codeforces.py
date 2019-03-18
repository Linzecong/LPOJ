import urllib.request
import json
def get_CF_data(name):
    api_url = "http://codeforces.com/api/user.status?handle="+name
    try:
        response = urllib.request.urlopen(api_url)
        response_data=response.read()

        response_data = json.loads(response_data)

        # print(response_data)
        acpro = set()
        attpro = set()

        for data in response_data["result"]:
            if data["verdict"]=="OK":
                acpro.add(str(data["problem"]["contestId"])+str(data["problem"]["index"]))
            attpro.add(str(data["problem"]["contestId"])+str(data["problem"]["index"]))
        return [len(acpro),len(attpro)]
    except:
        return [-1,-1]

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_CF_data(name))