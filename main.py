#coding:utf-8
import bs4
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import os
import pandas as pd
import time
import datetime
now_time = datetime.datetime.now().strftime('%Y-%m-%d')
def test_result(inner_url,title,source,date,wenhao):#检查异常值，测试用
    if inner_url==None or title==None or source==None or date==None or wenhao==None:
        # print([inner_url,title,source,date,wenhao])
        pass
def selenium_get_soup(url):
    option = webdriver.EdgeOptions()
    option.add_argument('headless')
    driver = webdriver.Edge(options=option)
    driver.get(url)
    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.close()
    return soup
def get_soup(url):
    headers = {
        # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    try:
        source = requests.get(url, headers=headers, timeout=10)
    except:
        return "获取信息超时！"
    source.encoding = source.apparent_encoding
    # data = source.json()
    soup = BeautifulSoup(source.text, 'html.parser')
    return soup
def get_json(url):
    headers = {
        # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
    try:
        source = requests.get(url, headers=headers, timeout=4)
    except:
        return "获取信息超时！"
    source.encoding = source.apparent_encoding
    if source.status_code==404 or source.status_code==500:
        return []
    data = source.json()
    return data
def check_back(url,checked_url):#检查url级数，重新拼接正确url
    if checked_url[:4]=='http':
        return checked_url
    pattern_back = re.compile(r'\.\./')
    level = pattern_back.findall(checked_url) # 查找'../'数量
    pattern_main = '[a-zA-z]+://[^\s\/]*/'
    match_main = re.search(pattern_main, url)[0]  # 将主域名拆分出来，
    # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
    # http://sthjt.shanxi.gov.cn/
    if checked_url[0]!='.' and checked_url[0]=='/':#不需要回退，主域名直接拼接
        return match_main[:-1]+checked_url
    matches_path = ['/'+i for i in re.sub(pattern_main,'',url).split('/') if i != '']
    # 将当前页面中的路径拆分出来，
    # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
    # ['/zwgk', '/hbbz', '/dfhjbhbz']
    ################
    # 此部分正则有问题
    # pattern_path = r'(?:http:\/\/[^\/]+\/?)?(?:\/([^\/]+))+?'
    # matches_path = ['/'+i for i in re.findall(pattern_path, url)]
    #################
    if checked_url[:2]=='./':#不用回退,？后面是参数，不看做路径，也需要去掉
        if not len(matches_path):
            return url+checked_url[2:]
        if matches_path[-1][1] != '?':
            match_main=url+checked_url[2:]
            return match_main
        else:
            level.append('1')#使得列表长度+1
            checked_url = '.'+checked_url#适配下面处理格式
    match_main = match_main[:-1]
    for i in range(len(matches_path)-len(level)):#有多少个'../'就去掉url后多少级
        match_main += matches_path[i]
    match_main += '/'+checked_url[len(level)*3:]#将checked_url前面的../去掉
    return match_main
# check_back('https://sthj.tj.gov.cn/ZWXX808/TZGG6419/','../../YWGZ7406/HJGL7886/SHJGL4585/202402/t20240226_6545184.html')

def list_to_excel(info_list,name):
    data = pd.DataFrame(data=info_list, columns=['链接', '标题', '发文机关', '日期', '文号','类型','爬取时间'])
    data.to_csv(os.getcwd()[:-2]+r'all_csv\data\{}-{}-{}.csv'.format(name,now_time,int(time.time())))

class sichuan:
    classname = '四川-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.lie2 > a')
        titles = [i.get('title') for i in title_href]
        href = [check_back(url,i.get('href')) for i in title_href]
        wenhaos = [i.get_text().strip() for i in soup.select('div.lie3')[1:]]
        templist = []
        for inner_url,title,wenhao in zip(href,titles,wenhaos):
            inner_soup = get_soup(inner_url)
            # print(inner_soup)
            date = inner_soup.select('div.zc-top > table > ul > li:nth-child(5)')
            if len(date):
                date = [i.get_text() for i in date][0][29:-1]
            else:
                date = None
            source = inner_soup.select('div.zc-top > table > ul > li:nth-child(2)')
            if len(source):
                source = [i.get('title') for i in source][0]
            else:
                source = None
            if wenhao.strip()=='':
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url,title,source,date,wenhao)
            print([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_sichuan_administrative_normative_documents(self, url):#行政规范性文件
        list_to_excel(self.template(url,'行政规范性文件'),self.classname+'行政规范性文件')
    def get_sichuan_other_documents(self,url):#其他文件
        list_to_excel(self.template(url,'其他文件'),self.classname+'其他文件')


class shanghai:
    classname = '上海-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.container > div > div.listn-right > div.listn-con > div > div > ul > li a')#主页面各文章标题与超链接
        # title = [i.get('title') for i in title_href]#标题
        href = [re.search('[a-zA-z]+://[^\s\/]*/',url)[0][:-1]+i.get('href') for i in title_href]#链接
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div[id=ivs_title]')[0].get_text().replace('\r','').replace('\n','').replace('\t','')  # 标题
            # title = re.search('[^\s]+',title)[0]
            source = None #难以爬取，暂时跳过
            date = inner_soup.select('[id=ivs_date]')[0].get_text()[1:-1]#日期
            wenhao = inner_soup.select('div.time > div:nth-child(7) > span')#文号
            if len(wenhao):
                wenhao = wenhao[0].get_text()
                if '〔〕号' in wenhao:
                    wenhao = None
            else:
                wenhao = None   #公告和地方性法规没有文号
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_shanghai_other_documents(self,url):#其他文件
        list_to_excel(self.template(url,'其他文件'),self.classname+'其他文件')
    def get_shanghai_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_shanghai_announcement(self,url):#公告通知
        list_to_excel(self.template(url,'公告通知'),self.classname+'公告通知')
    def get_shanghai_local_law(self,url):#地方性法规
        list_to_excel(self.template(url,'地方性法规'),self.classname+'地方性法规')

class beijing:
    classname = '北京-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.h_wz_m > ul > li > a')  # 标题和链接
        if not len(title_href):
            title_href = soup.select('div.colum_nr > div:nth-child(2) > div > ul > li > a')
        titles = [i.get('title') for i in title_href]  # 标题
        href = [check_back(url,i.get('href')) for i in title_href]  # 链接

        date = soup.select('div.colum_nr > div:nth-child(2) > div > ul > li > span:nth-child(1)')  # 日期
        if not len(date):
            date = soup.select('div.h_wz_m > ul > li > span:nth-child(1)')
        dates = [i.get_text() for i in date]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('div:nth-child(2) > div > ol > li:nth-child(2)')#发文机关
            source_split_num = 7
            if not len(source):
                source = inner_soup.select('div.h_dl_s > span:nth-child(1)')
                source_split_num = 3
            if len(source):
                source = [i.get_text() for i in source][0][source_split_num:]
            else:
                source = None
            union = inner_soup.select('div:nth-child(2) > div > ol > li:nth-child(3)')
            if len(union):
                union = [i.get_text() for i in union][0][9:]
                if source!=None and union != '----':
                    source += '、'+union
            else:
                union = None
            wenhao = inner_soup.select('div:nth-child(2) > div > ol > li:nth-child(6)')#文号
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0][7:]
                if wenhao=='----':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_beijing_local_standards(self,url):#地方标准，没有文号
        list_to_excel(self.template(url,'地方标准'),self.classname+'地方标准')
    def get_beijing_announcement(self,url):#通知公告，没有文号
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
    def get_beijing_policy(self,url):#政策文件
        list_to_excel(self.template(url,'政策文件'),self.classname+'政策文件')

class tianjin:
    classname = '天津-'
    def template(self,url,attr):#通知公告
        soup = get_soup(url)
        title_href = soup.select('div.commonList-body > ul > li > a')  # 标题和链接
        titles = [i.get('title') for i in title_href]  # 标题
        # href = [re.search('[a-zA-z]+://[^\s\/]*/', url)[0][:-1] + i.get('href')[5:] if i.get('href')[:5]=='../..' else url + i.get('href')[2:] for i in title_href]  # 链接
        href = [check_back(url,i.get('href')) for i in title_href]  # 链接
        dates = soup.select('div.commonList-body > ul > li > p')
        dates = [i.get_text().replace('\n','').strip() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = inner_soup.select('div.ty-content-title > p.ty-content-main-title')#标题
            # title = [i.get_text() for i in title][0].replace(' ','').replace('\n','')
            source = inner_soup.select('div.ty-content-bsmain > span:nth-child(1)')#发文机关
            source_split = 3
            if not len(source):
                source = inner_soup.select('div.xl-zw-top > div > div:nth-child(3) > div.sx-con')
                source_split = 0
            if len(source):
                source = [i.get_text() for i in source][0][source_split:]
            else:
                source = None
            # date = inner_soup.select('#content_fbrq')#日期
            # date = [i.get_text() for i in date][0][5:]
            #没有文号
            wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_tianjin_announcement(self,url):#通知公告，没有文号
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
class hebei:
    classname = '河北-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.lis_title.fl.td2 > a')#标题和链接
        href = [re.search('[a-zA-z]+://[^\s\/]*/', url)[0][:-1] + i.get('href') for i in title_href]  # 链接
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div.p_nei > h1')#标题
            title = [i.get_text() for i in title][0].replace(' ', '').replace('\n', '')
            source = inner_soup.select('div.p_nei > h4 > span:nth-child(2)')#发布机关
            source = [i.get_text() for i in source][0][5:]
            date = inner_soup.select('div.p_nei > h4 > span:nth-child(1)')#日期
            date = [i.get_text() for i in date][0][5:]
            #没有文号，但有文号表格位置
            wenhao = inner_soup.select('div.Bodyhead > table > tbody > tr:nth-child(3) > td:nth-child(4)')
            if len(wenhao):
                wenhao = [i.get_text().strip() for i in wenhao][0]
                if wenhao=='':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_hebei_announcement(self,url):#通知公告，没有文号
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')

