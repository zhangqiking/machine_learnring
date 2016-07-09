#_*_coding:utf-8_*_

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import random
import time
import MySQLdb
import urllib2
import pandas
import jieba


class Spider(object):
    def __init__(self,initsite):
        self.initsite = initsite
        self.tools = ['Python','Java','C++','C','Hadoop','R','Sas','Spss',
                      'Spark','SQL','NOSQL','Linux','Matlab','Mapreduce','Scala']
        self.tablehead =['ID','salary','place','experience','education',
                         'type','field','scale','capital']
        self.user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                    ]

    def OpenUrl(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        agent = random.choice(self.user_agents)
        dcap["phantomjs.page.settings.userAgent"] = (agent,"(KHTML, like Gecko) Chrome/15.0.87")
        #Browser = webdriver.PhantomJS(desired_capabilities=dcap)
        Browser = webdriver.Chrome(desired_capabilities=dcap)
        Browser.get(url)
        
        return Browser
    
    def OpenUrl1(self,url):
        agent = random.choice(self.user_agents)
        request = urllib2.Request(url)
        request.add_header('User-Agent',agent)
        html = urllib2.urlopen(request)
        return html.read()


    def Filltext(self,brower,text):
        place = browser.find_element_by_xpath("//*[@id='changeCityBox']/ul/li[1]/a")
        place.click()
        element = brower.find_element_by_xpath("//*[@id='search_input']")
        element.send_keys(text)
        element.send_keys(Keys.RETURN)

    def Textprocess(self,text):
        pass


    def Lagou(self,objects):
        results = []
        iters=0
        while iters<len(objects):
            print iters
            url = objects[iters].find_element_by_xpath("div[1]/div[1]/div[1]/a").get_attribute("href")
            print url
            if len(url)==38:
                result = [url[-12:-5]]
            else:
                result = [url[-11:-5]]
            html = self.OpenUrl1(url)
            html = BeautifulSoup(html,from_encoding='utf-8')

            try:
                html.find('dd',{'class':'job_request'}).p
            except:
                print "Enter Confirmcode!"
                time.sleep(30)
                continue

            content1 = html.find('dd',{'class':'job_request'}).p
            result.extend([i.get_text() for i in content1.findAll('span')]) 

            content2 = html.findAll('ul',{'class':'c_feature'})
            t = [i.get_text().strip()[3:] for i in content2[0].findAll('li')[0:2]]
            result.extend(t)
            t = [content2[1].find('li').get_text().strip()[5:]]
            result.extend(t)

            """ 处理任职条件的文本类容 利用jieba分词"""
            jobrequire = html.find('dd',{'class':'job_bt'})
            t = jobrequire.findAll('p')

            num = [0 for i in range(len(self.tools))]
            for i in t:
                texts = i.get_text().strip()
                words =[i for i in jieba.cut(texts,cut_all=True)]
                for j in range(len(self.tools)):
                    hupper = self.tools[j]
                    hlower = self.tools[j][0].lower()+self.tools[j][1:]
                    upper = self.tools[j].upper()
                    lower = self.tools[j].lower()
                    if (lower in words) or (upper in words) or (hupper in words) or (hlower in words):
                        num[j] += 1
            #print self.tools
            #print num
            result.extend(num)
            iters+=1
            results.append(result)
        return results

    def Lagou1(self,objects):

        results = []
        iters=1
        num = len(objects)
        print num
        while iters<num:
            url = objects[iters].find_element_by_xpath("div[1]/div[1]/div[1]/a").get_attribute("href")
            print url
            if len(url)==38:
                result = [url[-12:-5]]
            else:
                result = [url[-11:-5]]

            html = self.OpenUrl(url)
            html.page_source
            
            try:
                 html.find_element_by_xpath("//*[@id='job_detail']/dd[1]/p")
            except:
                print "Enter Confirmcode!"
                time.sleep(20)
                continue
            content1 = html.find_element_by_xpath("//*[@id='job_detail']/dd[1]/p")
            result.extend([i.text for i in content1.find_elements_by_xpath('span')]) 
            content2 = html.find_elements_by_xpath("//*[@id='container']/div[2]/dl/dd/ul")
            t = [i.text.strip()[3:] for i in content2[0].find_elements_by_xpath('li')[0:2]]
            result.extend(t)
            t = [content2[1].find_element_by_xpath('li').text.strip()[5:]]
            result.extend(t)

            iters+=1
            html.quit()
        return results



    
    def Deeppage(self,browser,target):
        self.Filltext(browser,target)
        browser.implicitly_wait(30)
        browser.page_source
        time.sleep(10)

        objects = browser.find_elements_by_xpath("//*[@id='s_position_list']/ul/li")
        FinalData = self.Lagou(objects)
        oldobjects = objects
        for i in range(1,30):
            print i
            nextpage =browser.find_elements_by_xpath("//*[@id='s_position_list']/div[2]/div/span")
            print len(nextpage)
            nextpage[-1].click()
            browser.implicitly_wait(30)
            browser.page_source
            time.sleep(10)
            objects = browser.find_elements_by_xpath("//*[@id='s_position_list']/ul/li")
            if oldobjects==objects:
                break
            oldobjects = objects
            FinalData.extend(self.Lagou(objects))
        print len(FinalData)
        h = self.tablehead
        h.extend(self.tools)
        print h
        FinalData.insert(0,h)
        return FinalData


if __name__ == '__main__':
       
       url = 'http://www.lagou.com'
       SP = Spider(url)
       browser = SP.OpenUrl(url)
       target = u'机器学习算法'
       data = SP.Deeppage(browser,target)
       
       data = pandas.DataFrame(data)
       print data
       data.to_csv('C:/Users/Qi/Desktop/spider/jiqixuexi.csv',encoding='utf-8')
       
       
    
