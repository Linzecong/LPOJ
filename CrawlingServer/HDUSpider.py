import requests
from time import sleep

login={
        'username':"504603913",
        'password':"721543705bd6c0469d22c781efe27343"
}
mafengwoSession = requests.session()
backendurl = "http://119.29.15.43:8000/login/"
responseRes = mafengwoSession.post(backendurl,data=login)

def getpro(problemid,ppid):

    def substr(start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                aaa = html[start:end].strip()
                if aaa == "" or aaa is None:
                    aaa = "No data."
                return aaa
        raise "Error"

    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        'User-Agent': userAgent,
    }


    Url = "http://acm.hdu.edu.cn/showproblem.php?pid="+problemid

    responseRes = requests.get(Url, headers=header)

    resstr = f"text = {responseRes.text}"

    try:
        titstr = substr("='color:#1A5CC8'>","</h1><font><b>",resstr)
    except:
        print(ppid+" error")
        return 1

    try:
        timestr = substr("Time Limit","(Java",resstr)
        timestr = substr("/"," MS",timestr)
    except:
        print(ppid+" error")
        return 1


    try:
        memstr = substr("Memory L","(Java",resstr)
        memstr = substr("/"," K",memstr)
        memstr = str(int(int(memstr)/1024))
    except:
        print(ppid+" error")
        return 1

    try:
        desstr = substr("Description</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    except:
        desstr = "No data."

    try:  
        instr = substr("Input</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    except:
        instr = "No data."
        
    try:
        outstr = substr("Output</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    except:
        outstr = "No data."
    try:
        sinstr = substr("ier,monospace;\">","</div></pre></div><div",resstr)
    except:
        sinstr = "No data."

    try:
        soutstr = substr("Sample Output</div>","</pre></div><div",resstr)
        soutstr = substr("monospace;\">","</div>",soutstr)
    except:
        soutstr = "No data."

    prodata = {
        'problem':ppid,
        'oj':"HDU",
        'title':'HDU - '+str(problemid)+' '+titstr,
        'des':desstr,
        'input':instr,
        'output':outstr,
        'sinput':sinstr,
        'soutput':soutstr,
        'source':str(problemid),
        'time':timestr,
        'memory':memstr,
    }
    prodatas = {
        'problem':ppid,
        'oj':"HDU",
        'title':'HDU - '+str(problemid)+' '+titstr,
        'tag':'HDU',
        'level':3,
    }

    
    
    backendurl = "http://119.29.15.43:8000/problem/"
    responseRes = mafengwoSession.post(backendurl,data=prodata)
    if int(responseRes.status_code/100) != 2:
        print(responseRes.text)
        exit(0)
    backendurl = "http://119.29.15.43:8000/problemdata/"
    responseRes = mafengwoSession.post(backendurl,data=prodatas)
    if int(responseRes.status_code/100) != 2:
        print(responseRes.text)
        exit(0)
    print('HDU - '+str(problemid)+' '+titstr)
    return 0

# totid = 0
# for i in range(6000):
#     totid += getpro(str(i+1930),str(i+954-totid))
getpro(str(1083),str(189))