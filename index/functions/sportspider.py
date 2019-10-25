import requests
from lxml import etree
import random




user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    ]
def sportget():
    url='http://www.ningmengtiyu.com/zuqiubifen.html'
    headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    html=requests.get(url,headers=headers)
    html.encoding="utf-8"
    html=html.text
    parseHtml=etree.HTML(html)
    starttime=parseHtml.xpath("//tr[contains(@class,'lkd')]/td[1]/text()")
    competition=parseHtml.xpath("//tr[contains(@class,'lkd')]/td[3]/a/text()")
    vs=parseHtml.xpath("//tr[contains(@class,'lkd')]/td[4]/a/text()")
    #直播间link
    link=parseHtml.xpath("//a[contains(@href,'/zuqiubifen/zhibo')]/@href")
    if len(starttime)==len(competition)==len(vs)==len(link):
        print("true")
        live_lst=[]
        for i in link:
            fulllink='http://www.ningmengtiyu.com'+i
            zhibohtml = requests.get(fulllink, headers={"User-Agent":random.choice(user_agents)})
            zhibohtml.encoding = "utf-8"
            zhibohtml = zhibohtml.text
            parseHtml = etree.HTML(zhibohtml)
            liveroomlink_list=parseHtml.xpath('//div[contains(@class,"match-live-zhibo")]/a/@href')
            live_lst.append(liveroomlink_list)
        return zip(starttime,competition,vs,live_lst)
    else:
        return


