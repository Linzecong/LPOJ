import urllib.request
import re

def get_CF_Rate(name):
    api_url = "https://codeforces.com/profile/"+name
    try:
        response = urllib.request.urlopen(api_url,timeout=2000)
        response_data=response.read().decode('utf-8')
        
        score = re.findall('<span style="font-weight:bold;" class=".*?">([0-9]{2,4})</span>', response_data)[0]
        return score
    except:
        return -1

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_CF_Rate(name))
