import requests
from lxml import etree
import re


def musicget(url):
    url=url
    headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    html=requests.get(url,headers=headers)
    html.encoding="utf-8"
    html=html.text
    regex = re.compile(r'\[{"id":\d+,"name":"(.*?)",', re.S)
    singer_list = regex.findall(html)
    # //a[contains(@href,"/song?id=")]/@href
    # https://music.163.com/song/media/outer/url?id=
    parseHtml=etree.HTML(html)
    r_list=parseHtml.xpath('//a[contains(@href,"/song?id=")]/@href')
    name_list=parseHtml.xpath('//a[contains(@href,"/song?id=")]/text()')
    names_list=[]
    for i in name_list:
        if "{" not in i:
            names_list.append(i)
    url_list=[]
    for j in r_list:
        if "$" not in j:
            id = j.split("/song?id=")[1]
            url1 = 'https://music.163.com/song/media/outer/url?id=' + id
            url_list.append(url1)
    return zip(names_list,url_list,singer_list)