class shanxi:
    classname = '山西-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.list-details-bar > ul.list-details > li > a')#标题和链接，地方标准网站、厅发规范性网站
        if len(title_href)==0 or title_href==None:
            title_href = soup.select('div.xxgk_main > div.main-box > div.p_right_box > div.p_right_ListBox.p_right_Scroll > ul > li > a')#规范性文件网站
        href = [check_back(url,i.get('href')) for i in title_href]  # 链接
        titles = [i.get('title') if i.get('title')!='' and i.get('title')!=None and 'cssbody' not in i.get('title') else i.get_text().replace('\n','').strip() for i in title_href]
        dates = soup.select('div.list-details-bar > ul > li > span')#日期
        if not len(dates):
            dates = soup.select('div.xxgk_main > div.main-box > div.p_right_box > div.p_right_ListBox.p_right_Scroll > ul > li > span')
        dates = [i.get_text().replace(' ','')[1:-1].replace('\n','') for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            try:
                title_check = inner_soup.select('#lbl_CWRQ')[1]#标题
            except:
                title_check = []
            if len(title_check) != 0 and title_check != None:
                # title = [i.get_text() for i in title][0].strip('\xa0').replace('\u200b','')#山西省生态环境厅\u200b关于优化调整全省重污染天
                source = inner_soup.select('#lbl_FWJG')  # 发文机关
                source = [i.get_text() for i in source][0].strip('\xa0')
                # date = inner_soup.select('#lbl_FBRQ')  # 发布日期
                # date = [i.get_text() for i in date][0].strip('\xa0')
                try:
                    wenhao = inner_soup.select('#lbl_WH')  # 文号
                    wenhao = [i.get_text() for i in wenhao][0].strip('\xa0')
                except:
                    wenhao = None
            # written_date = inner_soup.select('div.text-details > table > tbody > tr:nth-child(3) > td:nth-child(4) > span')#成文日期
            # written_date = [i.get_text() for i in written_date][0]
            # index_number = inner_soup.select('div.text-details > table > tbody > tr:nth-child(1) > td:nth-child(2) > span')#索引号
            # index_number = [i.get_text() for i in index_number]
                templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            else:#网页上部没有表格的网页
                # title = inner_soup.select('div.text-details > h2')#标题
                # title = [i.get_text() for i in title][0]
                # title = title.strip('\n').strip()
                source = inner_soup.select('div.text-details > p')  # 发文机关
                source = [i.get_text() for i in source][0]
                source = re.search('来源：([^\s]+)', source)[0][3:]
                # date = inner_soup.select('div.text-details > p')  # 发布日期
                # date = [i.get_text() for i in date][0]
                # date = re.search('编辑时间：(\d{4}-\d{2}-\d{2})',date)[0][5:]
                wenhao = None
                templist.append([inner_url, title, source, date,wenhao,attr,now_time])
                test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_shanxi_local_standards(self,url):#地方标准
        list_to_excel(self.template(url,'地方标准'),self.classname+'地方标准')
    def get_shanxi_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_shanxi_Departmental_normative_documents(self,url):#厅发规范性文件
        list_to_excel(self.template(url,'厅发规范性文件'),self.classname+'厅发规范性文件')

class neimenggu:
    classname = '内蒙古-'
    def montage_url(self,url, checked_url):  #重新拼接正确url
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        match_main = re.search(pattern_main, url)[0]  # 将主域名拆分出来，
        # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
        # http://sthjt.shanxi.gov.cn/
        if checked_url[0] != '.':  # 不需要回退，主域名直接拼接
            return match_main[:-1] + checked_url
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        # 将当前页面中的路径拆分出来，
        # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
        # ['/zwgk', '/hbbz', '/dfhjbhbz']
        if checked_url[:2] == './':  # 内蒙古特殊处理，将最后一级路径替换为正确路径
            match_main = match_main[:-1]
            for i in range(len(matches_path) - 1):
                match_main += matches_path[i]
            match_main += checked_url[1:]
            return match_main
    def get_true_url(self,url):
        soup = get_soup(url)  # https://sthjt.nmg.gov.cn/xxgk/zfxxgk/fdzdgknr/?gk=3&cid=16280爬不到正确数据，需要获取含有数据的正确url
        true_url = soup.select('#barrierfree_container > div > div:nth-child(2) > div > ul > li.on > div > div:nth-child(1) > a')[0].get('data-url')
        # 网页左侧菜单栏-法定主动公开内容-行政规范性文件   包含正确url路径
        url = self.montage_url(url, true_url)  # 将最后一级路径替换为正确路径
        return url
    def template(self,url,attr):
        soup = get_soup(self.get_true_url(url))#爬取正确url
        title_href = soup.select('tbody > tr > td:nth-child(2) > a')#标题和链接，地方标准网站、厅发规范性网站
        href = [check_back(url,i.get('href')) for i in title_href]  # 链接
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('h3.xiLanTitle')  # 标题
            title = [i.get_text() for i in title][0].replace('\n', '').replace(' ', '')
            source = inner_soup.select('tr:nth-child(3) > td:nth-child(2)')  # 发布机关
            source = [i.get_text() for i in source][0].replace('\n', '').replace(' ', '')
            date = inner_soup.select('div.xlBtn > div.xlBtnLeft')[0]  # 日期
            try:
                date = re.search('发布时间： (\d{4}-\d{2}-\d{2})', date.get_text())[0][6:]
            except:
                date = re.search('发布时间：(\d{4}-\d{2}-\d{2})', date.get_text())[0][5:]  # 中间多个空格
            try:
                wenhao = inner_soup.select('tr:nth-child(3) > td:nth-child(4)')  # 文号
                wenhao = [i.get_text() for i in wenhao][0].replace('\n', '').replace(' ', '')
            except:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_neimenggu_local_law(self,url):#地方法规规章
        list_to_excel(self.template(url,'地方法规规章'),self.classname+'地方法规规章')
class liaoning:
    classname = '辽宁-'
    def template_1(self,url,attr):#通知公告模板
        soup = get_soup(url)
        title_href = soup.select('div:nth-child(2) > ul > li > a')#链接与标题
        href = [check_back(url, i.get('href')) for i in title_href]  # 链接
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div.zy_content > h2.zy_title')#标题
            title = [i.get_text() for i in title][0]
            source = inner_soup.select('div.zy_content > div.info > span:nth-child(4)')#发文机关
            source = [i.get_text() for i in source][0][3:].strip()
            date = inner_soup.select('div.zy_content > div.info > span:nth-child(5)')  # 发布日期
            date = [i.get_text() for i in date][0][3:].replace('年','-').replace('月','-').replace('日','')
            wenhao = None
            templist.append([inner_url, title, source, date,wenhao,attr,now_time])
        print(templist)
        return templist
    def template_2(self,url,attr,source_id):#辽环函、辽环发、辽环办、其他 模板
        all_source_id = [353,354,355,356]#辽环函、辽环发、辽环办、其他id
        templist = []
        #观察网页实际展示数据考虑到四个来源加起来长度超过每页20的限制，只爬取第一页可能会有遗漏，故采用每个来源各爬20条保证都照顾到
        true_url = 'https://sthj.ln.gov.cn/eportal/ui?moduleId=5&portal.url=/portlet/xxgkml!queryList.portlet&pageNo=1&pageSize=20&flmc=tcfl&fldm={}'.format(source_id)
        #取自https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml的xhr类型
        #url中的pagesize可根据具体数据量要求修改
        soup = get_json(true_url)
        data = soup['result']
        href = [check_back(url,i['url']) for i in data]
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div.zy_content > h2')#标题
            title = [i.get_text() for i in title][0]
            source = inner_soup.select('div.headInfo > table > tbody > tr:nth-child(2) > td:nth-child(1)')#发文机关
            source = [i.get_text() for i in source][0][5:]#若为空字符串可以设置None
            date = inner_soup.select('div.headInfo > table > tbody > tr:nth-child(2) > td:nth-child(2)')#日期
            date = [i.get_text() for i in date][0][5:].replace('年','-').replace('月','-').replace('日','')
            try:
                wenhao = inner_soup.select('div.headInfo > table > tbody > tr:nth-child(3) > td:nth-child(2)')  # 文号
                wenhao = [i.get_text() for i in wenhao][0][3:]#若为空字符串可以设置None
            except:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_liaoning_announcement(self,url):#通知公告
        list_to_excel(self.template_1(url,'通知公告'),self.classname+'通知公告')
    def get_liaoning_liaohuanhan(self,url):#辽环函
        list_to_excel(self.template_2(url,'辽环函',353),self.classname+'辽环函')
    def get_liaoning_liaohuanfa(self,url):#辽环发
        list_to_excel(self.template_2(url,'辽环发',354),self.classname+'辽环发')
    def get_liaoning_liaohuanban(self,url):#辽环办
        list_to_excel(self.template_2(url,'辽环办',355),self.classname+'辽环办')
    def get_liaoning_other(self,url):#其他
        list_to_excel(self.template_2(url,'其他',356),self.classname+'其他')
class jilin:
    classname = '吉林-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.w100.mt36 > div.e_rdhy > ul > li > a')
        href = [check_back(url, i.get('href')) for i in title_href]  # 链接
        titles = [i.get('title') for i in title_href]
        dates = soup.select('div.w100.mt36 > div.e_rdhy > ul > li > span')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = inner_soup.select('div.tzgg_tzzd.mt50 > p:nth-child(5)')#标题
            # print(inner_url)
            # print(title)
            # title = [i.get_text() for i in title][0][9:]
            source = inner_soup.select('div.w100.mt36 > div > div.n_dqwz_c > script')#发文机关
            if len(source):
                source = [i.get_text() for i in source][0]
                source = re.search('document.write\("(.*?)"\)',source)[0][16:-2]
            else:
                source = None
            ###############
            # html代码：
            #<div class="n_dqwz_c">2023-09-12 10:07:33&nbsp;&nbsp; 来源：
            # <script type="text/javascript">
            #  var laiyuan = '';
            #  if(laiyuan == ""){
            #    document.write("吉林省生态环境厅");
            #  }else{
            #    document.write(laiyuan);
            #  }
            # </script>吉林省生态环境厅
            # </div>#
            #script意义不明，直接用正则匹配document.write内部字符串
            # date = inner_soup.select('div.tzgg_tzzd.mt50 > p:nth-child(7)')#日期
            # if len(date):
            #     date = [i.get_text() for i in date][0][5:]
            # else:
            #     date = None
            try:
                wenhao = inner_soup.select('div.tzgg_tzzd.mt50 > p:nth-child(6)')  # 文号
                wenhao = [i.get_text() for i in wenhao][0][5:]
            except:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_jilin_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
class heilongjiang:
    classname = '黑龙江-'
    def get_true_url(self,url):#获取可用于爬取的url
        soup = get_soup(url)
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        match_main = re.search(pattern_main, url)[0]  # 将主域名拆分出来，
        # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
        # http://sthjt.shanxi.gov.cn/
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        # 将当前页面中的路径拆分出来，
        # http://sthjt.shanxi.gov.cn/zwgk/hbbz/dfhjbhbz/拆分结果为
        # ['/zwgk', '/hbbz', '/dfhjbhbz']
        channelid_url = 'http://sthj.hlj.gov.cn/common/getChannelList?channelCode={}&websiteCodeName=sthj'.format(matches_path[1][1:])#获取所有模块的channelid
        data_soup = get_json(channelid_url)
        channel_list = data_soup['results']['children']
        channelid = ''
        for channel in channel_list:#遍历检查获取行政规范性文件的channelid,一般就是第一个,实际只循环一次,考虑以后获取其他文件的需求做成循环
            if channel['displayName'] == '规章':
                channelid = channel['channelId']
                break
        if channelid=='':
            return ''
        true_url = 'http://sthj.hlj.gov.cn/common/search/{}?_isAgg=true&_isJson=true&_pageSize=10&_template=index&_rangeTimeGte=&_channelName=&page=1'.format(channelid)
        return true_url
    def template(self,url,attr):
        soup = get_json(self.get_true_url(url))
        data = soup['data']['results']
        href = []
        titles = []
        dates = []
        for i in range(soup['data']['rows']):
            href.append(check_back(url,data[i]['url']))
            titles.append(data[i]['title'])
            dates.append(data[i]['publishedTimeStr'][:-9])
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = inner_soup.select('div.mainbox.clearfix > h1 > ucaptitle')
            # if len(title):
            #     title = [i.get_text() for i in title][0].replace('\r','').replace('\n','').replace(' ','')
            # else:
            #     title = None#只有标题而链接失效的，丢弃标题

            # date = inner_soup.select('div.mainbox.clearfix > div.article_attr.clearfix > div.article_attr_l > span.date > b')#日期
            # if len(date):
            #     date = [i.get_text() for i in date][0]
            # else:
            #     date = None#数据缺失处理

            source1 = inner_soup.select('div.mainbox.clearfix > div.article_attr.clearfix > div.article_attr_l > span.ly > b')#副标题内发文机构
            source2 = inner_soup.select('div.detail_xxgk_info.zcwj > ul > li:nth-child(3) > div')#上部表格内发文机构
            # 哪个爬下来用哪个
            if len(source1)>len(source2):#排除掉没有标签的
                source = [i.get_text() for i in source1][0]
            elif len(source1)<len(source2):
                source = [i.get_text() for i in source2][0]
            elif len(source1)==len(source2)!=0:#排除掉有标签没文本的
                if [i.get_text() for i in source1][0] == None or [i.get_text() for i in source1][0] == '':
                    source = [i.get_text() for i in source2][0]
                else:
                    source = [i.get_text() for i in source1][0]
                if source=='':
                    source = None
            else:
                source = None#数据缺失处理

            wenhao = inner_soup.select('div.detail_xxgk_info.zcwj > ul > li:nth-child(6) > div')#文号
            if len(wenhao) and [i.get_text() for i in wenhao][0]!='' and [i.get_text() for i in wenhao][0]!=',':
                wenhao = [i.get_text() for i in wenhao][0]
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_heilongjiang_administrative_normative_documents(self,url):#行政规范性文件
        list_to_excel(self.template(url,'行政规范性文件'),self.classname+'行政规范性文件')
