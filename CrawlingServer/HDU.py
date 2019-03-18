import urllib.request
import json
def get_HDU_data(name):
    try:
        api_url = "http://acm.hdu.edu.cn/userstatus.php?user="+name
        response = urllib.request.urlopen(api_url)
        response_data=response.read()
        response_data = str(response_data)
        
        ac = response_data[response_data.find("Problems Solved</td><td align=center>")+len("Problems Solved</td><td align=center>"):response_data.find("</td></tr>",response_data.find("Problems Solved</td><td align=center>"))]
        submit =response_data[response_data.find("Problems Submitted</td><td align=center>")+len("Problems Submitted</td><td align=center>"):response_data.find("</td></tr>",response_data.find("Problems Submitted</td><td align=center>"))]
        return [int(ac),int(submit)]
    except:
        return [-1,-1]

if __name__ == "__main__":
    while(True):
        name = input("请输入要爬的ID:")
        print(get_HDU_data(name))