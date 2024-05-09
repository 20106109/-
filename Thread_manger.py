import threading
import time

import csv_manager
from ceshipachong import crawler_dict,crawler_dict_other
from pypinyin import pinyin, Style

def chinese_to_pinyin(text, style=Style.NORMAL):
    return ''.join([y[0] for y in pinyin(text, style=style)])

class Thread_Control(threading.Thread):
    def __init__(self, name, selected=None,mainwindow=None,thread_1=None,thread_2=None):
        threading.Thread.__init__(self)
        self.name = name
        self.selected = selected
        self.mainwindow = mainwindow
        self.stop_singal = 0
        self.singal = threading.Event()
        self.singal.clear()
        self.fun_dict = {'爬虫线程1':lambda :crawler_run(self),'爬虫线程2':lambda :crawler_other_run(self),'指定线程':lambda :selected_crawler_run(self.selected,self.mainwindow),'数据存储':lambda :save_data(thread_1,thread_2,self.mainwindow),None:donothing}
    def run(self):
        self.fun_dict[self.name]()
    def pause(self):
        # print("\n暂停！")
        self.singal.clear()
    def restart(self):
        # print("\n继续！")
        self.singal.set()
    def stop(self):
        # print("\n停止！")
        self.stop_singal = 1

def save_data(thread_1,thread_2,mainwindow):
    while (thread_1.is_alive()):
        pass
    if thread_2:
        while(thread_2.is_alive()):
            pass
    mainwindow.temp_thread_num = 0
    # print("存入数据库!\n")
    csv_manager.start()
    csv_manager.dboperation()
    mainwindow.logtext.append("爬取完毕!")
def selected_crawler_run(name_ch,mainwindow):
    if name_ch:
        name = chinese_to_pinyin(name_ch) + '_crawler'
    else:
        return
    if name_ch=='陕西':
        name = 'shan_xi_crawler'
    # crawler_dict[name]()
    if not mainwindow.temp_thread_num:
        # print('selected_crawler_run线程数：',mainwindow.temp_thread_num)
        if name_ch!='省份':
            # print(name,' ',crawler_dict[name])
            crawler_dict[name]()
            # time.sleep(5)
            # mainwindow.temp_thread_num = 0
        else:
            mainwindow.threads()
    else:
        mainwindow.logtext.append('当前有其他指定爬虫运作！')
def crawler_run(self):
    for name,func in crawler_dict.items():
        if not self.stop_singal:
            self.singal.wait()
        else:
            break
        # print(name,func)
        func()
        # time.sleep(2)
def crawler_other_run(self):
    for name,func in crawler_dict_other.items():
        if not self.stop_singal:
            self.singal.wait()
        else:
            break
        # print(name,func)
        func()
        # time.sleep(2)
def donothing():
    pass
# def test1(self):
#     for i in range(100):
#         self.singal.wait()
#         print(self.name,i,sep=': ',end='\n')
#         time.sleep(1)




