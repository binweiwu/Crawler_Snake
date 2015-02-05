# ! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015-2-4
 ##job_url可以不断更新，job_requirement就不用更新了。
@author: bingo
'''
import urllib
from bs4 import BeautifulSoup
from with_conn_to_db import conn_to_mysql

def get_content(url):
    """doc."""
    html = urllib.urlopen(url)
    content = html.read()
    html.close()
#     print content
    return content

def get_jobbt(info):
    """doc.
    <dd class="job_bt">
                        <h3 class="description">职位描述</h3>
                        <p>=====春雨简介=====</p> 
<p>春雨移动健康成立于2011年7月，</p> 
<p>度过三个春秋，历经两轮融资，春雨已成为中国最大的移动医患交流与交易平台。</p> 
<p>春雨致力于以科技整合医疗资源，为用户创造健康。</p> 
<p>春雨搭建了一个虚拟的医院，用户可以定制在线医疗，医生可以开设空中诊所，而春雨，则在其中调和，既保证医者的权威，也保证用户的稳定。</p> 
<p>&nbsp;</p> 
<p>=====什么样的人适合春雨=====</p> 
<p>如果你拥有冒险精神，乐于挑战自己，愿意承担风险而不是危险；</p> 
<p>如果你具有先锋品质，勇于探索移动医疗这一未知领域，敢当先驱而不是烈士；</p> 
<p>如果你怀揣浪漫情怀，善于做生活的玩家，为人风流而不下流。</p> 
<p>如果你追求自由，不随波逐流，不盲目跟从；</p> 
<p>既有理想主义者的冒险与坚持，又有现实主义者的踏实与技术；</p> 
<p>愿意用双手丈量移动医疗这片新大陆，打破医患交流的壁垒；</p> 
<p>那么，请加入春雨。</p> 
<p>&nbsp;</p> 
<p>=====春雨开放什么岗位=====</p> 
<p>&nbsp;</p> 
<p><strong>Android</strong><strong>高级研发工程师</strong></p> 
<p>【你来做什么】</p> 
<p>负责Android等移动平台的应用程序开发和架构设计；</p> 
<p>&nbsp;</p> 
<p>【我们希望你】</p> 
<p>1、1-3年 android相关开发经验；</p> 
<p>2、熟练掌握android各种开发框架；</p> 
<p>3、有较强的独立解决问题的能力；</p> 
<p>4、计算机相关专业重点本科以上学历。</p> 
<p>【薪资】</p> 
<p>20-40W 优秀员工可获得期权奖励</p> 
<p>&nbsp;</p> 
<p>====春雨可奉上=====</p> 
<p>1-免费的早、午餐，免费的零食、咖啡，免费的水果、冷饮；</p> 
<p>2-每年一次免费体检，捷足先登的医疗服务；</p> 
<p>3-每月300元下午茶补贴；</p> 
<p>4-每月一日的大姨妈假（男生共享）；</p> 
<p>5-每周享有的羽毛球、篮球、台球、乒乓球健身活动；</p> 
<p>6-每月享有的私人按摩师；</p> 
<p>7-匹配图书室、电玩室、健身房的办公环境；（即将开放）</p> 
<p>8-每年2次自主加薪机会。</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p>
                    </dd>
    """   
    try:
        soup = BeautifulSoup(info)
        all_jobbt = soup.find_all('dd',class_="job_bt")
    #     return [jobbt['src'] for jobbt in all_jobbt] #待用时，可用列表解析先保存     
        all_jobbt = "<html>"+str(all_jobbt[0])+"</html>"
        soup = BeautifulSoup(all_jobbt)
        return soup.get_text()   
    except:
        pass
    return "遇见你的时候所有星星都落在我头上"  

sql_num = """SELECT id FROM job_url"""
sql_geturl = """SELECT url FROM job_url WHERE id = '{id}'"""
sql_insert = "INSERT INTO job_requirement (requirement) VALUE('{job_requirement12}')"
with conn_to_mysql() as db:
    num = db.execute(sql_num)
    for id_num in xrange(1,num+1):
        db.execute(sql_geturl.format(id=id_num))
        url = db.fetchall()
        print url[0][0]
        info = get_content(url[0][0])
#         print get_jobbt(info)
        job_bt = get_jobbt(info).encode('utf8').strip().replace("'",'#')
        db.execute(sql_insert.format(job_requirement12=str(job_bt)))
#         print get_jobbt(info)
