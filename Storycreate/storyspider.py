import requests
from lxml import etree
import random
import pymysql
import os
from threading import Thread,Semaphore,local,Lock
import time

user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    ]
class Getstory:
    def __init__(self):
        #改变页数
        self.url='https://qxs.la/top/1/'
        self.headers={"User-Agent":random.choice(user_agents)}
        #控制爬行线程数
        # self.sem=Semaphore(3)
        # self.conn=pymysql.connect(host='192.168.100.3', user='root', password='python', database='MysiteProject', port=3306)
        # self.cursor = local()
        # self.cursor=self.conn.cursor()
        # self.lock=Lock()


    def getpage_story(self):
        html = requests.get(self.url, headers=self.headers).text
        parseHtml = etree.HTML(html)
        names = parseHtml.xpath('/html/body/div[3]/ul/li[1]/a/text()')
        authors = parseHtml.xpath('/html/body/div[3]/ul/li[3]/a/text()')
        last_time=parseHtml.xpath('/html/body/div[3]/ul[@class="list_content "]/li[4]/text()')
        links = parseHtml.xpath('/html/body/div[3]/ul/li[1]/a/@href')
        return zip(names,authors,links,last_time)
        # self.getpage_dir(names,links)

    def getpage_dir(self):
        n=0
        for i in self.getpage_story():
            # self.sem.acquire()

            print(i)
            os.mkdir("D:\爬虫数据2\{}".format(i[0]))
            name=i[0]
            url1 = 'https://qxs.la' + i[2]
            html1= requests.get(url1, headers={"User-Agent": random.choice(user_agents)}).text
            parseHtml1 = etree.HTML(html1)
            story_dir = parseHtml1.xpath('/html/body/div[9]/div/a/text()')
            story_links = parseHtml1.xpath('/html/body/div[9]/div/a/@href')
            n+=1
            Thread(target=self.gettext, args=(story_dir,story_links,name)).start()



    def gettext(self,story_dir,story_links,name):

        x=1
        for i in zip(story_dir,story_links):
            # print(i[0],i[1])
            url2 = 'https://qxs.la' + i[1]
            html2 = requests.get(url2, headers={"User-Agent": random.choice(user_agents)})
            # time.sleep(0.2)
            html2=html2.text
            parseHtml2 = etree.HTML(html2)
            context = parseHtml2.xpath('//*[@id="content"]/text()')
            content = ""
            for line in context:
                content += line + "\n"
            content = i[0]+"\n"+" " * 6 + content.strip()
            #对文件名处理
            # newstr = ""
            # for i in i[0]:
            #     if i not in ["*", "/", "\\", ":", "?", "<", ">", "|", "\""]:
            #         newstr += i
            s=str(i[1])
            s=s.split("/")[-3]+"_"+str(x)
            x=x+1
            with open("D:/爬虫数据2/{}/{}.txt".format(name,s), "w",encoding="utf-8") as f:
                f.write(content)
            self.savepath(name,i[0],s)
        # self.sem.release()
        # self.conn.close()


    def savepath(self,name,story_dirname,content_path):
        conn = pymysql.connect(host='192.168.100.3', user='root', password='python', database='MysiteProject',port=3306)
        cursor = conn.cursor()
        sql = 'select id from story where name = %s'
        print(name)
        cursor.execute(sql, (name,))
        story_id = cursor.fetchone()[0]
        sql1 = 'insert into story_text(story_dirname,content_path,story_id) values (%s,%s,%s)'
        cursor.execute(sql1, (story_dirname, content_path, story_id))
        conn.commit()
        cursor.close()
        conn.close()

        # 关闭连接


a=Getstory()
a.getpage_dir()


# #入数据库
# def savedata():
#     conn=pymysql.connect(host='192.168.100.3', user='root', password='python', database='MysiteProject', port=3306)
#     cursor=conn.cursor()
#     sql='insert into story(name,author,last_time) values (%s,%s,%s)'
#     for story in a.getpage_story():
#         cursor.execute(sql,(story[0],story[1],story[3]))
#         conn.commit()
#     cursor.close()
#     conn.close()


# savedata()

# 链接入数据库
# def savepath(name,story_dirname,content_path):
# conn=pymysql.connect(host='192.168.100.3', user='root', password='python', database='MysiteProject', port=3306)
# cursor=conn.cursor()
# sql='select id from story where name = %s'
# story_id=cursor.execute(sql,("疯狂农场主",))
# story_id=cursor.fetchone()[0]
# print(story_id)
# sql1='insert into story(story_dirname,content_path,story_id) values (%s,%s,%s)'
# cursor.execute(sql1,(story_dirname,content_path,story_id))
# conn.commit()
# cursor.close()
# conn.close()