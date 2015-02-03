# ! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015-2-3
##爬取拉勾网Android标签下的所有URL，写入数据库dw里的表job_url
DROP TABLE IF EXISTS job_url;
CREATE TABLE `job_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
@author: bingo
'''

import urllib
from sgmllib import SGMLParser
import urlparse
from with_conn_to_db import conn_to_mysql

class URLLister(SGMLParser):  
    '''获取网页中所有链接地址,加入到列表中'''  
    def reset(self):
        self.urls = []
        SGMLParser.reset(self)        

    def start_a(self, attrs):
        """在序列中取出URL地址"""
        urlList = [v for k, v in attrs if k=='href']
        if urlList:
            self.urls.extend(urlList)

    def getHTML(self,targetUrl):
        """获取网页内容"""
        sockPage=urllib.urlopen(targetUrl)
        HTML=sockPage.read()  
        sockPage.close()  
        return HTML

def getUrls (targetUrl):
    """获取URL地址后处理返回"""
    parser = URLLister();
    HTML=parser.getHTML(targetUrl);
    parser.feed(HTML);# 装填分析器，使得"start_"开头的方法都被执行了并自动匹配出所有已定义的start_方法的 tag信息
    urlList = parser.urls
    parser.close()
    urlTup = urlparse.urlparse(targetUrl) #解析URL
    for i in range(len(urlList)):
        urlList[i] = addHttp(urlList[i],urlTup)
    return urlList

def addHttp(url,urlTup):
    """处理成完整的URL"""
    if url.startswith("http"):return url
    rootUrl = urlTup.scheme + "://" + urlTup.netloc
    if url.startswith("/"):
        fullUrl = rootUrl + url
    else:
        fullUrl = rootUrl + urlTup.path
    return fullUrl

if __name__ == "__main__":
    
    Joburl = []
    for i in xrange(1,31):
        contain_word1 = 'jobs'
        contain_word2 = 'htm'
        targetUrl = 'http://www.lagou.com/jobs/list_Android?kd=Android&spc=1&pl=&gj=&xl=&yx=&gx=&st=&labelWords=label&lc=&workAddress=&city=%E5%85%A8%E5%9B%BD&requestId=&pn='+str(i) 
        urls = getUrls(targetUrl)
        Joburl = [url for url in urls if url.find(contain_word1)>=0 and url.find(contain_word2)>=0]
        Joburl = list(set(Joburl))
        for job in Joburl:
            print job
            sql_insert = "INSERT INTO job_url (url) VALUE('{job_url12}')"
            with conn_to_mysql() as db:
                db.execute(sql_insert.format(job_url12=job))
