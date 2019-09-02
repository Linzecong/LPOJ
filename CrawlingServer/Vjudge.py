import urllib.request
import urllib.parse
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_VJ_data(name):
    

    try:
        api_url = "http://vjudge.net/user/"+name
        response = urllib.request.urlopen(api_url,timeout=2000)
        response_data=response.read()
        response_data = str(response_data)
        
        ac = response_data[response_data.find("title=\"Overall solved\" target=\"_blank\">")+len("title=\"Overall solved\" target=\"_blank\">"):response_data.find("</a>",response_data.find("title=\"Overall solved\" target=\"_blank\">"))]
        submit =response_data[response_data.find("title=\"Overall attempted\" target=\"_blank\">")+len("title=\"Overall attempted\" target=\"_blank\">"):response_data.find("</a>",response_data.find("title=\"Overall attempted\" target=\"_blank\">"))]
        return [int(ac),int(submit)]
    except:
        return [-1,-1]

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_VJ_data(name))