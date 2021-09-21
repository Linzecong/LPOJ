import urllib.request
import json
import urllib.parse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_LPOJ_data(name):
    if name == "":
        return [-1, -1]

    api_url = "https://www.lpoj.cn/api/userdata/?username=" + \
        urllib.parse.quote(name)
    try:
        response = urllib.request.urlopen(api_url, timeout=2000)
        response_data = response.read()

        response_data = json.loads(response_data)
        if len(response_data) == 0:
            return [-1, -1]
        for data in response_data:
            return [data["ac"], data["submit"]]
    except:
        return [-1, -1]


if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_LPOJ_data(name))