class jiangsu:
    classname = '江苏-'
    def get_wenhao(self,inner_soup,selector):#将重复的处理文号的工作抽出来
        wenhao = inner_soup.select(selector)
        if len(wenhao):
            wenhao = [i.get_text() for i in wenhao][0]
            wenhao = re.search('[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)', wenhao)
            if wenhao != None:
                wenhao = wenhao.group(0)
                return wenhao
            else:
                return None
        else:
            return None

    def text_set(self,text):#直接用正则将所需标签匹配出来
        temp_text = text
        # del_list = ['<record>','</record>','<![CDATA[',']]>','<recordset>','</recordset>','<datastore>','</datastore>']
        # for del_str in del_list:
        #     temp_text = temp_text.replace(del_str,'')
        pattern = re.compile(r'<li class="cf" style=".*?;"><a href=".*?" target="_blank" title=".*?">.*?</a><span>.*?</span></li>')
        match_text = pattern.findall(temp_text)
        set_text = ''
        for i in match_text:
            set_text += i
        return set_text
    def special_soup(self,url):#江苏省网页代码含有<record>以及<![CDATA[',']]>等无法解析的标签，需要对源代码进行处理
        headers = {
            # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        try:
            source = requests.get(url, headers=headers, timeout=4)
        except:
            return "获取信息超时！"
        source.encoding = source.apparent_encoding
        soup = BeautifulSoup(self.text_set(source.text), 'html.parser')
        return soup
    def template(self,url,attr):
        soup = self.special_soup(url)
        title_href = soup.select('li > a')
        titles = [i.get('title') for i in title_href]
        href = [check_back(url,i.get('href')) for i in title_href]
        dates = soup.select('li > span')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # try:
            #     title = inner_soup.select('div.main-con > div:nth-child(1) > h1')#标题
            #     title = [i.get_text() for i in title][0]
            # except:
            #     title = None#失效链接处理
            source = inner_soup.select('div.main-con > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(1)')#发文机关
            if len(source):
                source = [i.get_text() for i in source][0][5:]
            else:
                source = None
            # date = inner_soup.select('div.main-con > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2)')#日期
            # if not len(date):
            #     date = inner_soup.select('div.main-con > div:nth-child(1) > div > span:nth-child(1)')  # 日期
            # if len(date):
            #     date = [i.get_text() for i in date][0][5:]
            # else:
            #     date = None
            wenhao = self.get_wenhao(inner_soup,'div.main-con > div.zoom > p > a')#http://sthjt.jiangsu.gov.cn/art/2018/11/5/art_89427_11044343.html爬正文内容
            if wenhao == None:#http://sthjt.jiangsu.gov.cn/art/2019/1/7/art_83738_10098271.html爬正文内容
                wenhao = self.get_wenhao(inner_soup,'div.main-con > div.zoom > a')
            if wenhao == None:#http://sthjt.jiangsu.gov.cn/art/2023/10/18/art_89427_11044340.html#爬文件编号
                wenhao = self.get_wenhao(inner_soup,'div.main-con > div:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            if wenhao == None:#http://sthjt.jiangsu.gov.cn/art/2023/10/18/art_89427_11044340.html爬内容摘要
                wenhao = self.get_wenhao(inner_soup,'div.main-con > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(1)')

            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_jiangsu_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_jiangsu_law(self,url):#法律法规规章
        list_to_excel(self.template(url,'法律法规规章'),self.classname+'法律法规规章')
    def get_jiangsu_ecological_environment_standards(self,url):#生态环境标准
        list_to_excel(self.template(url,'生态环境标准'),self.classname+'生态环境标准')
class zhejiang:
    classname = '浙江-'
    def text_set(self,text):#直接用正则将所需标签匹配出来
        temp_text = text
        # del_list = ['<record>','</record>','<![CDATA[',']]>','<recordset>','</recordset>','<datastore>','</datastore>']
        # for del_str in del_list:
        #     temp_text = temp_text.replace(del_str,'')
        pattern = re.compile(r'<table[^>]+>(.*?)</table>')
        match_text = pattern.findall(temp_text)
        set_text = ''
        for i in match_text:
            set_text += i
        return set_text
    def special_soup(self,url):#江苏省网页代码含有<record>以及<![CDATA[',']]>等无法解析的标签，需要对源代码进行处理
        headers = {
            # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        try:
            source = requests.get(url, headers=headers, timeout=4)
        except:
            return "获取信息超时！"
        source.encoding = source.apparent_encoding
        soup = BeautifulSoup(self.text_set(source.text), 'html.parser')
        return soup
    def template(self,url,attr):
        soup = self.special_soup(url)
        title_href = soup.select('tr > td:nth-child(1) > a')#标题与链接
        titles = [i.get('title') for i in title_href]
        dates = soup.select('tr > td:nth-child(2)')
        dates = [i.get_text()[1:-1] for i in dates]
        href = [check_back(url,i.get('href')) for i in title_href]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = inner_soup.select('tr:nth-child(1) > td.title')#标题
            # if not len(title):
            #     title = inner_soup.select('table:nth-child(13) > tbody > tr > td')
            # if not len(title):
            #     title = inner_soup.select('td.wzbt')
            # if len(title):
            #     title = [i.get_text() for i in title][0].replace('\r','').replace('\n','').replace(' ','').replace('\t','')
            # else:
            #     title = None
            source_type = 3
            source = inner_soup.select('table#article > tr:nth-child(2) > td:nth-child(1) > table > tr:nth-child(1) > td:nth-child(3)')#发文机关http://sthjt.zj.gov.cn/art/2024/2/7/art_1201919_58955109.html
            if not len(source):#https://minyi.zjzwfw.gov.cn/dczjnewls/dczj/idea/topic_12760.html
                source = inner_soup.select('table:nth-child(15) > tbody > tr:nth-child(2) > td:nth-child(1)')
                source_type = 5
            if not len(source):#https://www.zj.gov.cn/art/2021/2/10/art_1229417063_2247400.html
                source = inner_soup.select('li.laiyuan')
                source_type = 3
            if len(source):
                source = [i.get_text() for i in source][0][source_type:].replace('\r','').replace('\n','').replace(' ','').replace('\t','')
            else:
                source = None
            # date_type = 5
            # date = inner_soup.select('table#article > tr:nth-child(2) > td:nth-child(1) > table > tr:nth-child(1) > td:nth-child(1) > span')#日期
            # if not len(date):
            #     date = inner_soup.select('table:nth-child(15) > tbody > tr:nth-child(2) > td:nth-child(2)')#日期
            # if not len(date):
            #     date = inner_soup.select('ul.list > li:nth-child(1)')
            #     date_type = 3
            # if len(date):
            #     date = [i.get_text() for i in date][0].replace('\t','').replace('\r','').replace('\n','')[date_type:]
            # else:
            #     date = None
            wenhao = inner_soup.select('div.headInfo > div > table > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)')#文号
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao=='-':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_zhejiang_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
    def get_zhejiang_local_law(self,url):#地方法规规章
        list_to_excel(self.template(url,'地方法规规章'),self.classname+'地方法规规章')
    def get_zhejiang_local_standards(self,url):#地方标准
        list_to_excel(self.template(url,'地方标准'),self.classname+'地方标准')
class anhui:
    classname = '安徽-'
    def get_true_url(self,url):#获取正确url
        soup = get_soup(url)
        siteId = soup.select('head > meta[name=SiteId]')[0].get('content')
        pageSize = '15'
        organId = "21691"
        type = [4,6]#4是信息公开,6是行政规范性文件
        fileNum = ''
        filterFileNum = ''
        catIds = re.search('yxCatId = "[0-9]+"',soup.select('body > script')[0].get_text())[0][11:-1]
        fromCode = 'title'
        sortType = '1'
        fuzzySearch = 'false'
        keyWords = ''
        isInvalid = '0'
        result =  "暂无相关信息"
        file = "/jh5/publicInfoList_xzgfk"
        publicDivId = 'tab_0_0'
        isInvalid = '0,5'
        the_url = 'https://sthjt.ah.gov.cn/site/label/8888?labelName=publicInfoList&siteId={siteId}&pageSize=15&pageIndex=1&isDate=true&dateFormat=yyyy-MM-dd&length=50&active=0&organId={organId}&type={type}&fileNum=&filterFileNum=&catIds={catIds}&fromCode=title&sortType=1&action=list&fuzzySearch=false&keyWords=&publicDivId=tab_0_0&isInvalid=0%2C5&result=暂无相关信息&file=%2Fjh5%2FpublicInfoList_xzgfk'.format(siteId=siteId,organId = organId,type=type[1],catIds=catIds)
        # print(the_url)
        return the_url
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.gk_list > ul > li > div > a.title')#标题和链接https://sthjt.ah.gov.cn/public/column/21691?type=4&action=list&nav=3&catId=32709621

        if not len(title_href):#https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng
            soup = get_soup(self.get_true_url(url))
            title_href = soup.select('div.title > a[class!=a]')
        href = [i.get('href') for i in title_href]
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('h1.newstitle')#标题
            if not len(title):
                title = inner_soup.select('div.div_table_suoyin > table > tbody > tr:nth-child(7) > td')
            if len(title):
                title = [i.get_text() for i in title][0].replace('\r', '').replace('\n', '').replace(' ', '').replace(
                    '\t', '')
            else:
                title = None
            source = inner_soup.select('tbody > tr:nth-child(3) > td')#发文机关
            if len(source)>1:
                source = [i for i in source if i.get_text()!='' and i.get_text()!=title]
            if len(source):
                source = [i.get_text() for i in source][0].replace('\r','').replace('\n','').replace(' ','').replace('\t','')
            else:
                source = None

            date = inner_soup.select('tbody > tr:nth-child(6) > td')#日期
            if len(date):#如果标签爬取成功
                date = date[0].get_text()
            else:
                date = ''
            date_check = re.search('\d{4}-\d{1,2}-\d{1,2}',date)
            if date_check is None:#如果日期标签爬取错误
                date = inner_soup.select('tbody > tr:nth-child(4) > td:nth-child(2)')
                if len(date):
                    date = date[0].get_text()
            if date=='' or date == []:
                date = None
            wenhao = inner_soup.select('table.table_suoyin.hidden-lg.hidden-md > tbody > tr > td#_fileNum')#文号
            if not len(wenhao):
                wenhao = inner_soup.select('table.table_suoyin > tbody > tr > td#_fileNum')
            if len(wenhao):#如果标签爬取正常
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao=='':#如果标签内没有内容
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_anhui_active_publicity(self,url):#法定主动公开内容-政策法规
        list_to_excel(self.template(url,'政策法规'),self.classname+'政策法规')
    def get_anhui_publicity(self,url):#政府信息公开-政策
        list_to_excel(self.template(url,'政策'),self.classname+'政策')

class fujian:
    classname = '福建-'
    def get_title(self,inner_soup):
        title = inner_soup.select('div.tabs.tab_base_01.rules_con1 > div.rules_tit')
        if not len(title):
            title = inner_soup.select('div.bt-big-top > h4')
        if not len(title):
            title = inner_soup.select('div.article_title_group > div')
        if len(title):
            return [i.get_text() for i in title][0].strip('\r\n\t')
        else:
            return None
    def get_source(self,inner_soup,title):
        source = inner_soup.select('div.syh > div.syh_box > div > span:nth-child(3)')
        if not len(source):
            source = inner_soup.select('span.article_source')
        if not len(source):#'http://sthjt.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/gfxwj/202305/t20230504_6162571.htm'
            #不完善
            temp = ''
            source_ting = re.search('(福建省[^\s]+厅){1,}',title)
            source_hui = re.search('(福建省[^\s]+会){1,}',title)
            source_ban = re.search('(福建省[^\s]+办){1,}',title)
            if source_ting!=None:
                for i in source_ting.groups():
                    temp += i+' '
            if source_hui != None:
                for i in source_hui.groups():
                    temp += i+' '
            if source_ban != None:
                for i in source_ban.groups():
                    temp += i + ' '
            if temp!='':
                return temp.strip()
        if len(source):
            source = [i.get_text() for i in source][0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
            temp = re.search('：[\u4e00-\u9fa5]+', source)
            if temp == None:
                temp = re.search(':[\u4e00-\u9fa5]+', source)
            if temp != None:
                source = temp.group(0)[1:]
            return source
        else:
            return None
    def get_date(self,inner_soup,soup,title,title_href):
        date = inner_soup.select('div.xl_big_bOX > div.lip.clearflx.lip2 > p > span:nth-child(1)')
        if not len(date):
            date = inner_soup.select('span.article_time')
        if not len(date):
            titles = [i.get('title') for i in title_href]
            index = titles.index(title)
            temp = soup.select('div.tabs.info_tabs.mar_t_large.mar_t_base_sm > div.rules_tabs_01 > dl:nth-child({}) > dd.trt-col-3.none_sm.slb_none'.format(index+1))
            temp = [i.get_text() for i in temp]
            if len(temp):
                temp = re.search('\d{4}-\d{1,2}-\d{1,2}',temp[0])
                if temp != None:
                    temp = temp.group(0)
                return temp
        if len(date):
            date = [i.get_text() for i in date][0]
            date = re.search('\d{4}-\d{1,2}-\d{1,2}',date)
            if date != None:
                date = date.group(0)
            return date
        else:
            return None

    def get_wenhao(self,inner_soup):
        split_num = 0   #切割字符串用
        wenhao = inner_soup.select('div.tabs.tab_base_01.rules_con1 > div.rules_tit1')
        if not len(wenhao):
            wenhao = inner_soup.select('div.syh > div.syh_box > div > span:nth-child(2)')
            split_num = 6
        if not len(wenhao):
            wenhao = inner_soup.select('div.index_box.shadow_base.pad_base > ul > li:nth-child(2)')
            split_num = 4
        # if not len(wenhao):#从内容中提取文号，不完善，只识别文章中出现的第一个文号，暂时注释掉
        #     wenhao = inner_soup.select('div.TRS_Editor > p')
        #     temp_str = ''
        #     for i in wenhao:
        #         temp_str +=i.get_text()
        #     temp_pattern = '(?<=[\(（])[\\u4E00-\\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)(?=[\)）])'
        #     temp = re.search(temp_pattern,temp_str)
        #     if temp!=None:
        #         return temp.group(0).replace('\n','').strip()
        #     else:
        #         return None
        if len(wenhao):
            return [i.get_text() for i in wenhao][0].strip('\n\r\t')[split_num:].replace('\n','').strip()
        else:
            return None
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.pad_l_base.pad_r_base.pad_l_base0_sm.pad_r_base0_sm > div:nth-child(3) > div > ul > li >a')#标题和链接
        if not len(title_href):
            title_href = soup.select('div.rules_tabs_01 > dl > dd > a')
        href = [check_back(url, i.get('href')) for i in title_href if i.get('href')!=None]
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = self.get_title(inner_soup)
            source = self.get_source(inner_soup,title)
            date = self.get_date(inner_soup,soup,title,title_href)
            wenhao = self.get_wenhao(inner_soup)
            title = title.replace('\u3000',' ').strip().replace('\n','').replace('\u2002','')#其他函数需要调用原始标题，故最后处理标题
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
        print(templist)
        return templist
    def get_fujian_policies_law(self,url):#政策法规
        list_to_excel(self.template(url,'政策法规'),self.classname+'政策法规')
    def get_fujian_announcement(self,url):#公告公示
        list_to_excel(self.template(url,'公告公示'),self.classname+'公告公示')
    def get_fujian_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_fujian_policy(self,url):#政策文件
        list_to_excel(self.template(url,'政策文件'),self.classname+'政策文件')

class jiangxi:#来源不完善#文号只有一个特例无法爬取
    classname = '江西-'
    def text_set(self,text):#直接用正则将所需标签匹配出来
        temp_text = text
        # del_list = ['<record>','</record>','<![CDATA[',']]>','<recordset>','</recordset>','<datastore>','</datastore>','<nextgroup>','</nextgroup>']
        # for del_str in del_list:
        #     temp_text = temp_text.replace(del_str,'')
        # return temp_text
        pattern = re.compile(r'<li>        <a href=".*?" target="_blank" title=".*?">.*?</a><span class=".*?">.*?</span>    </li>')
        match_text = pattern.findall(temp_text)
        set_text = ''
        for i in match_text:
            set_text += i
        return set_text
    def special_soup(self,url):#江西省网页代码含有<record>以及<![CDATA[',']]>等无法解析的标签，需要对源代码进行处理
        headers = {
            # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        try:
            source = requests.get(url, headers=headers, timeout=4)
        except:
            return "获取信息超时！"
        source.encoding = source.apparent_encoding
        soup = BeautifulSoup(self.text_set(source.text), 'html.parser')
        return soup
    def template(self,url,attr):
        soup = self.special_soup(url)
        title_href = soup.select('li > a')
        href = [check_back(url, i.get('href')) for i in title_href]
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('h1.title')
            title = [i.get_text() for i in title][0].strip('\r\n\t')
            source = inner_soup.select('div.resource')
            if len(source):
                source = [i.get_text() for i in source][0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')[5:]
            else:
                source = None
            date = inner_soup.select('div.sub-title > span:nth-child(1)')
            date = [i.get_text() for i in date][0][5:]
            wenhao = inner_soup.select('p[style*="text-align: center;"]')#http://sthjt.jiangxi.gov.cn/art/2020/7/20/art_42202_2796146.html  text-align: center
            #爬取不到的特例,p标签没有text-align: center
            #http://sthjt.jiangxi.gov.cn/art/2020/7/30/art_42202_2796154.html
            if not len(wenhao):
                wenhao = inner_soup.select('p[style*="text-align:center;"]')#http://sthjt.jiangxi.gov.cn/art/2018/6/12/art_42202_2796080.html  text-align:center
            if len(wenhao):
                temp_wenhao = ''
                for i in wenhao:
                    temp_wenhao += i.get_text().replace(' ','')+'\n'
                temp_wenhao = re.search('[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)',temp_wenhao)
                if temp_wenhao != None:
                    wenhao = temp_wenhao.group(0)
                else:
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, '1')
        print(templist)
        return templist
    def get_jiangxi_local_standards(self,url):#地方标准
        list_to_excel(self.template(url,'地方标准'),self.classname+'地方标准')
    def get_jiangxi_announcement(self,url):#公示公告
        list_to_excel(self.template(url,'公示公告'),self.classname+'公示公告')
    def get_jiangxi_plan(self,url):#规划计划
        list_to_excel(self.template(url,'规划计划'),self.classname+'规划计划')

class shandong:
    classname = '山东-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('ul > li.clearfix > a.tListTitleNormal')
        if not len(title_href):#20层表格一个id和class属性都没写
            title_href = soup.select('tr > td > a')
            title_href = [i for i in title_href if i.get('class') == None and i.get('onclick') == None]

        date = soup.select('ul > li.clearfix > span.tListTime')
        if not len(date):
            date = soup.select('tr > td.date14')
        dates = [i.get_text() for i in date]

        href = [check_back(url, i.get('href')) for i in title_href]
        # print(href)
        templist = []
        for inner_url,date in zip(href,dates):
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('strong.red_title')
            if not len(title):
                title = inner_soup.select('strong.black_title')
            title = [i.get_text() for i in title][0]
            source = inner_soup.select('table.jg > tr:nth-child(3) > td:nth-child(2)')
            if not len(source):#考虑福建类方法
                source = None
            else:
                source = [i.get_text() for i in source][0]
            wenhao = inner_soup.select('table.jg > tr:nth-child(4) > td:nth-child(2)')
            if not len(wenhao):
                wenhao = inner_soup.select('td.bk1 > table:nth-child(3) > tr:nth-child(2) > td > table > tr > td > span')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
            elif wenhao=='':
                wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url,title,source,date,wenhao)
        print(templist)
        return templist
    def get_shandong_policies_law(self,url):#政策法规
        list_to_excel(self.template(url,'政策法规'),self.classname+'政策法规')
    def get_shandong_normative_documents(self,url):#现行有效的规范性文件
        list_to_excel(self.template(url,'现行有效的规范性文件'),self.classname+'现行有效的规范性文件')
class hunan:
    classname = '湖南-'
    ######################
    #http://hnfg.hnrd.gov.cn/#/fileLibrary-detail?id=629219146155950080
    #该网站爬取难度大，签名难以伪造或生成，暂时跳过
    #以上已采用selenium解决
    #######################
    #http://sthjt.hunan.gov.cn/sthjt/xxgk/tzgg/index.html
    #通知公告爬取有问题，高概率爬不到24年数据，只有23年，多次爬取或在浏览器中手动刷新都有可能触发只显示23年数据的情况，原因不明
    #######################
    def get_url_text(self,url):#获取html源代码文本
        headers = {
            # 'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        try:
            source = requests.get(url, headers=headers, timeout=4)
        except:
            return "获取信息超时！"
        source.encoding = source.apparent_encoding
        return source.text
    def get_json_url(self,url):#获取json数据的url
        soup = self.get_url_text(url)
        channelid = re.search("var channelId =  '[0-9]+';",soup)
        if channelid != None:
            channelid = channelid.group(0)[18:-2]
        else:
            channelid = 'fail'
        return 'http://api.hunan.gov.cn/search/common/search/'+channelid
    def split_url(self,url):#拆出url中的指定部分
        pattern = 'id=[0-9]+'
        result = re.search(pattern,url)
        if result != None:
            result = result.group(0)[3:]
        else:
            result = ''
        return result
    # def get_title(self,inner_soup,url):
    #     title = inner_soup.select('#activity-name')#https://mp.weixin.qq.com/s?__biz=MzI2NDA3MzAwMA==&mid=2651395337&idx=2&sn=ef56f31c3381eb0ae369a8dbeeaae61d&chksm=f14f8f4ec63806587d08dc12659cf3571ea87dcdda879c01bb7bf91af8141191421de6256245&mpshare=1&scene=1&srcid=0816MHzYZOyHQxMYkIYNtjD9&sharer_sharetime=1692147131947&sharer_shareid=504012f0d14f4faec8b1104ebd3f9dfb#rd
    #     if not len(title):#https://www.hunan.gov.cn/hnszf/szf/hnzb_18/2023/202313/02222gqgsdsddtcfvurptpusubvvggrfbfffbrhukgepdkfqshfpuruegb/202307/t20230714_29401987.html
    #         # print(1)
    #         title = inner_soup.select('h3.sp_title')
    #     if not len(title):#http://sthjt.hunan.gov.cn/sthjt/xxgk/tzgg/gg/202312/t20231219_32515055.html
    #         # print(2)
    #         title = inner_soup.select('div.main_content > h2')
    #     if not len(title):#https://www.hnrd.gov.cn/content/646755/74/13313108.html
    #         # print(3)
    #         title = inner_soup.select('h1.detail_title')
    #     if not len(title):#http://amr.hunan.gov.cn/amr/zwx/xxgkmlx/tzggx/202310/t20231026_31720128.html
    #         # print(4)
    #         title = inner_soup.select('h3.title')
    #     if not len(title):#https://www.hunan.gov.cn/xxgk/zfgz/202312/t20231215_32512523.html
    #         # print(5)
    #         title = inner_soup.select('p:nth-child(3) > span')
    #     if not len(title):#http://hnfg.hnrd.gov.cn/#/fileLibrary-detail?id=629219146155950080   #爬取难度大，暂时跳过
    #         # print(6)
    #         inner_soup = get_json('http://218.76.24.131:8081/lzt/statute/regulatory/documents/bigData/info/'+self.split_url(url))
    #         try:
    #             title = inner_soup['data']['statuteTitle']#json
    #             return title
    #         except:
    #             title = []
    #     if len(title):
    #         title = [i.get_text() for i in title][0].strip()
    #     else:
    #         title = None
    #     return title
    def get_source(self,inner_soup,url):
        source = inner_soup.select('div.rul_note > p')#https://www.hunan.gov.cn/hnszf/xxgk/zfgz/202312/t20231229_32615461.html
        split_num_front = 0
        split_num_behind = -3
        if not len(source):
            source = inner_soup.select('div.xxgk_top_frame > ul > li:nth-child(3)')#http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/202305/t20230518_29342670.html
            if len(source):
                if source[0].get_text()[:4] != '发布机构':
                    source = inner_soup.select('div.xxgk_top_frame > ul > li:nth-child(2)')
            split_num_front = 6
            split_num_behind = -1
        if not len(source):
            source = inner_soup.select('#js_content > section > section > section > p:nth-child(1)')
            if len(source):
                source = [i for i in source if re.search('来源丨[\u4e00-\u9fa5]+',i.get_text()) != None]
            else:
                source = []
            split_num_front = 3
            split_num_behind = -1
        # if not len(source):#https://mp.weixin.qq.com/s?__biz=MzI2NDA3MzAwMA==&mid=2651395337&idx=2&sn=ef56f31c3381eb0ae369a8dbeeaae61d&chksm=f14f8f4ec63806587d08dc12659cf3571ea87dcdda879c01bb7bf91af8141191421de6256245&mpshare=1&scene=1&srcid=0816MHzYZOyHQxMYkIYNtjD9&sharer_sharetime=1692147131947&sharer_shareid=504012f0d14f4faec8b1104ebd3f9dfb#rd
        #     # print(2)
        #     source = inner_soup.select('#js_content > section > section:nth-child(7) > section > p:nth-child(1)')
        #     # js_content > section > section:nth-child(7) > section > p:nth-child(1)
        #     # js_content > section > section:nth-child(8) > section > p:nth-child(1) > span
        #     split_num_front = 3
        #     split_num_behind = -1
        # if not len(source):#https://mp.weixin.qq.com/s?__biz=MzI2NDA3MzAwMA==&mid=2651417554&idx=1&sn=457206cb31cd39e915c12a766db68810&chksm=f14ff195c6387883a17f2fc5d18486482cd9686da5943ac7ba120fab3c48450f1d752cf8dac0&mpshare=1&scene=23&srcid=1207Fl5fXeXwintQ0i5hPDyW&sharer_shareinfo=b30d895007ff16c84ef26b5c6c1508a7&sharer_shareinfo_first=b30d895007ff16c84ef26b5c6c1508a7#rd
        #     source = inner_soup.select('#js_content > section > section:nth-child(5) > section > p:nth-child(1)')
        #     split_num_front = 3
        #     split_num_behind = -1
        if not len(source):#https://www.hunan.gov.cn/hnszf/szf/hnzb_18/2023/202313/02222gqgsdsddtcfvurptpusubvvggrfbfffbrhukgepdkfqshfpuruegb/202307/t20230714_29401987.html
            # print(3)
            source = inner_soup.select('div.xly_bg > div.xly_Box > div.clearfix > div > div.chare-left')
            if len(source):
                source = [i.get_text() for i in source][0]
                source = re.search('信息来源：[\s]*[\u4e00-\u9fa5]+责任编辑', source)
                if source != None:
                    source = source.group(0)
                    split_num_front = 5
                    split_num_behind = -5
                else:
                    source = []
            else:
                source = []
        if not len(source):#https://www.hnrd.gov.cn/content/646755/74/13313108.html
            # print(4)
            source = inner_soup.select('section.box_left.f_left > div > span:nth-child(1)')
            split_num_front = 3
            split_num_behind = -1
        if not len(source):#https://amr.hunan.gov.cn/amr/zwx/xxgkmlx/tzggx/202310/t20231026_31720128.html
            # print(5)
            source = inner_soup.select('div.xxgk_top_frame > ul > li:nth-child(2)')
            split_num_front = 6
            split_num_behind = -1
        if not len(source):#http://hnfg.hnrd.gov.cn/#/fileLibrary-detail?id=629219146155950080
            temp_soup = selenium_get_soup(url)
            source = temp_soup.select('div.fileLibraryDetail.details > div.details-item-box > div:nth-child(2) > div > div.details-item-value')
            split_num_front = 0
            split_num_behind = -1
        if len(source):
            source = [i.get_text() for i in source][0]+' '
            if source.strip() != '':
                source = source[split_num_front:split_num_behind]
                if source == '':
                    source = None
            else:
                source = None
            return source
        else:
            return None
    # def get_date(self,inner_soup):#改用直接提取列表的方法，本方法弃用
    #     date = inner_soup.select('div.xxgk_top_frame > ul > li:nth-child(4)')#http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/202305/t20230518_29342670.html
    #     split_num = 6
    #     if not len(date):#https://mp.weixin.qq.com/s?__biz=MzI2NDA3MzAwMA==&mid=2651395337&idx=2&sn=ef56f31c3381eb0ae369a8dbeeaae61d&chksm=f14f8f4ec63806587d08dc12659cf3571ea87dcdda879c01bb7bf91af8141191421de6256245&mpshare=1&scene=1&srcid=0816MHzYZOyHQxMYkIYNtjD9&sharer_sharetime=1692147131947&sharer_shareid=504012f0d14f4faec8b1104ebd3f9dfb#rd
    #         date = inner_soup.select('#publish_time')
    #         split_num = 0
    #     if not len(date):#https://www.hunan.gov.cn/hnszf/szf/hnzb_18/2023/202313/02222gqgsdsddtcfvurptpusubvvggrfbfffbrhukgepdkfqshfpuruegb/202307/t20230714_29401987.html
    #         date = inner_soup.select('span.time')
    #         split_num = 6
    #     if not len(date):#https://www.hnrd.gov.cn/content/646755/74/13313108.html
    #         date = inner_soup.select('section.box_left.f_left > div > span:nth-child(4)')
    #         split_num = 0
    #     if not len(date):#https://amr.hunan.gov.cn/amr/zwx/xxgkmlx/tzggx/202310/t20231026_31720128.html
    #         date = inner_soup.select('div.xxgk_top_frame > ul > li:nth-child(3)')
    #         split_num = 6
    #     if len(date):
    #         date = [i.get_text() for i in date][0][split_num:].strip()
    #     else:
    #         date = None
    #     return date
    def get_wenhao(self,inner_soup,url):
        wenhao = inner_soup.select('#zoom > p:nth-child(4) > span')
        if not len(wenhao):#http://hnfg.hnrd.gov.cn/#/fileLibrary-detail?id=629219146155950080
            temp_soup = selenium_get_soup(url)
            wenhao = temp_soup.select('div.fileLibraryDetail.details > div.details-item-box > div:nth-child(4) > div.details-item-value')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0].strip()
                if wenhao=='':
                    wenhao = []
                else:
                    return wenhao
            else:
                wenhao = []
        if len(wenhao):
            wenhao = [i.get_text() for i in wenhao][0][12:-17]
        else:
            wenhao = None
        return wenhao
    def template(self,url,attr):
        soup = get_json(self.get_json_url(url))#数据为json格式
        if soup!=None and len(soup['data']['results']):
            href = [check_back(url,i['url']) for i in soup['data']['results']]
            dates = [i['publishedTimeStr'] for i in soup['data']['results']]
            titles = [i['title'] for i in soup['data']['results']]
        else:
            soup = get_soup(url)#数据为html格式
            title_href = soup.select('div.hy-list-text > ul > li > a')
            titles = [i.get('title') for i in title_href]
            href = [check_back(url, i.get('href')) for i in title_href]
            dates = soup.select('div.hy-list-text > ul > li > a > small')
            dates = [i.get_text() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = self.get_title(inner_soup,inner_url)#标题
            source = self.get_source(inner_soup,inner_url)#发文机关
            wenhao = self.get_wenhao(inner_soup,inner_url)#文号
            # date = self.get_date(inner_soup)
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_hunan_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
    def get_hunan_local_law(self,url):#地方性法规和政策
        list_to_excel(self.template(url,'地方性法规和政策'),self.classname+'地方性法规和政策')
    def get_hunan_normative_documents(self,url):#部门规章和规范性文件
        list_to_excel(self.template(url,'部门规章和规范性文件'),self.classname+'部门规章和规范性文件')

class hubei:
    classname = '湖北-'
    def get_order(self,info):
        return info['order']
    def template(self,url,attr):
        soup = get_json(url+'2022qtzdgk.json')#http://sthjt.hubei.gov.cn/fbjd/zc/zcwj/
        if len(soup):
            soup = soup['data']
            soup.sort(key=self.get_order,reverse=True)
            years = soup[0]['PubDate'][:4]
            href = []
            for i in soup:
                if i['PubDate'][:4] == years:
                    href.append(check_back(url,i['url']))
                else:
                    break
        else:
            #http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/hjbz/
            #http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/sthjfg/flfg/
            soup = get_soup(url)
            title_href = soup.select('ul.info-list > li > a')
            href = [check_back(url,i.get('href')) for i in title_href]
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div.article_new > h2')#标题
            if len(title):
                title = [i.get_text() for i in title][0]
            else:
                title = None

            source = inner_soup.select('div.ftable > div:nth-child(3) > div.ftd')#发文机关
            if len(source):
                source = [i.get_text() for i in source][0]
            else:
                source = None

            date = inner_soup.select('div.ftable > div:nth-child(4) > div.ftd')#日期
            if len(date):
                date = [i.get_text() for i in date][0]
                if date == '':
                    date = inner_soup.select('div.info.fl > span:nth-child(1) > em')
                    if len(date):
                        date = [i.get_text() for i in date][0]
                    else:
                        date =None
            else:
                date = None
            wenhao = inner_soup.select('div.ftable > div:nth-child(5) > div.ftd')#文号
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao=='无':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            # test_result(inner_url,title,source,date,wenhao)
        print(templist)
        return templist
    def get_hubei_active_publicity(self,url):#其他主动公开文件
        list_to_excel(self.template(url,'其他主动公开文件'),self.classname+'其他主动公开文件')
    def get_hubei_ecological_environment_standards(self,url):#生态环境标准
        list_to_excel(self.template(url,'生态环境标准'),self.classname+'生态环境标准')
    def get_hubei_local_law(self,url):#地方性法规规章
        list_to_excel(self.template(url,'地方性法规规章'),self.classname+'地方性法规规章')
class henan:
    classname = '河南-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.pdlist > ul > li > a')
        if not len(title_href):
            title_href = soup.select('ul.newslist > li > span.list_tit3 > a')
        href = [check_back(url,i.get('href')) for i in title_href]
        templist = []
        for inner_url in href:
            inner_soup = get_soup(inner_url)
            title = inner_soup.select('div.zw_con > h1')#标题
            if len(title):
                title = [i.get_text() for i in title][0]
            else:
                title = None
            source = inner_soup.select('#headContainer > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > span')#发文机关
            split_num = 0
            if not len(source):
                source = inner_soup.select('div.zw_con > h2 > span.zw_sta')
                split_num = 3
            if len(source):
                source = [i.get_text() for i in source][0][split_num:].strip()
                if source.strip()=='':
                    source = None
            else:
                source = None
            date = inner_soup.select('#headContainer > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > span')#日期
            split_num = 0
            if not len(date):
                date = inner_soup.select('div.zw_con > h2 > span.zw_time')
                split_num = 5
            if len(date):
                date = [i.get_text() for i in date][0][split_num:].strip()
            else:
                date = None
            wenhao = inner_soup.select('#headContainer > tbody > tr:nth-child(4) > td > table > tbody > tr > td:nth-child(1) > span')#文号
            if not len(wenhao):
                wenhao = None
            else:
                wenhao = [i.get_text() for i in wenhao][0]
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            # test_result(inner_url,title,source,date,wenhao)
        print(templist)
        return templist
    def get_henan_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
    def get_henan_environmental(self,url):#环保文件
        list_to_excel(self.template(url,'环保文件'),self.classname+'环保文件')

class guangdong:
    classname = '广东-'
    def get_true_url_1(self,url):#提取json数据的url    #https://gdee.gd.gov.cn/gkmlpt/index#3155
        result = re.search('index#[0-9]*',url)
        if result!=None:
            result = result.group(0)[6:]
        else:
            result = ''
        true_url = 'https://gdee.gd.gov.cn/gkmlpt/api/all/{}?page=1'.format(result)
        return true_url
    def get_true_url_2(self,url):#提取json数据的url  #https://gdee.gd.gov.cn/hdjlpt/yjzj/answer/34748
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        result = matches_path[-1][1:]
        true_url = 'https://gdee.gd.gov.cn/hdjlpt/yjzj/api/comments/?questionnaire_id={}&per_page=500&page=1'.format(result)
        return true_url
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.listimg_data > ul > li > div.list_table > a.titlelie')
        if not len(title_href):
            soup = get_json(self.get_true_url_1(url))
            title_href = soup['articles'][:20]
            href = [check_back(url,i['url']) for i in title_href]
            titles = [i['title'] for i in title_href]
            dates = [i['created_at'] for i in title_href]
        else:
            href = [check_back(url,i.get('href')) for i in title_href]
            titles = [i.get('title') for i in title_href]
            dates = soup.select('div.listimg_data > ul > li > div > span.list-date')
            dates = [i.get_text().strip() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)

            #从待爬取列表中直接提取，此部分弃用
            # title = inner_soup.select('div.headline.col-xs-12.col-sm-12.col-md-10.col-md-offset-1 > p')#.strip()#https://gdee.gd.gov.cn/hbwj/content/post_4142338.html
            # if not len(title):#https://gdee.gd.gov.cn/gkmlpt/content/4/4382/post_4382822.html#3158
            #     title = inner_soup.select('div.content > h1.title.document-number')
            # if not len(title):#https://gdee.gd.gov.cn/hdjlpt/yjzj/answer/34748
            #     json_soup = get_json(self.get_true_url_2(inner_url))
            #     if len(json_soup):
            #         title = json_soup['questionnaire']['title']
            #         if title.strip() == '':
            #             title = None
            #     else:
            #         title = []
            # if len(title):
            #     if not isinstance(title, str):
            #         title = [i.get_text() for i in title][0].strip()
            # else:
            #     title = None

            source = inner_soup.select('div.hidden-xs.hidden-sm.col-md-12 > div > div:nth-child(1) > span:nth-child(2)')#https://gdee.gd.gov.cn/hbwj/content/post_4142338.html
            split_num = 8
            if not len(source):#https://gdee.gd.gov.cn/gkmlpt/content/4/4382/post_4382822.html#3158
                source = inner_soup.select('div.classify > table > tr:nth-child(2) > td.td-value-xl > span')
                split_num = 0
            if len(source):
                source = [i.get_text() for i in source][0][split_num:]
            else:
                source = None

            # 从待爬取列表中直接提取，此部分弃用
            # date = inner_soup.select('div.hidden-xs.hidden-sm.col-md-12 > div > div:nth-child(1) > span:nth-child(1)')#https://gdee.gd.gov.cn/hbwj/content/post_4142338.html
            # if not len(date):#https://gdee.gd.gov.cn/gkmlpt/content/4/4382/post_4382822.html#3158
            #     date = inner_soup.select('div.date-row')
            # if not len(date):#https://gdee.gd.gov.cn/hdjlpt/yjzj/answer/34748
            #     json_soup = get_json(self.get_true_url_2(inner_url))
            #     if len(json_soup):
            #         date = json_soup['questionnaire']['created_at']
            #         if date.strip() == '':
            #             date = None
            #     else:
            #         date= []
            # if len(date):
            #     if not isinstance(date, str):
            #         date = [i.get_text() for i in date][0].strip()
            #         date = re.search('\d{4}-\d{1,2}-\d{1,2}',date).group(0)
            # else:
            #     date = None

            wenhao = inner_soup.select('#panel_article2 > p:nth-child(2) > span')#https://gdee.gd.gov.cn/hbwj/content/post_4142338.html
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_4081264.html
                wenhao = inner_soup.select('#panel_article2 > p:nth-child(1) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_3926655.html
                wenhao = inner_soup.select('#panel_article > div > div > p:nth-child(2) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_3836322.html
                wenhao = inner_soup.select('#logPanel > p:nth-child(2) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_3312396.html
                wenhao = inner_soup.select('#panel_article > p:nth-child(2) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_3126451.html
                wenhao = inner_soup.select('#panel_article > div > p:nth-child(2) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/hbwj/content/post_4081264.html
                wenhao = inner_soup.select('#logPanel > p:nth-child(3) > span')
            if not len(wenhao):#https://gdee.gd.gov.cn/gkmlpt/content/2/2963/post_2963244.html#3155
                wenhao = inner_soup.select('div.classify > table > tr:nth-child(4) > td.td-value-xl > span')
            #可以考虑采用更模糊的选择器匹配方式，然后使用正则表达式[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)
            #去匹配网页中出现的第一个文号，缺点是可能匹配到文章中提及而非文章本身的文号
            #不完善

            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao.strip() == '':
                    wenhao = None
                if wenhao != None:#如果文号不为空字符串时检查字符串是否为文号
                    wenhao = re.search('[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)',wenhao)
                if wenhao!=None:#如果正则匹配成功
                    wenhao = wenhao.group(0)
                else:
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url,title,source,date,wenhao)
        print(templist)
        return templist
    def get_guangdong_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_guangdong_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')
    def get_guangdong_standards(self,url):#法规标准
        list_to_excel(self.template(url,'法规标准'),self.classname+'法规标准')

class guangxi:
    classname = '广西-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('#morelist > ul > li > a')
        titles = [i.get('title') for i in title_href]
        href = [check_back(url,i.get('href')) for i in title_href]
        dates = soup.select('#morelist > ul > li')
        dates = [i.get_text()[-12:][1:-1] for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            print(inner_url)
            source = inner_soup.select('div.article-inf-left')
            if not len(source):
                source = inner_soup.select('div.people-desc > table > tbody > tr:nth-child(1) > td:nth-child(1)')
                if len(source):
                    source = [i.get_text() for i in source][0][5:]
                else:
                    source = None
            else:
                source = re.search('来源：[\s]*[\u4e00-\u9fa5]+',[i.get_text() for i in source][0])
                if source!=None:
                    source = source.group(0)[3:].strip()
                else:
                    source = None

            wenhao = inner_soup.select('div.people-desc > table > tbody > tr:nth-child(3) > td:nth-child(1) > strong')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0][5:]
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_guangxi_local_standards(self,url):#地方生态环境标准
        list_to_excel(self.template(url,'地方生态环境标准'),self.classname+'地方生态环境标准')
    def get_guangxi_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')

class hainan:
    classname = '海南-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.tab-li-t > div.tab-li-t-m > a')
        if not len(title_href):
            title_href = soup.select('div.list-right_title > a')
        dates = soup.select('div.tab-li-x > span:nth-child(3)')
        if not len(dates):
            dates = soup.select('div.list-right_title > span.time_gailan')
        dates = [re.search('\d{4}-\d{1,2}-\d{1,2}',i.get_text()).group(0) for i in dates]
        wenhaos = soup.select('div.tab-li-x > span:nth-child(2)')
        if not len(wenhaos):
            wenhaos = [None for i in title_href]
        else:
            wenhaos = [i.get_text()[3:] for i in wenhaos]
        href = [check_back(url,i.get('href')) for i in title_href]
        titles = [i.get('title') for i in title_href]
        templist = []
        for inner_url,title,date,wenhao in zip(href,titles,dates,wenhaos):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('#fwjg')
            if not len(source):
                source = inner_soup.select('#ly')
            if len(source):
                source = [i.get_text() for i in source][0]
            else:
                source = None
            if wenhao==None:
                wenhao = inner_soup.select('tr:nth-child(4) > td > table > tr > td:nth-child(1) > span:nth-child(2)')
                if len(wenhao):
                    wenhao = [i.get_text() for i in wenhao][0]
                    if wenhao == '无':
                        wenhao = None
            if wenhao == []:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_hainan_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_hainan_proclamation(self,url):#公告
        list_to_excel(self.template(url,'公告'),self.classname+'公告')
    def get_hainan_notice(self, url):  # 通知
        list_to_excel(self.template(url, '通知'), self.classname + '通知')

class chongqing:
    classname = '重庆-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.content.centerWidth > div.right > ul > li > a')
        dates = soup.select('div.content.centerWidth > div.right > ul > li > span')
        href = [check_back(url, i.get('href')) for i in title_href]
        titles = [i.get('title') for i in title_href]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('div.zwxl-title > div.zwxl-bar > script')
            if len(source):
                source = re.search('<span class="tit">来源：</span><span class="con">[\u4e00-\u9fa5、]+</span>',source[0].get_text())[0][46:-7]
            else:
                source = inner_soup.select('div.main.centerWidth > div > table > tbody > tr:nth-child(3) > td.t2')
                if len(source):
                    source = [i.get_text() for i in source][0]
                else:
                    source = None
            date = [i.get_text() for i in date][0]
            wenhao = inner_soup.select('div.main.centerWidth > div > table > tbody > tr:nth-child(1) > td:nth-child(4)')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao.strip() == '':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url,title,source,date,wenhao,attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_chongqing_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')

class guizhou:
    classname = '贵州-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.PageMainBox.aBox > ul > li > a')
        if len(title_href):
            dates = soup.select('div.PageMainBox.aBox > ul > li > span')
            href = [i.get('href') for i in title_href]
            titles = [i.get('title') for i in title_href]
        else:#https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/
            soup = selenium_get_soup(url)
            title_href = soup.select('tbody#Result > tr > td > a')
            href = [i.get('href') for i in title_href]
            titles = [i.get('title') for i in title_href]
            dates = soup.select('tbody#Result > tr > td:nth-child(3)')
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('#PUBLISHDEPT')#https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/202401/t20240131_83657830.html
            split_num = 0
            if not len(source):#https://sthj.guizhou.gov.cn/zwgk/zcwj/tjwj/202310/t20231009_82714679.html
                source = inner_soup.select('div.info_detail > table > tbody > tr:nth-child(2) > td:nth-child(2)')
                if len(source):
                    if source[0].get_text().strip()!='':
                        pass
                    else:
                        source = []
            if not len(source):#https://sthj.guizhou.gov.cn/zwgk/zdlyxx/fgybz/flfgjbz/202206/t20220629_76925493.html
                source = inner_soup.select('div.ArticleProperties > div.f_l > span:nth-child(2)')
                split_num = 3
            if len(source):
                source = [i.get_text() for i in source][0][split_num:]
            else:
                source = None
            date = [i.get_text() for i in date][0]
            wenhao = inner_soup.select('#fileNum')#https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/202401/t20240131_83657830.html
            if not len(wenhao):#https://sthj.guizhou.gov.cn/zwgk/zcwj/tjwj/202310/t20231009_82714679.html
                wenhao = inner_soup.select('div.info_detail > table > tbody > tr:nth-child(3) > td:nth-child(2)')
                if len(wenhao):
                    if wenhao[0].get_text().strip()!='':
                        pass
                    else:
                        wenhao = []
            if len(wenhao) and wenhao!='':
                wenhao = [i.get_text() for i in wenhao][0]
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_guizhou_normative_documents(self, url):  # 规范性文件库
        list_to_excel(self.template(url, '规范性文件库'), self.classname + '规范性文件库')
    def get_guizhou_departmental_documents(self,url):#厅局文件
        list_to_excel(self.template(url,'厅局文件'),self.classname+'厅局文件')
    def get_guizhou_law_standards(self,url):#法规及标准
        list_to_excel(self.template(url,'法规及标准'),self.classname+'法规及标准')
class yunnan:
    classname = '云南-'
    def get_main_url(self,url):
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        match_main = re.search(pattern_main, url)[0]
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        return match_main[:-1]+matches_path[0]
    def get_true_url(self,url):
        soup = get_soup(url)
        true_url = soup.select('[name=myFrameName]')
        true_url = [i.get('src') for i in true_url][0]
        return self.get_main_url(url)+'/'+true_url
    def template(self,url,attr):
        soup = get_soup(self.get_true_url(url))
        title_href = soup.select('div.content > div.txt > div.list > div.item > a')
        titles = [i.get_text() for i in title_href]
        # suoyinhao = soup.select('div.content > div.txt > div.list > div.item > div:nth-child(1)')#索引号，需要删除
        dates = soup.select('div.content > div.txt > div.list > div.item > div')
        dates = [i.get_text() for i in dates if re.search('\d{4}-\d{2}-\d{2}',i.get_text()) != None]
        href = [check_back(self.get_main_url(url), i.get('href')) for i in title_href]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            # title = inner_soup.select('div.main > div > div.title')
            # if not len(title):
            #     title = inner_soup.select('#Body_lb_newsTitle')
            # if len(title):
            #     title = []
            source = inner_soup.select('div.msg-2 > div:nth-child(3) > div:nth-child(1)')#https://sthjt.yn.gov.cn/xxgk/read.aspx?id=237193
            split_num = 4
            if not len(source):#https://hrss.yn.gov.cn/html/2023/7/20/56700.html
                source = inner_soup.select('#Body_lb_NewsOrigin')
                split_num = 0
            if len(source):
                source = [i.get_text() for i in source][0][split_num:]
            else:
                source = None
            wenhao = None#文号出现不规律
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, 1)
        print(templist)
        return templist
    def get_yunnan_publicity(self,url):#信息公开
        list_to_excel(self.template(url,'信息公开'),self.classname+'信息公开')

class shan_xi:#陕西
    classname = '陕西-'
    def get_main_url(self,url):
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        match_main = re.search(pattern_main, url)[0]
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        return match_main[:-1]
    def get_true_url(self,url):
        soup = get_soup(url)
        true_url = soup.select('div.ny_nry > div > iframe')
        if not len(true_url):
            true_url = soup.select('div.daxmlist > div > iframe')
        true_url = [i.get('src') for i in true_url][0]
        return self.get_main_url(url)+'/'+true_url
    def template(self, url, attr):
        soup = get_soup(self.get_true_url(url))
        title_href = soup.select('div.sdxmnr22 > ul > li > a')
        titles = [i.get('title') for i in title_href]
        href = [check_back(self.get_main_url(url)+'/', i.get('href')) for i in title_href]
        dates = soup.select('div.sdxmnr22 > ul > li > a > span')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('div.pages_datetou > p')
            if len(source):
                source = [i.get_text() for i in source][0]
                source = re.search('来源：([^\s]+)', source)[0][3:]
            else:
                source = None
            wenhao = inner_soup.select('div.shfbiaoti')
            if len(wenhao):
                wenhao = [i.get_text().strip() for i in wenhao][-1]
                if wenhao!='':
                    wenhao = re.search('[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)', wenhao)
                else:
                    wenhao = None
                if wenhao != None:
                    wenhao = wenhao.group(0)
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_shan_xi_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')
    def get_shan_xi_standards(self,url):#法规标准
        list_to_excel(self.template(url,'法规标准'),self.classname+'法规标准')

class ningxia:
    classname = '宁夏-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.scroll_main.ScrollStyle > div.zfxxgk_zdgkc > ul > li > a')
        if not len(title_href):
            title_href = soup.select('#dataListSearch > tr > td.text-left > a')
        titles = [i.get('title') for i in title_href]
        href = [check_back(url,i.get('href')) for i in title_href]
        dates = soup.select('div.scroll_main.ScrollStyle > div.zfxxgk_zdgkc > ul > li > b')
        if not len(dates):
            dates = soup.select('#dataListSearch > tr > td:nth-child(3)')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('span.article.text-news-tip.font-weight')
            if not len(source):#https://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/202310/t20231027_1044116.html 中华人民共和国生态环境部
                source = inner_soup.select('body > div.xxgk-main2-bg.xxgk_xqCenter > div:nth-child(1) > div > div > ul > li:nth-child(3) > div:nth-child(1) > i')
                if len(source):
                    if source[0].get_text()=='生态环境部':
                        source = '中华人民共和国生态环境部'
            if len(source):
                if not isinstance(source, str):
                    source = [i.get_text() for i in source][0]
            else:
                source = None
            #把所有居中标题爬取后筛出文号
            wenhao = inner_soup.select('#textcon > div > p[style*="text-align: center"]')#https://sthjt.nx.gov.cn/zfxxgk/fdzdgknr/lzyj/gfxwj1/202312/t20231229_4401126.html
            if len(wenhao):
                temp_wenhao = ''
                for i in wenhao:#拼接标题与副标题
                    temp_wenhao += i.get_text().replace(' ', '') + '\n'#换行符将文号与其他标题隔开避免正则匹配失败
                wenhao = re.search('[\u4E00-\u9fA5]{2,}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)', temp_wenhao)
                if wenhao != None:
                    wenhao = wenhao.group(0)
                else:
                    wenhao = []

            if not len(wenhao):#中华人民共和国生态环境部
                wenhao = inner_soup.select('body > div.xxgk-main2-bg.xxgk_xqCenter > div:nth-child(1) > div > div > ul > li.last > div:nth-child(1)')#本省文号不规律，且掺杂中华人民共和国生态环境部文件
            if len(wenhao):
                if isinstance(wenhao,list):
                    wenhao = [i.get_text() for i in wenhao][0][4:]
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_ningxia_publicity(self,url):#法定公开内容
        list_to_excel(self.template(url,'法定公开内容'),self.classname+'法定公开内容')
    def get_ningxia_announcement(self,url):#公示公告
        list_to_excel(self.template(url,'公示公告'),self.classname+'公示公告')
    def get_ningxia_standards(self,url):#标准规范
        list_to_excel(self.template(url,'标准规范'),self.classname+'标准规范')

class gansu:
    classname = '甘肃-'
    def special_soup(self,url):
        headers = {
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'host' : 'sthj.gansu.gov.cn',
            'cookie' : '4hP44ZykCTt5O=60jESMxspKrEJQjCJbTSFh720GUoEBFYWd8K6YX0AmfF86MgELaYalbYhq1k_1YQZvgD13qCB4r3C6MGACs18lca; yfx_c_g_u_id_10000005=_ck24031618390710405597585767149; sl-session=ubXPO0nI9mUDWr8S9n/hLg==; arialoadData=true; ariawapChangeViewPort=true; JSESSIONID=453F76F1C5A89B159A4944D14AF8BC08; yfx_f_l_v_t_10000005=f_t_1710585547043__r_t_1710643070335__v_t_1710647657611__r_c_1; 4hP44ZykCTt5P=0C4XOO08WP4dc2ecZQ5jo48.LsvVF.NgsUBq3Ure2StB42QdBWFkqXAyvyurQZOVL3uEavK_VXLs8hbNaEgnnh5HkS_sizpZ3Hz4mXBw.hIeH6oHODdIVnoy26MXo_tWE.opvw3zYr_2.AueiBYIcqCRXHAJrXYMrYjdtvgDAx8GZTWLVFy6HB81VNgAGBoGSBoP6e2jWc8l3kkHJcAmxok1ID26SIwQCqJHS8ypYthvMwg7E5vFFV5Eje8Wh8uAHspdBhjgA_2GDOMNXfNBNgTN5e2SkLIYfAp4IMvX8BxCQ_u__sS2PBq5k6.Ou2wJRval3WUfyf5xIa_1Sywxq.kvRmAG1UXx6lb.FrMAcgkW'
        }
        try:
            source = requests.get(url, headers=headers, timeout=10)
        except:
            return "获取信息超时！"
        source.encoding = source.apparent_encoding
        # data = source.json()
        soup = BeautifulSoup(source.text, 'html.parser')
        return soup
    # def get_channel_id(self,url):#爬取难度大，暂时放弃
    #     temp_soup = selenium_get_soup(url)
    #     channel_id = temp_soup.select('meta[name=channelId]')
    #     channel_id = [i.get('content') for i in channel_id][0]
    #     return channel_id
    def template(self,url,attr):
        soup = self.special_soup(url)
        #'https://sthj.gansu.gov.cn/common/search/721e95722dae4733ba77670c40d342bd'
        # print(soup)
        # print(self.get_channel_id(url))
    def get_gansu_normative_documents(self,url):#规范性文件
        list_to_excel(self.template(url,'规范性文件'),self.classname+'规范性文件')

# test = gansu().template('https://sthj.gansu.gov.cn/sthj/c113065/xxgk_list.shtml','111')

class xinjiang:
    classname = '新疆-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('#list-data > ul > li > a')
        if not len(title_href):
            title_href = soup.select('div.list > div > div.name.ellipsis.pull-left > a')
        titles = [i.get_text() for i in title_href]
        href = [check_back(url, i.get('href')) for i in title_href]
        dates = soup.select('#list-data > ul > li > span:nth-child(2)')
        if not len(dates):
            dates = soup.select('div.list > div > div.time.pull-right')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url, title, date in zip(href, titles, dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('div.listtopbox > ul > li:nth-child(2) > div:nth-child(2) > span')#http://sthjt.xinjiang.gov.cn/xjepd/hjyxpjsl/202403/b43e1364d2ed40cba356ad8a173f2ea1.shtml
            split_num = 0
            if len(source):
                if source[0].get_text().strip()=='':
                    source = []
            if not len(source):#http://www.xjbt.gov.cn/c/2024-03-05/8326352.shtml
                source = inner_soup.select('#detail > div.detail-tit.text-center > div.title_info.text-center > span:nth-child(2)')
                split_num = 5
            if len(source):
                source = [i.get_text() for i in source][0][split_num:]
            else:
                source = None

            wenhao = inner_soup.select('div.listtopbox > ul > li:nth-child(3) > div:nth-child(1) > span')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao=='〔〕号':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_xinjiang_notice(self, url):  # 通知
        list_to_excel(self.template(url, '通知'), self.classname + '通知')
    def get_xinjiang_proclamation(self,url):#公示
        list_to_excel(self.template(url,'公示'),self.classname+'公示')
    def get_xinjiang_publicity(self,url):#重点公开
        list_to_excel(self.template(url,'重点公开'),self.classname+'重点公开')

class shengtaihuanjingbu:
    classname = '生态环境部-'
    def get_true_url(self,url,type):#规章和行政规范性文件都要从https://www.mee.gov.cn/xxgk2018/获取
        soup = get_soup(url)
        temp_url = './temptemp'
        if type==1:#1是规章
            temp_url = soup.select('#left > div.xxgkLDropdown_zc > a.xxgkLBtnLi_gz')
        if type==2:#2是行政规范文件
            temp_url = soup.select('#left > div.xxgkLDropdown_zc > a.xxgkLBtnLi_wj')
        if type==0:#0是政策文件和标准，不用处理
            return url
        temp_url = [i.get('href') for i in temp_url][0]
        true_url = check_back(url,temp_url)
        return true_url
    def template(self, url, attr,type):#1是规章2是行政规范文件0是其他
        url = self.get_true_url(url,type)
        soup = get_soup(url)
        title_href = soup.select('body > div.cjcs_dqwz_wai > div > div.cjcs_kong > div.outBox.zcwj > div.bd > div > div > div > ul > li > a')#https://www.mee.gov.cn/zcwj/
        if not len(title_href):#https://www.mee.gov.cn/xxgk2018/
            title_href = soup.select('body > div > div.gz_list > ul > li > div.title > a')
        if not len(title_href):#https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/
            title_href = soup.select('#div > li > a')
        if not len(title_href):#https://www.mee.gov.cn/xxgk2018/xxgk/xzgfxwj/行政规范性文件
            title_href = soup.select('div > div > table > tr > td:nth-child(2) > a')

        dates = soup.select('body > div.cjcs_dqwz_wai > div > div.cjcs_kong > div.outBox.zcwj > div.bd > div > div > div > ul > li > span.date')#https://www.mee.gov.cn/zcwj/
        if not len(dates):#https://www.mee.gov.cn/xxgk2018/
            dates = soup.select('div.gz_list > ul > li > div.title > p')
        if not len(dates):#https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/
            dates = soup.select('#div > li > span')
        if not len(dates):#https://www.mee.gov.cn/xxgk2018/xxgk/xzgfxwj/
            dates = soup.select('table > tr > td.td-date > span')
        href = [check_back(url, i.get('href')) for i in title_href]
        templist = []
        for inner_url, date in zip(href,dates):
            inner_soup = get_soup(inner_url)

            title = inner_soup.select('#print_html > div > h1.cjcs_phone_title')
            if not len(title):
                title = inner_soup.select('div.content_top_box > ul > li.first > div > p')
            if not len(title):#https://www.mee.gov.cn/gzk/gz/202310/t20231020_1043695.shtml
                title = inner_soup.select('div.gz_content > h1')
            if len(title):
                title = [i.get_text() for i in title][0].replace('\u2002','')
                if title.strip()=='':
                    title = None
            else:
                title = None

            source = inner_soup.select('div.content_top_box > ul > li:nth-child(3) > div:nth-child(1) > i')
            split_num = 0
            if not len(source):
                source = inner_soup.select('div.wjkFontBox > em:nth-child(2)')
                split_num = 3
            if not len(source):#https://www.mee.gov.cn/xxgk2018/xxgk/xxgk02/202212/t20221230_1009167.html
                source = inner_soup.select('div.content_top_box > ul > li:nth-child(3) > div:nth-child(1) > div')
                split_num = 0
            if not len(source):#https://www.mee.gov.cn/gzk/gz/202212/t20221230_1009192.shtml
                source = inner_soup.select('div.gz_footer')
                split_num = 0
            if len(source):
                source = [i.get_text() for i in source][0][split_num:].replace('\n','').replace(' ','')
                if source.strip() == '':
                    source = None
                if source[-2:]=='发布':
                    source = source[:-2]
            else:
                source = None

            date = date.get_text()
            temp_date = re.search('(\d{4}年\d{1,2}月\d{1,2}日)',date)#https://www.mee.gov.cn/gzk/gz/
            if temp_date != None:
                date = temp_date.group(0).replace('年','-').replace('月','-').replace('日','')

            wenhao = inner_soup.select('div.content_top_box > ul > li.last > div:nth-child(1)')#文号不规律
            split_num = 4
            #https://www.mee.gov.cn/zcwj/gwywj/202401/t20240122_1064384.shtml
            #https://www.mee.gov.cn/zcwj/gwywj/202402/t20240220_1066422.shtml
            #https://www.mee.gov.cn/zcwj/gwywj/202401/t20240105_1061368.shtml
            if not len(wenhao):
                wenhao = inner_soup.select('div.gz_content > h3')#https://www.mee.gov.cn/gzk/gz/202310/t20231020_1043695.shtml
                split_num = 0

            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0][split_num:].replace(' ','')
                if split_num==0:#2023年10月19日生态环境部、市场监管总局令第31号公布，自公布之日起施行https://www.mee.gov.cn/gzk/gz/202310/t20231020_1043695.shtml
                    wenhao = re.search('（\d{4}年\d{1,2}月\d{1,2}日[\u4e00-\u9fa50-9、]*公布',wenhao)
                    if wenhao!=None:
                        wenhao = re.sub('（\d{4}年\d{1,2}月\d{1,2}日','',wenhao.group(0))[:-2]
                    else:
                        wenhao = ''
                if wenhao.strip() == '':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_shengtaihuanjingbu_policy(self,url):#政策文件
        list_to_excel(self.template(url,'政策文件',0),self.classname+'政策文件')
    def get_shengtaihuanjingbu_law(self,url):#规章
        list_to_excel(self.template(url,'规章',1),self.classname+'规章')
    def get_shengtaihuanjingbu_administrative_normative_documents(self,url):#行政规范文件
        list_to_excel(self.template(url,'行政规范文件',2),self.classname+'行政规范文件')
    def get_shengtaihuanjingbu_ecological_environment_standards(self,url):#生态环境标准
        list_to_excel(self.template(url,'生态环境标准',0),self.classname+'生态环境标准')

class zhongguorenminzhengfu:
    classname = '中国人民政府-'
    def get_true_url(self,url):
        temp_t = re.search('&t=[a-zA-Z_]+',url)
        if temp_t != None:
            temp_t = temp_t.group(0)[3:]
        else:#https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=&t=zhengcelibrary_bm&orpro=
            return False
        page = 1#第n页
        num = 40#每页数据条数
        json_url = 'https://sousuo.www.gov.cn/search-gov/data?t={}&sort=score&sortType=1&searchfield=title&p={}&n={}&type=gwyzcwjk'.format(temp_t,page,num)
        return json_url
    def template(self, url, attr):
        json_url = self.get_true_url(url)
        if json_url:
            soup = get_json(json_url)
            soup = soup['searchVO']['listVO']
            href = [i['url'] if i['url'].strip()!='' else None for i in soup]
            titles = [i['title'] if i['title'].strip()!='' else None for i in soup]
            sources = [i['puborg'] if i['puborg'].strip()!='' else None for i in soup]
            dates = [i['pubtimeStr'] if i['pubtimeStr'].strip()!='' else None for i in soup]
            wenhaos = [i['pcode'] if i['pcode'].strip()!='' else None for i in soup]
        else:
            soup = selenium_get_soup(url)
            title_href = soup.select('#xxgkzn_list_tbody_ID > tr > td.info > a')
            href = [check_back(url, i.get('href')) for i in title_href]
            titles = [i.get_text() for i in title_href]
            sources = [None for i in range(len(titles))]
            dates = soup.select('#xxgkzn_list_tbody_ID > tr > td:nth-child(5)')
            dates = [i.get_text().replace('年','-').replace('月','-').replace('日','') for i in dates]
            wenhaos = soup.select('#xxgkzn_list_tbody_ID > tr > td:nth-child(3)')
            wenhaos = [i.get_text() if i.get_text().strip()!='' else None for i in wenhaos]

        templist = []
        for inner_url,title,source,date,wenhao in zip(href,titles,sources,dates,wenhaos):
            inner_soup = get_soup(inner_url)
            if source==None:
                source = inner_soup.select('div.pchide.abstract.mxxgkabstract > p:nth-child(6)')
                if len(source):
                    source = [i.get_text() for i in source][0]
                else:
                    source = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_zhongguorenminzhengfu_policy(self,url):#国务院政策文件库
        list_to_excel(self.template(url,'国务院政策文件库'),self.classname+'国务院政策文件库')
    def get_zhongguorenminzhengfu_publicity(self, url):  #政府信息公开
        list_to_excel(self.template(url, '政府信息公开'), self.classname + '政府信息公开')

class jiaotongyunshubu:
    classname = '交通运输部-'
    def get_true_url(self,url):
        pattern_main = '[a-zA-z]+://[^\s\/]*/'
        match_main = re.search(pattern_main, url)[0][:-1]
        matches_path = ['/' + i for i in re.sub(pattern_main, '', url).split('/') if i != '']
        for i in matches_path[:-1]:#去掉最后一级路径
            match_main += i
        return match_main+'/list.html'
    def template(self,url,attr):
        soup = get_soup(self.get_true_url(url))
        title_href = soup.select('div.viewport > div > ul > li > a')
        href = [check_back(url, i.get('href')) for i in title_href]
        titles = [i.get('title') for i in title_href]
        dates = soup.select('div.viewport > div > ul > li > a > font')
        dates = [i.get_text().replace('年','-').replace('月','-').replace('日','') for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            ###################################
            source = inner_soup.select('div.fl.w100.main_xl_header.hidden-xs > div:nth-child(2) > form > div:nth-child(1) > div > p')#这是机构分类不是来源
            if len(source):
                source = [i.get_text() for i in source][0]
                if source == '无':
                    source = None
            else:
                source = None
            ###################################
            wenhao = inner_soup.select('div.fl.w100.main_xl_header.hidden-xs > div:nth-child(1) > form > div:nth-child(2) > div > p')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0]
                if wenhao=='无':
                    wenhao = None
            else:
                wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_jiaotongyunshubu_publicity(self, url):  #政府信息公开
        list_to_excel(self.template(url, '政府信息公开'), self.classname + '政府信息公开')

class ziranziyuanbu:
    classname = '自然资源部-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.kyy_textR.fr > ul > li > a')
        if not len(title_href):
            soup = get_soup(url+'index_3553.html')#http://f.mnr.gov.cn/
            title_href = soup.select('div.con-table > ul#ul > li.p123 > div.ffbox > a > a')
        href = [check_back(url, i.get('href')) for i in title_href]
        titles = [i.get_text() for i in title_href]
        dates = soup.select('div.kyy_textR.fr > ul > li > span')
        if not len(dates):
            dates = soup.select('#ul > li > a.none_line')
        dates = [re.search('\d{4}-\d{2}-\d{2}',i.get_text().replace('年', '-').replace('月', '-').replace('日', '')).group(0) for i in dates]
        templist = []
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('#country > div.dtl-middle > div.mid-2 > span:nth-child(2)')#http://f.mnr.gov.cn/202403/t20240307_2838977.html
            if not len(source):#http://gi.mnr.gov.cn/202312/t20231212_2813539.html
                source = inner_soup.select('div.site_table > div > div.box > table > tr:nth-child(3) > td:nth-child(4)')
            if len(source):
                source = [i.get_text() for i in source][0].strip()
                if source.strip()=='':
                    source = None
            else:
                source = None

            wenhao = inner_soup.select('#country > div.dtl-middle > div.mid-2 > span:nth-child(1)')#http://f.mnr.gov.cn/202403/t20240307_2838977.html
            if not len(wenhao):
                wenhao = inner_soup.select('div.site_table > div > div.box > table > tr:nth-child(3) > td:nth-child(2)')
            if len(wenhao):
                wenhao = [i.get_text() for i in wenhao][0].replace('\xa0','').strip()
                if wenhao.strip()=='':
                    wenhao = None
            else:
                wenhao = None

            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_ziranziyuanbu_standards(self,url):#标准规范
        list_to_excel(self.template(url,'标准规范'),self.classname+'标准规范')
    def get_ziranziyuanbu_publicity(self,url):#政策法规库
        list_to_excel(self.template(url,'政策法规库'),self.classname+'政策法规库')
    def get_ziranziyuanbu_announcement(self,url):#通知公告
        list_to_excel(self.template(url,'通知公告'),self.classname+'通知公告')

class fazhangaigewei:
    classname = '发展改革委-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.list > ul > li > a')
        dates = soup.select('div.list > ul > li > span')
        href = [check_back(url, i.get('href')) for i in title_href]
        titles = [i.get('title') for i in title_href]
        dates = [i.get_text().replace('/','-') for i in dates]
        templist = []
        # print(href)
        # print(titles)
        # print(dates)
        for inner_url,title,date in zip(href,titles,dates):
            inner_soup = get_soup(inner_url)
            title = title.replace('\u200b','')
            source = inner_soup.select('div.ly.laiyuantext > span')
            if len(source):
                source = [i.get_text() for i in source][0]
            else:
                source = None
            wenhao = inner_soup.select('div[style="text-align: center;"]')
            temp_text = ''
            for i in wenhao:#把文章标题副标题落空拼到一块用正则筛文号
                temp_text += i.get_text().replace(' ','')
            temp_text = re.search('[\u4E00-\u9fA5]{2,5}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)',temp_text)
            if temp_text!=None:
                wenhao = temp_text.group(0)
            else:#尝试从标题中提取
                wenhao = re.search('\d{4}年第\d+号',title)#《全额保障性收购可再生能源电量监管办法》 2024年第15号令
                if wenhao != None:
                    wenhao = wenhao.group(0)+'令'#关于发布《鼓励外商投资产业目录（2022年版）》的令 2022年第52号
                else:
                    wenhao = re.search('[\u4E00-\u9fA5]{2,5}[\[〔﹝［【{（(]\d{4}[〕﹞］\]】}）)]\d+(?:号)',title)
                    if wenhao != None:#关于印发《全国公共信用信息基础目录（2022年版）》和《全国失信惩戒措施基础清单（2022年版）》的通知(发改财金规〔2022〕1917号)
                        wenhao = wenhao.group(0)
                    else:
                        wenhao = None
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, wenhao)
        print(templist)
        return templist
    def get_fazhangaigewei_order(self,url):#发展改革委令
        list_to_excel(self.template(url, '发展改革委令'), self.classname + '发展改革委令')
    def get_fazhangaigewei_normative_documents(self, url):  # 规范性文件
        list_to_excel(self.template(url, '规范性文件'), self.classname + '规范性文件')
    def get_fazhangaigewei_proclamation(self,url):#公告
        list_to_excel(self.template(url,'公告'),self.classname+'公告')
    def get_fazhangaigewei_notice(self, url):  # 通知
        list_to_excel(self.template(url, '通知'), self.classname + '通知')

