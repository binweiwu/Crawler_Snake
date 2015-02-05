# ! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015-2-5
 
@author: bingo
'''
import urllib
from bs4 import BeautifulSoup
from with_conn_to_db import conn_to_mysql
from HTMLParser import HTMLParser  
from re import sub  
from sys import stderr  
from traceback import print_exc  

class _DeHTMLParser(HTMLParser):  
    def __init__(self):  
        HTMLParser.__init__(self)  
        self.__text = []  

    def handle_data(self, data):  
        text = data.strip()  
        if len(text) > 0:  
            text = sub('[ \t\r\n]+', ' ', text)  
            self.__text.append(text + ' ')  
  

    def handle_starttag(self, tag, attrs):  
        if tag == 'p':  
            self.__text.append('\n\n')  
        elif tag == 'br':  
            self.__text.append('\n')  

    def handle_startendtag(self, tag, attrs):  
        if tag == 'br':  
            self.__text.append('\n\n')  

    def text(self):  
        return ''.join(self.__text).strip()  

def dehtml(text):  
    try:  
        parser = _DeHTMLParser()  
        parser.feed(text)  
        parser.close()  
        return parser.text().strip()  
    except:  
        print_exc(file=stderr)  
        return text.strip()    

def get_content(url):
    """doc."""
    html = urllib.urlopen(url)
    content = html.read()
    html.close()
#     print content
    return content

def get_keyword(info):
    """doc.

    """   
    try:
        soup = BeautifulSoup(info)
        all_keyword = soup.find_all('h2',class_="highlight")
        all_keyword = "<html>"+str(all_keyword[0])+"</html>"
        soup = BeautifulSoup(all_keyword)
        return soup.get_text()   
    except:
        pass
    return "keyword遇见你的时候所有星星都落在我头上"  

def get_jobbt(info):
    """doc.

    """   
    try:
        soup = BeautifulSoup(info)
        all_jobbt = soup.find_all('div',class_="myj-details-descrip")
        return all_jobbt[1]
    except:
        pass
    return "jobbt遇见你的时候所有星星都落在我头上"

def main():
    try:  
        keyword12 = get_keyword(info).encode('utf8')
        requirement12 = dehtml(str(get_jobbt(info)))
        print i
#     print keyword12,type(keyword12)
#     print requirement12,type(requirement12)
        sql_insert = """INSERT INTO job_csdn_requirement (url, keyword, requirement) VALUE ("%s","%s","%s")
    """
        with conn_to_mysql() as db:
            db.execute(sql_insert %(url, keyword12, requirement12.strip().replace("'",'#')))
    except:
        pass


for i in xrange(79786,80000):
# for i in xrange(80827,80828):
    url = 'http://job.csdn.net/Job/Index?jobID='+str(i)
    info = get_content(url)
    main()
      