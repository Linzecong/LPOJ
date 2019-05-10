import requests
from time import sleep


def getpro(problemid):
    def substr(start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()

    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    header = {
        'User-Agent': userAgent,
    }


    Url = "http://acm.hdu.edu.cn/showproblem.php?pid="+problemid

    responseRes = requests.get(Url, headers=header)

    resstr = f"text = {responseRes.text}"

    timestr = substr("Time Limit","(Java",resstr)
    timestr = substr("/"," MS",timestr)

    memstr = substr("Memory L","(Java",resstr)
    memstr = substr("/"," K",memstr)
    memstr = str(int(int(memstr)/1024))
    
    desstr = substr("Description</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    instr = substr("Input</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    outstr = substr("Output</div> <div class=panel_content>","</div><div class=panel_bottom>",resstr)
    sinstr = substr("ier,monospace;\">","</div></pre></div><div",resstr)

    soutstr = substr("Sample Output</div>","</pre></div><div",resstr)
    soutstr = substr("monospace;\">","</div>",soutstr)

    print(timestr)
    print(memstr)
    print(desstr)
    print(instr)
    print(outstr)
    print(sinstr)
    print(soutstr)

if __name__ == "__main__":
    getpro("1000")
