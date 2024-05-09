# -*- coding: utf-8 -*-
import re
import csv
import time

import pandas as pd
import os
from mysql_operation import *
import shutil

db = dbUtils()
def delete_index_col(path):#删掉第一列索引列
    templist = []
    csv_file_r = open(path, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file_r)
    for row in reader:
        templist.append(row[1:])
    csv_file_r.close()

    csv_file_w = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file_w)
    for row in templist:
        writer.writerow(row)
    csv_file_w.close()
def delete_index_row(path):#删掉第一行索引
    templist = []
    status = 0
    csv_file_r = open(path, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file_r)
    for row in reader:
        if status==0:
            status = 1
            continue
        templist.append(row)
    csv_file_r.close()
    csv_file_w = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file_w)
    for row in templist:
        writer.writerow(row)
    csv_file_w.close()

def concat_all_data(data_path,allinfo_path,save_data_path):#合并所有文件
    alldata = pd.DataFrame()
    for dirname in os.listdir(data_path):
        if dirname=='data':
            continue
        data = pd.read_csv(data_path+r'\{}'.format(dirname))
        data['source_name'] = [dirname for i in range(len(data['链接']))]
        alldata = pd.concat([alldata,data])
    alldata.to_csv(allinfo_path)
    delete_index_col(allinfo_path)
    delete_index_col(allinfo_path)
    save_data(data_path, save_data_path)
    clear_data(data_path)

def create_target_url(province_path,target_path,target_url_path):
    try:
        province = pd.read_csv(province_path,encoding='gbk')
    except:
        province = pd.read_csv(province_path, encoding='utf-8')
    try:
        target = pd.read_csv(target_path,encoding='gbk')
    except:
        target = pd.read_csv(target_path, encoding='utf-8')
    province_len = len(province['source_name'])
    target_len = len(target['url_source'])
    temp_source_id = []
    temp_weight = []
    for t_loc in range(target_len):
        for p_loc in range(province_len):
            if province['source_name'][p_loc] in target['url_source'][t_loc]:
                temp_source_id.append(province['id'][p_loc])
                temp_weight.append(round(int(target['group'][t_loc])/int(province['group'][p_loc]),2))#权重计算
    target['source_id'] = temp_source_id
    target['weight'] = temp_weight
    target = target[['id', 'url_source', 'source_attr', 'url','source_id','group','weight']]
    target.to_csv(target_url_path)
    delete_index_col(target_url_path)

def create_file_url(target_url_path,allinfo_path,file_url_path):
    try:
        target_url = pd.read_csv(target_url_path,encoding='gbk')
    except:
        target_url = pd.read_csv(target_url_path, encoding='utf-8')
    try:
        allinfo = pd.read_csv(allinfo_path,encoding='gbk')
    except:
        allinfo = pd.read_csv(allinfo_path, encoding='utf-8')
    target_url_len = len(target_url['url_source'])
    allinfo_len = len(allinfo['source_name'])
    pattern_source = '[\u4e00-\u9fa5]+-'
    pattern_attr = '-[\u4e00-\u9fa5、]+'
    file_url = pd.DataFrame()
    file_count = db.queryTable('count(*)', 'file_url')[0][0]

    for a_loc in range(allinfo_len):
        source_name = re.search(pattern_source, allinfo['source_name'][a_loc]).group(0)[:-1]
        attr = re.search(pattern_attr, allinfo['source_name'][a_loc]).group(0)[1:]

        temp_url = []
        temp_target_id = []
        temp_source_id = []
        temp_file_url = pd.DataFrame()
        for t_loc in range(target_url_len):
            if source_name in target_url['url_source'][t_loc]:
                if attr in target_url['source_attr'][t_loc]:
                    temp_url.append(allinfo['链接'][a_loc])
                    temp_target_id.append(target_url['id'][t_loc])
                    temp_source_id.append(target_url['source_id'][t_loc])
                    break

        temp_file_url['file_url'] = temp_url
        temp_file_url['target_id'] = temp_target_id
        temp_file_url['source_id'] = temp_source_id
        file_url = pd.concat([file_url, temp_file_url])

    file_url['id'] = list(range(file_count + 1, file_count + len(file_url) + 1))
    # file_url['id'] = [i for i in range(1,allinfo_len+1)]
    # file_url['id'] = [i for i in range(1, 1251)]
    file_url = file_url[['id','file_url','target_id','source_id']]
    file_url.set_index('id',drop=True)
    file_url = file_url.rename_axis('index')

    file_url.to_csv(file_url_path)
    delete_index_col(file_url_path)


