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


class Spider(object):
    def __init__(self,initsite):
        self.initsite = initsite

    def OpenUrl(self,url):

        user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                    ]

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        agent = random.choice(user_agents)
        dcap["phantomjs.page.settings.userAgent"] = (agent,"(KHTML, like Gecko) Chrome/15.0.87")
        #Browser = webdriver.PhantomJS(desired_capabilities=dcap)
        Browser = webdriver.Chrome()
       
        Browser.get(url)
        
        return Browser

    def ChangeClick(self,browser,flag):
        opstart = browser.find_element_by_xpath("//span[@class='btn_more']")
        opend = browser.find_element_by_xpath("//a[@id='btn_cd_more']")
        opsort = browser.find_element_by_xpath("//ul[@class='condition_tags btn_select list_fl fl']/li[@data-type='cd-yy']")

        op_0 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='0']")
        op_3 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='3']")
        op_4 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='4']") 
        if flag==1:
            op1 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='8']")
            op2 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='5']")
            op3 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='1']")
            op4 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='2']")
            opstart.click()
            op1.click()
            op2.click()
            op3.click()
            op4.click()
            opend.click()
            #opsort.click()
        elif flag==2:
            op1 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='8']")
            op2 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='6']")
            op3 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='7']")
            op4 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='8']")
            op5 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='10']")
            op6 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='11']")
            op7 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='12']")
            opstart.click()
            op1.click()
            op2.click()
            op3.click()
            op4.click()
            op_0.click()
            op_3.click()
            op_4.click()
            op5.click()
            op6.click()
            op7.click()
            opend.click()
            #opsort.click()
        elif flag==3:
            op1 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_select list_fl fl']/li[@data-type='8']")
            op2 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='13']")
            op3 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='14']")
            op4 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='15']")
            op5 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='16']")
            op6 = browser.find_element_by_xpath("//ul[@class='condition_tags btn_more_option list_fl fl']/li[@data-type='17']")
            opstart.click()
            op1.click()
            op2.click()
            op3.click()
            op4.click()
            op_0.click()
            op_3.click()
            op_4.click()
            op5.click()
            op6.click()
            opend.click()
            #opsort.click()
        else:
            print "Not Exist"

    def GetContent_ty(self,browser):
        html = browser.page_source
        Object = BeautifulSoup(html,from_encoding='utf-8')
        App = Object.findAll('tr',{'class','bd'})
        final = []
        for item in App:
            result = []

            id = item.find('td',{'class','name'}).a['href']
            result.append(id)
            name = item.find('td',{'class','name'}).a.get_text()
            result.append(name)
            total = item.find('td',{'class','total'}).get_text()
            result.append(total)
            rate = item.find('td',{'class','rate'}).get_text()
            result.append(rate)
            pnum = item.find('td',{'class','pnum'}).get_text()
            result.append(pnum)
            cycle = item.find('td',{'class','cycle'}).get_text()
            result.append(cycle)
            plnum = item.find('td',{'class','p1num'}).get_text()
            result.append(plnum)
            fuload = item.find('td',{'class','fuload'}).get_text()
            result.append(fuload)
            alltotal = item.find('td',{'class','alltotal'}).get_text()
            result.append(alltotal)

            final.append(result)
        return final

    def Ty(self):
        sites = ['http://www.p2peye.com/platdata.html',
                 'http://www.p2peye.com/week.html',
                 'http://www.p2peye.com/month.html']
        index = ['day','week','month']

        for i in range(len(sites)):
                url = sites[i]
                browser = self.OpenUrl(url)
                final = SP.GetContent(browser)
                final_pd = pd.DataFrame(final)
                final_pd.to_csv('C:\\Users\Qi\\Desktop\\text'+index[i]+'.csv',encoding='utf-8')

    def Zj(self,site):
       url = site
       result1 = []
       result2 = []
       result3 = []
       for m in range(480):
            result1.append([])
            result2.append([])
            result3.append([])

       for i in range(1,4):
            browser = self.OpenUrl(url)
            browser.implicitly_wait(60)
            self.ChangeClick(browser,i)
            browser.page_source
            time.sleep(10)
            td = browser.find_elements_by_xpath('//td')
            td_num = len(td)
            print td_num

            j=0
            index = 0
            while j<=td_num-8:
                print j
                temp = []
                if i==1:
                    for k in range(j,j+8):
                        t = td[k].text
                        if k==j+2:
                            temp.append(t[0:-2])
                        elif k>j+2:
                            temp.append(t[0:-1])
                        else:
                            temp.append(t)
                    j=j+8
                elif i==2:
                    for k in range(j,j+8):
                        t = td[k].text
                        if k==j+3 or k==j+7:
                            temp.append(t[0:-1])
                        elif k==j+5:
                            temp.append(t[0:-3])
                        elif k<=j+1:
                            temp.append(t)
                        else:
                            temp.append(t[0:-2])
                    j=j+8
                else:
                    for k in range(j,j+7):
                        t = td[k].text
                        if k==j+2 or k==j+4:
                            temp.append(t[0:-2])
                        elif k<=j+1:
                            temp.append(t)
                        else:
                            temp.append(t[0:-1])
                    j=j+7

                if i==1:
                    result1[index].extend(temp)
                elif i==2:
                    result2[index].extend(temp)
                else:
                    result3[index].extend(temp)
                index+=1
            browser.quit()

       return result1,result2,result3

if __name__ == '__main__':
       
       url = 'http://shuju.wdzj.com/'
       SP = Spider(url)
       result1,result2,result3 = SP.Zj(url)
       
       ############### 以下程序将抓取的数据导入 MySql 数据库 ###########
       db = MySQLdb.connect("localhost","root","","test",charset='utf8')
       cursor = db.cursor()

       for i in range(1,len(result1)):
           print i
           t1 = result1[i]
           t2 = result2[i]
           t3 = result3[i]
           if len(t1)==0:
               continue
           sql1 = "insert into zhijia1 values\
                 ('%s','%s','%s','%s','%s','%s','%s','%s')" % (t1[0],t1[1],t1[2],t1[3],t1[4],t1[5],t1[6],t1[7])    
           
           sql2 = "insert into zhijia2 values\
                 ('%s','%s','%s','%s','%s','%s','%s','%s')" % (t2[0],t2[1],t2[2],t2[3],t2[4],t2[5],t2[6],t2[7])
           sql3 = "insert into zhijia3 values\
                 ('%s','%s','%s','%s','%s','%s','%s')" % (t3[0],t3[1],t3[2],t3[3],t3[4],t3[5],t3[6]) 
           
           
           cursor.execute(sql1) 
           cursor.execute(sql2)
           cursor.execute(sql3)
           db.commit()
        print "Scrapy successful!"
       
       
    
