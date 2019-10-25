#这是一个将图片链接 存入数据库的文件


import os
import pymysql
path='D:\爬虫数据\校花'


links=os.listdir('D:\爬虫数据\头像')

conn = pymysql.connect(host='192.168.100.3', user='root', password='python', database='MysiteProject',port=3306)
cursor = conn.cursor()
for link in links:
    sql = 'insert into images(link,type_id) values (%s,%s)'
    cursor.execute(sql, (link,2))
    conn.commit()
cursor.close()
conn.close()