class beijixing:
    classname = '北极星环保网-'
    def template(self,url,attr):
        soup = get_soup(url)
        title_href = soup.select('div.cc-list-content > ul > li > a')
        href = [check_back(url, i.get('href')) for i in title_href]
        titles = [i.get('title') for i in title_href]
        dates = soup.select('div.cc-list-content > ul > li > span')
        dates = [i.get_text() for i in dates]
        templist = []
        for inner_url, title, date in zip(href, titles, dates):
            inner_soup = get_soup(inner_url)
            source = inner_soup.select('div.cc-headline > div > p > span:nth-child(2)')
            if len(source):
                source = [i.get_text()[3:] for i in source][0]
            else:
                source = None
            wenhao = None#北极星环保网都是转发其他政府文件，文号若需要去相应地区生态环境局爬取
            templist.append([inner_url, title, source, date, wenhao, attr,now_time])
            test_result(inner_url, title, source, date, '')
        print(templist)
        return templist
    def get_beijixing_environmental_policy(self,url):#环保政策
        list_to_excel(self.template(url, '环保政策'), self.classname + '环保政策')
    def get_beijixing_standards(self,url):#标准
        list_to_excel(self.template(url,'标准'),self.classname+'标准')
if __name__ == '__main__':
    pass
    # test = beijixing().template('https://huanbao.bjx.com.cn/bz/','111')
    # test = fazhangaigewei().template('https://www.ndrc.gov.cn/xxgk/zcfb/tz/','111')
    # test = ziranziyuanbu().template('https://www.mnr.gov.cn/gk/tzgg/','111')
    # test = jiaotongyunshubu().template('https://xxgk.mot.gov.cn/2020/jigou/?gk=5','111')
    # test = zhongguorenminzhengfu().template('https://www.gov.cn/zhengce/xxgk/','111')
    # test = shengtaihuanjingbu().template('https://www.mee.gov.cn/ywgz/fgbz/bz/bzfb/','111',0)
    # test = xinjiang().template('http://www.xjbt.gov.cn/xxgk/zdgk/tzgg/','111')
    # test = gansu().template('https://sthj.gansu.gov.cn/sthj/c113065/xxgk_list.shtml','111')
    # test = ningxia().template('https://sthjt.nx.gov.cn/xwzx/gsgg/','111')
    # test = shan_xi().template('https://sthjt.shaanxi.gov.cn/html/hbt/standard/fgbzxq/index.html','111')
    # test = yunnan().template('https://sthjt.yn.gov.cn/xxgk/index.aspx','111')
    # test = guizhou().template('https://sthj.guizhou.gov.cn/zwgk/gzhgfxwjsjk/gfxwjsjk/','111')
    # test = chongqing().template('https://sthjj.cq.gov.cn/zwxx_249/tzgg/','111')
    # test = hainan().template('http://hnsthb.hainan.gov.cn/xxgk/0200/0202/zwgk/zcfg/','111')
    # test = sichuan().template('https://sthjt.sc.gov.cn/sthjt/c23101802/qtwj.shtml','555')
    # test = guangxi().template('http://sthjt.gxzf.gov.cn/zfxxgk/zfxxgkgl/fdzdgknr/zcfg/gfxwj/','111')
    # test = guangdong().template('http://gdee.gd.gov.cn/gkmlpt/index#3155','11')
    # test = henan().template('https://sthjt.henan.gov.cn/xxgk/hbwj/index.html')
    # test = hubei().template('http://sthjt.hubei.gov.cn/fbjd/xxgkml/gysyjs/sthj/hjbz/')
    # test = hunan().template('http://sthjt.hunan.gov.cn/sthjt/xxgk/zcfg/gfxwj/index.html','aaa')
    # test = shandong().template('http://zfc.sdein.gov.cn/gfxwj/xxyxgfxwj/')
    # test = jiangxi().template('http://sthjt.jiangxi.gov.cn/col/col42202/index.html','222')
    # test = fujian().template('http://sthjt.fujian.gov.cn/zwgk/flfg/')
    # test = anhui().template('https://sthjt.ah.gov.cn/public/column/21691?type=4&action=list&nav=3&catId=32709621')
    # test = anhui().get_true_url('https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng')
    # test = anhui().template('https://sthjt.ah.gov.cn/public/column/21691?type=6&action=xinzheng')
    # test = zhejiang().template('http://sthjt.zj.gov.cn/col/col1229564975/index.html')
    # test = jiangsu().template('http://sthjt.jiangsu.gov.cn/col/col83739/index.html','qqq')
    # test = liaoning().get_liaoning_liaohuanhan('https://sthj.ln.gov.cn/sthj/xxgk/zwxxgk/xxgkml/index.shtml')
    # test = heilongjiang().get_true_url('http://sthj.hlj.gov.cn/sthj/c111958/public_zfxxgk.shtml?tab=gkzc')
    # test = heilongjiang().get_heilongjiang_administrative_normative_documents('http://sthj.hlj.gov.cn/sthj/c111958/public_zfxxgk.shtml?tab=gkzc')
    # test = jilin().get_jilin_announcement('http://sthjt.jl.gov.cn/ywdt/tzgg/')
    # test = liaoning().get_liaoning_announcement('https://sthj.ln.gov.cn/sthj/index/tzgg/index.shtml')
    # test = neimenggu().get_neimenggu_local_law('https://sthjt.nmg.gov.cn/xxgk/zfxxgk/fdzdgknr/?gk=3&cid=16280')
    # test = shanxi().get_shanxi_Departmental_normative_documents('http://sthjt.shanxi.gov.cn/zwgk/zcfg/gfxwj_1/dfgfxwj/')
    # test = tianjin().get_tianjin_announcement('https://sthj.tj.gov.cn/ZWXX808/TZGG6419/')
    #test = beijing().template('http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/325924085/index.html')
    # 文本：http://sthjt.shanxi.gov.cn/gzdt/tndt/202310/t20231023_9407970.shtml
    # 预期结果：['/gzdt', '/tndt', '/202310', '/t20231023_9407970.shtml']
