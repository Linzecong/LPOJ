import requests
import urllib
import base64
from time import sleep


def JudgeHDU(problemid, language, usercode):
    usercode = urllib.parse.quote(usercode)
    usercode = base64.b64encode(usercode.encode('utf-8'))

    def substr(start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()

    if language == "C++":
        language = 0
    elif language == "Java":
        language = 5
    elif language == "C":
        language = 1
    else:
        return ["-4", "0", "0", "Language not support"]

    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        'User-Agent': userAgent,
    }

    mafengwoSession = requests.session()

    loginUrl = "http://acm.hdu.edu.cn/userloginex.php?action=login"
    loginData = {
        "username": "lpojjudger1",
        "userpass": "504603913"
    }
    responseRes = mafengwoSession.post(
        loginUrl, data=loginData, headers=header, allow_redirects=True)
    print(problemid,responseRes.status_code)

    postUrl = "http://acm.hdu.edu.cn/submit.php?action=submit"
    postData = {
        "problemid": problemid,
        "language": language,
        "_usercode": usercode,
        'check':0
    }
    responseRes = mafengwoSession.post(postUrl, data=postData, headers=header)
    resstr = f"text = {responseRes.text}"
    print(responseRes.status_code)

    while True:
        sleep(1)
        statusUrl = "http://acm.hdu.edu.cn/status.php?first=&pid=%s&user=lpojjudger1&status=0" % (problemid)
        responseRes = mafengwoSession.get(statusUrl)
        resstr = f"text = {responseRes.text}"

        subid = substr("<td height=22px", "lpojjudger1", resstr)
        subid = substr(">", "</td><td>", subid)

        restr = substr(subid, "font>", resstr)
        restr = substr("color", "/", restr)
        restr = substr(">", "<", restr)
        print(restr)
        if restr != "Queuing" and restr != "Compiling" and restr != "Running":

            timestr = substr(subid, "S</td><td>", resstr)
            timestr = substr("</a></td><td>", "M", timestr)

            memstr = substr("MS</td><td>", "K</td><td>", resstr)
            memstr = int(memstr)
            memstr = str(int(memstr/1024))
            
            if restr == "Accepted":
                restr = "0"
            elif restr == "Presentation Error":
                restr = "-5"
            elif restr == "Wrong Answer":
                restr = "-3"
            elif restr.find("Runtime Error") >= 0:
                restr = "4"
            elif restr == "Time Limit Exceeded" or restr == "Output Limit Exceeded":
                restr = "1"
            elif restr == "Memory Limit Exceeded":
                restr = "3"
            elif restr == "Compilation Error":
                restr = "-4"
            else:
                restr = "5"
         
                

            return [restr, timestr, memstr, "Remote run ID:HDU  "+subid]


if __name__ == "__main__":

    code = """#include<stdio.h>
#include<math.h>
int main()
{
	double X1,Y1,X2,Y2;
	while (scanf ("%lf" "%lf" "%lf" "%lf" , &X1,&Y1,&X2,&Y2) !=EOF)
	{
		double sum = pow(X1-X2,2) + pow(Y1-Y2,2);
		double result = sqrt(sum);
		printf ("%.2lf\n" , result);
	}
	return 0;
}"""

    
    print(code)
    JudgeHDU(2001,"C++",code)