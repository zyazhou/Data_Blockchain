from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

class Lagou:
    def __init__(self,keyword,f):
        self.times=8
        self.driver = webdriver.Chrome()
        self.driver.minimize_window()
        self.url='https://www.lagou.com/'
        file_path = './files/scrapy_files/'
        self.file_path = file_path + keyword + '.txt'
        self.f=f


    def search(self ,keywords):
        self.driver.get(self.url)
        #self.driver.find_element_by_xpath("//a[@class='cboxClose']").click()
        self.driver.find_element_by_id("cboxClose").click()#通过id定位，这个点击按钮没有class
       # self.driver.find_element_by_css_selector("#cboxClose").click() #通过css选择器定位，要确保用到了css
        time.sleep(1) #等待一会，搜索框
        self.driver.find_element_by_css_selector("#search_input").send_keys(keywords)
        self.driver.find_element_by_xpath("//input[@id='search_button']").click()

        page_source=self.driver.page_source

        return  page_source

    def get_jobs(self,page_source):

      #  f = open(self.file_path, 'wb+')
        soup=BeautifulSoup(page_source,'lxml')
        hot_items=soup.select('.item__10RTO')
        for item in hot_items:
            d=dict()
            job_palce=item.select_one(".item-top__1Z3Zo>.position__21iOS>.p-top__1F7CL >a").get_text()
            s1 = job_palce.split('[')
            s2 = s1[1].split(']')
            d['job']=s1[0]
            d['position']=s2[0]
            d['company'] = item.select_one(".item-top__1Z3Zo>.company__2EsC8>.company-name__2-SjF > a").get_text()
            d['salary'] = item.select_one(".item-top__1Z3Zo>.position__21iOS>.p-bom__JlNur>.money__3Lkgq").get_text()
            temp=item.select_one(".item-top__1Z3Zo>.position__21iOS>.p-bom__JlNur").get_text()

            s1 = temp.split('验')
            s2 = s1[1].split('"')
            d['experience'] = s2[0]
            d['welfare']=item.select_one(".item-bom__cTJhu>.il__3lk85").get_text()

           # temp1=item.select_one(".item-bom__cTJhu>.ir___QwEG>span").get_text()
           # if(temp1==''):
           #     d['need_capacity'] =''
           # else:
           #     d['need_capacity'] =temp1

            #print(d)
            data = json.dumps(str(d),ensure_ascii=False).encode('utf8')  # 将str转化为二进制字节
            self.f.write(data + b'\n')
            d = {}





    def repeat(self):
        time.sleep(0.2)
        self.driver.find_element_by_css_selector('.order__3ikQO .order-item__34E7Q .option__21bte').click()
        #self.driver.find_element_by_css_selector(" .lg-pagination-next .lg-pagination-item-link").click()
        #self.driver.find_element_by_xpath(('//li[@class="lg-pagination-next"]').click())
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
        time.sleep(1)
        page_source=self.driver.page_source
        return page_source


if __name__ == '__main__':

    hot=Lagou()
    f = open('./files/scrapy_files/lagou.txt', 'wb+')
    page_source=hot.search('机器学习')
    f.write(hot.get_jobs(page_source) + b'\n')
    for i in  range (1,2):
        page_source0= hot.repeat()
        f.write(hot.get_jobs(page_source0) + b'\n')
    f.close()


    ##读取文件
    f = open('./files/scrapy_files/lagou.txt', 'rb+')
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    for line in lines:
        new = json.loads(line.decode('utf8'))
        print(new)
    f.close()



