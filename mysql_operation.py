import pymysql
class dbUtils():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',user='root',password='20106109',database='biyesheji',port=3306,local_infile=1)
        self.cursor = self.conn.cursor()
    def operation_with_result(self,sql,param=None):#需要返回结果的语句
        self.cursor.execute(sql,param)
        res = self.cursor.fetchall()
        return res
    def operation_not_result(self,sql,param=None):#不需要返回结果的语句
        self.cursor.execute(sql,param)
        self.conn.commit()
    def createTable(self):
        # sql = "create table province(`id` int primary key auto_increment,`source_name` varchar(10),`group` int(5))"
        # sql = "create table target_url(`id` int primary key auto_increment,`url_source` varchar(20),`source_attr` varchar(20),`url` varchar(500),`source_id` int(5), `group` int(5))"
        # sql = "create table file_url(`id` int primary key auto_increment,`file_url` varchar(500),`target_id` int(5),`source_id` int(5))"
        # sql = "create table result(`id` int primary key auto_increment,`file_id` int(5),`title` varchar(255),`institution` varchar(500),`publish_date` date,`wenhao` varchar(255),`crawling_time` date)"
        # sql = "create table tools(`id` int primary key auto_increment,`target_id` int(5),`tool_name` varchar(100),`source_id` int(5),`creator` varchar(50),`create_time` date)"
        # sql = "create table users(`id` int primary key auto_increment,`username` varchar(50),`userpwd` varchar(50),`grade` int(5))"
        sql = "create table permission(`id` int primary key auto_increment,`name` varchar(10)," \
              "target_url_create int(1),target_url_read int(1),target_url_update int(1),target_url_delete int(1)," \
              "file_url_create int(1),file_url_read int(1),file_url_update int(1),file_url_delete int(1)," \
              "result_create int(1),result_read int(1),result_update int(1),result_delete int(1)," \
              "tools_create int(1),tools_read int(1),tools_update int(1),tools_delete int(1)," \
              "users_create int(1),users_read int(1),users_update int(1),users_delete int(1)," \
              "permission_create int(1),permission_read int(1),permission_update int(1),permission_delete int(1)" \
              ")"
        self.operation_not_result(sql)
    def insertTable(self,username,userpwd):
        try:
            # sql = f"insert into user values(null,'{username}','{userpwd}')"
            sql = "insert into user values(null,'%s','%s')"
            self.cursor.execute(sql,(username,userpwd))
            self.conn.commit()
            flag = True
        except:
            flag = False
        return flag
    def queryTable(self,colname,table):#简单查询
        # sql = f"select {colname} from {table}"
        sql = "select %s from %s"
        return self.operation_with_result(sql,(colname,table))
    def search_attr(self,source_name):#匹配属性的查询
        # sql = f"select source_attr from target_url join (select source_name,id from province)pro where pro.id=target_url.source_id and pro.source_name='{source_name}'"
        sql = "select source_attr from target_url join (select source_name,id from province)pro where pro.id=target_url.source_id and pro.source_name='%s'"
        return self.operation_with_result(sql,(source_name))
    def query_col_name(self,table):#查询实际存在的数据表的字段名
        # sql = f"select COLUMN_NAME from information_schema.COLUMNS where table_name = '{table}' order by ordinal_position;"
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' order by ordinal_position;"
        return self.operation_with_result(sql,(table))
    def query_concat_table(self,table1,table2,table1_key,table2_key):#拼接两表
        # sql = f"SELECT {table1}.`*`,{table2}.`*` FROM {table1} JOIN {table2} WHERE {table1}.{table1_key}={table2}.{table2_key}"
        sql = f"SELECT %s.`*`,%s.`*` FROM %s JOIN %s WHERE %s.%s=%s.%s"
        return self.operation_with_result(sql,(table1,table2,table1,table2,table1,table1_key,table2,table2_key))
    def gui_search(self,url_source,startdate,enddate,orderby,sortrule,*args):#前端查询功能
        # sql = f"SELECT result.id,result.title,result.institution,result.wenhao,result.publish_date,temp.file_url,temp.url_source,temp.source_attr FROM result JOIN (SELECT file_url.id,file_url.file_url,target_url.url_source,target_url.source_attr,target_url.weight FROM file_url JOIN target_url ON file_url.target_id = target_url.id WHERE target_url.url_source like '%{url_source}%')temp ON temp.id=result.id WHERE result.publish_date BETWEEN '{startdate}' AND '{enddate}' AND (result.title like '%{url_source}%' OR result.institution like '%{url_source}%') ORDER BY {orderby} {sortrule},temp.weight DESC"
        sql = f"SELECT result.id,result.title,result.institution,result.wenhao,result.publish_date,temp.file_url,temp.url_source,temp.source_attr FROM result JOIN (SELECT file_url.id,file_url.file_url,target_url.url_source,target_url.source_attr,target_url.weight FROM file_url JOIN target_url ON file_url.target_id = target_url.id WHERE target_url.url_source like '%%s%')temp ON temp.id=result.id WHERE result.publish_date BETWEEN '%s' AND '%s' AND (result.title like '%%s%' OR result.institution like '%%s%') ORDER BY %s %s,temp.weight DESC"
        return self.operation_with_result(sql,(url_source,startdate,enddate,url_source,url_source,orderby,sortrule))
    def update_data(self,id,colname,data,table_name):#更新数据
        # sql = f"update {table_name} set {colname}='{data}' where id = {id}"
        sql = f"update %s set %s='%s' where id = %s"
        # print(sql)
        self.operation_not_result(sql,(table_name,colname,data,id))
    def check_permission(self,permission,operation,tablename):#检查与读取权限
        sql = f"select {operation} from {tablename} where id = {permission}"
        return self.operation_with_result(sql)
    def set_infile_status(self):# 允许导入csv
        sql = "set global local_infile='ON';"
        self.operation_not_result(sql)
    def load_data(self,databasename,path):
        sql = "load data local infile '{}' into table biyesheji.{} fields terminated by ',' ignore 1 rows".format(path,databasename)
        self.set_infile_status()
        self.operation_not_result(sql)
    def insert_data(self,tablename,collist,values):
        for res in values:
            # print('insert into {} ({}) values ({})'.format(tablename,collist,res))
            # self.cursor.execute('insert into {} ({}) values ({})'.format(tablename,collist,res))
            self.cursor.execute('insert into %s (%s) values (%s)',(tablename, collist, res))
        self.conn.commit()
    def check_account(self,username,userpwd):#检查账户正确性
        # sql = f"select grade from users_info where username='{username}' and userpwd='{userpwd}'"
        sql = "select grade from users_info where username = (%s) and userpwd = (%s)"
        return self.operation_with_result(sql,(username,userpwd))
if __name__=='__main__':
    d = dbUtils()
    # d.createTable()
    # print([i[0] for i in d.query_col_name('permission')])
    # print(d.check_permission(2,'*','permission'))
    # d.load_data('result',r'C:\\Users\\Smith963\\Desktop\\temp\\result.csv')
    # d.load_data('test',r'C:\\Users\\Smith963\\Desktop\\temp\\file_url.csv')
    # d.insertTable("20106109","20106109")
    print(d.queryTable('name','permission'))
    # print(d.query_col_name('target_url'))
    # print(d.queryTable("*","target_url"))
    #target_url
    # print(d.queryTable())