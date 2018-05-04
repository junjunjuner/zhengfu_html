# !/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd
import pymysql
import os
conn=pymysql.connect(host='172.28.171.12',user='root',passwd='qwe!23',db='car_db',use_unicode=True,charset='utf8')
cursor=conn.cursor()
cursor.execute("drop table if exists car")

path1 = '/home/260199/巴士完整'
pathdir = os.listdir(path1)
# pathdir.remove('error.txt')
x=0
for r in range(len(pathdir)):
    if x ==0:
        file = pathdir[r]
        # 读取EXCEL中内容到数据库中
        wb = xlrd.open_workbook('/home/260199/巴士完整/'+file)
        sh = wb.sheet_by_index(0)
        nrows = sh.nrows  # 行数
        ncols = sh.ncols  # 列数
        if ncols <=2:
            x=0
            print("此文件为空，表头为空:",file)
            continue
        else:
            fo = []
            # 创建table
            fo.append(sh.row_values(0))
            # 创建table属性
            name = []
            for i in range(0, ncols):
                newfoi = fo[0][i].replace('-', '').replace(':', '').replace('：', '').replace('(', '').replace(')','').replace(';', '').replace('+', '').replace('/', '')
                name.append(newfoi + ' varchar(100)')
            test_na = ','.join(name)
            cursor.execute("create table car(" + test_na + " )DEFAULT CHARSET=utf8;")
            print('表头写入成功:',file)
            for i in range(1, nrows):
                val = []
                for j in range(0, ncols):
                    newfoi = sh.row_values(i)[j]
                    val.append("'" + newfoi + "'")
                dd = ','.join(val)
                sql = "insert into car values(" + dd + ");"
                # print("sql:%s" % sql)
                cursor.execute(sql)
            conn.commit()
            print("%s 存入成功"%file)
            x=1
    elif x==1:
        file = pathdir[r]
        # 读取EXCEL中内容到数据库中
        wb = xlrd.open_workbook('/home/260199/巴士完整/'+file)
        sh = wb.sheet_by_index(0)
        nrows = sh.nrows  # 行数
        ncols = sh.ncols  # 列数
        if ncols <=2:
            print("此文件为空:",file)
            continue
        for i in range(1, nrows):
            val = []
            for j in range(0, ncols):
                newfoi = sh.row_values(i)[j]
                val.append("'" + newfoi + "'")
            dd = ','.join(val)
            sql = "insert into car values(" + dd + ");"
            # print("sql:%s" % sql)
            cursor.execute(sql)
        conn.commit()
        print("%s 存入成功"%file)

# #读取EXCEL中内容到数据库中
# wb = xlrd.open_workbook('L9GCBF4BXG2CB0617_2018-04-25.xls')
# sh = wb.sheet_by_index(0)
# nrows = sh.nrows  #行数
# ncols = sh.ncols  #列数
# fo=[]
#
# #创建table
# fo.append(sh.row_values(0))
# #创建table属性
# name = []
# for i in range(0,ncols):
#     newfoi = fo[0][i].replace('-','').replace(':','').replace('：','').replace('(','').replace(')','').replace(';','').replace('+','').replace('/','')
#     name.append(newfoi+' varchar(100)')
# test_na = ','.join(name)
# cursor.execute("create table car("+ test_na+" )DEFAULT CHARSET=utf8;")
# for i in range(1, nrows):
#     val = []
#     for j in range(0,ncols):
#         newfoi = sh.row_values(i)[j]
#         val.append("'"+newfoi+"'")
#     dd = ','.join(val)
#     sql = "insert into car values("+dd+");"
#     print("sql:%s"%sql)
#     cursor.execute(sql)
#     conn.commit()
#     print("存入第%d行 成功。"%i)