def create_result(target_url_path,allinfo_path,result_path):
    target_url = pd.read_csv(target_url_path)
    try:
        allinfo = pd.read_csv(allinfo_path,encoding='gbk')
    except:
        allinfo = pd.read_csv(allinfo_path, encoding='utf=8')
    target_url_len = len(target_url['url_source'])
    allinfo_len = len(allinfo['source_name'])
    pattern_source = '[\u4e00-\u9fa5]+-'
    pattern_attr = '-[\u4e00-\u9fa5、]+'
    result = pd.DataFrame()
    result_count = db.queryTable('count(*)', 'result')[0][0]

    for a_loc in range(allinfo_len):
        source_name = re.search(pattern_source, allinfo['source_name'][a_loc]).group(0)[:-1]
        attr = re.search(pattern_attr, allinfo['source_name'][a_loc]).group(0)[1:]

        temp_title = []
        temp_institution = []  # 发文机关
        temp_date = []
        temp_wenhao = []
        temp_file_id = []
        temp_attr = []
        temp_time = []

        temp_result = pd.DataFrame()
        for t_loc in range(target_url_len):
            if source_name in target_url['url_source'][t_loc]:
                if attr in target_url['source_attr'][t_loc]:
                    temp_title.append(allinfo['标题'][a_loc])
                    temp_institution.append(allinfo['发文机关'][a_loc])
                    temp_date.append(allinfo['日期'][a_loc])
                    temp_wenhao.append(allinfo['文号'][a_loc])
                    # temp_file_id.append(a_loc + 1 + result_count)#计算有误，暂时注释
                    temp_attr.append(target_url['source_attr'][t_loc])
                    temp_time.append(allinfo['爬取时间'][a_loc])
                    break

        temp_result['title'] = temp_title
        temp_result['institution'] = temp_institution
        temp_result['publish_date'] = temp_date
        temp_result['wenhao'] = temp_wenhao
        temp_result['attr'] = temp_attr
        # temp_result['file_id'] = temp_file_id
        temp_result['crawling_time'] = temp_time
        result = pd.concat([result, temp_result])

    result['id'] = list(range(result_count + 1, result_count + len(result) + 1))
    result['file_id'] = result['id']
    result = result[['id','file_id','title','institution','publish_date','wenhao','crawling_time']]
    result.set_index('id')

    result.to_csv(result_path)
    delete_index_col(result_path)
def get_path(splitstrnum):#适配mysql和pandas的路径识别
    if splitstrnum==1:
        splitstr = '\\'
    elif splitstrnum==2:
        splitstr = '\\\\'
    root_path = os.getcwd()[:-2]+"all_csv"
    province_path = os.getcwd()[:-2]+"all_csv{}province.csv".format(splitstr)
    target_path = os.getcwd()[:-2]+"all_csv{}target.csv".format(splitstr)
    target_url_path = os.getcwd()[:-2]+"all_csv{}target_url.csv".format(splitstr)
    allinfo_path = os.getcwd()[:-2]+"all_csv{}allinfo.csv".format(splitstr)
    file_url_path = os.getcwd()[:-2]+"all_csv{}file_url.csv".format(splitstr)
    result_path = os.getcwd()[:-2]+"all_csv{}result.csv".format(splitstr)
    data_path = os.getcwd()[:-2]+"all_csv{}data".format(splitstr)
    province_backup_path = os.getcwd()[:-2]+"all_csv{}backup{}province.csv".format(splitstr,splitstr)
    target_backup_path = os.getcwd()[:-2]+"all_csv{}backup{}target.csv".format(splitstr,splitstr)
    save_data_path = os.getcwd()[:-2]+"all_csv{}savedata".format(splitstr,splitstr)
    return province_path,target_url_path,file_url_path,result_path,target_path,allinfo_path,data_path,province_backup_path,target_backup_path,save_data_path,root_path

def start():
    province_path,target_url_path,file_url_path,result_path,target_path,allinfo_path,data_path,province_backup_path,target_backup_path,save_data_path,root_path = get_path(1)
    try:#恢复备份
        province_backup = pd.read_csv(province_backup_path, encoding='gbk')
    except:
        province_backup = pd.read_csv(province_backup_path, encoding='utf-8')
    try:
        target_backup = pd.read_csv(target_backup_path, encoding='gbk')
    except:
        target_backup = pd.read_csv(target_backup_path, encoding='utf-8')
    province_backup.to_csv(province_path)
    delete_index_col(province_path)
    target_backup.to_csv(target_path)
    delete_index_col(target_path)

    concat_all_data(data_path,allinfo_path,save_data_path)
    create_target_url(province_path,target_path,target_url_path)
    create_file_url(target_url_path,allinfo_path,file_url_path)
    create_result(target_url_path,allinfo_path,result_path)

