import urllib.request
import urllib.parse
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_VJ_data(name):
    # try:
    #     api_url="https://vjudge.net/user/data"
    #     test_data = {'username':name,"draw":1,"start":0,"length":20,"nickname":"","school":"","statRange":3}
    #     aaa = urllib.parse.urlencode(test_data).encode('utf-8')
    #     req = urllib.request.Request(url = api_url,data = aaa)

    #     res_data = urllib.request.urlopen(req)
    #     res = res_data.read().decode('utf-8')
    #     res = json.loads(res)
    #     if len(res["data"]) == 0:
    #         return [0,0]
    #     return [int(res["data"][0][4]),int(res["data"][0][5])]
    # except:
    #     return [-1,-1]

    
    api_url = "http://vjudge.net/user/"+name
    response = urllib.request.urlopen(api_url)
    response_data=response.read()
    response_data = str(response_data)
    
    ac = response_data[response_data.find("title=\"Overall solved\" target=\"_blank\">")+len("title=\"Overall solved\" target=\"_blank\">"):response_data.find("</a>",response_data.find("title=\"Overall solved\" target=\"_blank\">"))]
    submit =response_data[response_data.find("title=\"Overall attempted\" target=\"_blank\">")+len("title=\"Overall attempted\" target=\"_blank\">"):response_data.find("</a>",response_data.find("title=\"Overall attempted\" target=\"_blank\">"))]
    return [int(ac),int(submit)]
    

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_VJ_data(name))