def clear_data(data_path):#清空目录
    shutil.rmtree(data_path)
    os.mkdir(data_path)
def save_data(data_path,save_data_path):#将文件归档
    for dirpath, dirnames, filenames in os.walk(data_path):
        for filename in filenames:
            src = os.path.join(dirpath, filename)
            dst = save_data_path
            shutil.move(src, dst)
def rename(data_path):
    for old_name in os.listdir(data_path):
        os.rename(os.path.join(data_path,old_name),os.path.join(data_path,old_name[:-4]+'-2024-3-20.csv'))
def create_col_dict(sqldict):#创建{表名:字段列表字符串}的字典
    tablelist = sqldict.keys()
    collist = [tuple(j[0] for j in db.query_col_name(i)) for i in tablelist]  # 获取各表字段列表
    for cols in range(len(collist)):  # 拼成字符串
        temp_str = ''
        for col in collist[cols]:
            temp_str += '`' + col + '`,'
            # if col != collist[cols][-1]:
            #     temp_str += ','
        collist[cols] = temp_str[:-1]
    coldict = {table:result for (table,result) in zip(tablelist,collist)}
    return coldict
def get_data_list(tablename,root_path):
    rows = []
    with open(os.path.join(root_path,tablename+'.csv').replace('\\\\','\\'), 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # print(row)
            # 对每一行数据进行处理，例如打印或进行其他操作
            temp_str = ''
            for r in row:
                if r.isdigit():
                    temp_str += r+','
                else:
                    temp_str += "\'" + r + "\',"
                # if r != row[-1]:
                #     temp_str += ','
            rows.append(temp_str[:-1])
    return rows[1:]
def dboperation():#创建表，存入数据
    province_path,target_url_path,file_url_path,result_path,target_path,allinfo_path,data_path,province_backup_path,target_backup_path,save_data_path,root_path = get_path(2)
    tablelist = [province_path,target_url_path,file_url_path,result_path]
    sqldict = {'province':"create table province(`id` int primary key auto_increment,`source_name` varchar(10),`group` int(5))",
        'target_url':"create table target_url(`id` int primary key auto_increment,`url_source` varchar(20),`source_attr` varchar(20),`url` varchar(500), `group` int(5),`source_id` int(5),`group` float(12))",
        'file_url':"create table file_url(`id` int primary key auto_increment,`file_url` varchar(500),`target_id` int(5),`source_id` int(5))",
        'result':"create table result(`id` int primary key auto_increment,`file_id` int(5),`title` varchar(100),`institution` varchar(500),`publish_date` date,`wenhao` varchar(40),`crawling_time` date)",
        'tools':"create table tools(`id` int primary key auto_increment,`target_id` int(5),`tool_name` varchar(100),`source_id` int(5),`creator` varchar(50),`create_time` date)"
        }
    try:
        province_backup = pd.read_csv(province_backup_path,encoding='gbk')
    except:
        province_backup = pd.read_csv(province_backup_path,encoding='utf-8')
    try:
        target_backup = pd.read_csv(target_backup_path,encoding='gbk')
    except:
        target_backup = pd.read_csv(target_backup_path,encoding='utf-8')
    province_backup.to_csv(province_path)#把省份表备份拿出来覆盖被删除行索引的省份表
    delete_index_col(province_path)
    target_backup.to_csv(target_path)#把目标网址表备份拿出来覆盖被删除行索引的目标网址表
    delete_index_col(target_path)
    for i in tablelist:
        try:
            data = pd.read_csv(i,encoding='gbk')
            data.to_csv(i, encoding='utf-8')
            delete_index_col(i)
        except:
            pass
        # delete_index_row(i)
    # for i in sqldict.keys():
    #     db.createTable(sqldict[i])
    # for name,path in zip(list(sqldict.keys()),tablelist):
    #     db.load_data(name,path)

    coldict = create_col_dict(sqldict)
    for t_name in coldict.keys():
        if t_name=='tools' or t_name=='users_info' or t_name== 'test' or t_name=='permission' or t_name=='province' or t_name=='target_url':
            continue
        # if t_name=='province' or t_name=='target_url' or t_name=='tools' or t_name=='users':
        #     continue
        db.insert_data(t_name,coldict[t_name],get_data_list(t_name,root_path))


if __name__ == '__main__':
    start()
    # dboperation()
    # clear_data(r"C:\Users\Smith963\Desktop\temp\savedata")









