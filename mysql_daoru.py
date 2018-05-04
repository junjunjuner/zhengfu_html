# # -*- coding: utf-8 -*-
# import  xdrlib ,sys
# import xlrd
# def open_excel(file= 'file.xls'):
#     try:
#         data = xlrd.open_workbook(file)
#         return data
#     except Exception as e:
#         print (str(e))
# #根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
# def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
#     data = open_excel(file)
#     table = data.sheets()[by_index]
#     nrows = table.nrows #行数
#     ncols = table.ncols #列数
#     colnames =  table.row_values(colnameindex) #某一行数据
#     list =[]
#     for rownum in range(1,nrows):
#
#          row = table.row_values(rownum)
#          if row:
#              app = {}
#              for i in range(len(colnames)):
#                 app[colnames[i]] = row[i]
#              list.append(app)
#     return list
#
# #根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
# def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
#     data = open_excel(file)
#     table = data.sheet_by_name(by_name)
#     nrows = table.nrows #行数
#     colnames =  table.row_values(colnameindex) #某一行数据
#     list =[]
#     for rownum in range(1,nrows):
#          row = table.row_values(rownum)
#          if row:
#              app = {}
#              for i in range(len(colnames)):
#                 app[colnames[i]] = row[i]
#              list.append(app)
#     return list
#
# def main():
#    tables = excel_table_byindex()
#    for row in tables:
#        print(row)
#
#    tables = excel_table_byname()
#    for row in tables:
#        print(row)
#
# if __name__=="__main__":
#     main()




# # -*- coding: utf8 -*-
# # !/usr/bin/python
# import xlrd
# def excel(fname):
#     bk = xlrd.open_workbook(fname)
#     shxrange = range(bk.nsheets)
#     try:
#         sh = bk.sheet_by_name("历史数据")
#     except:
#         print("no sheet in %s named Sheet1" % fname)
# # 获取行数
#     nrows = sh.nrows
# # 获取列数
#     ncols = sh.ncols
#     print("nrows %d, ncols %d" % (nrows, ncols))
# # 获取第一行第一列数据
#     cell_value = sh.cell_value(0, 2)
#     print(cell_value)
#
# #row_list = []
# # 获取各行数据
#     for i in range(1, nrows):
#         row_data = sh.row_values(i)
#     #row_list.append(row_data)
#         print(row_data)
#         return row_data
# # if __name__ == '__main__':
# #     excel("F://study//xuss.xlsx")
#
# # !/usr/bin/python
# # -*- coding: UTF-8 -*-
# import pymysql
#
#
# def connection(x):
#     # 打开数据库连接
#     db = pymysql.connect(host='172.28.171.12', port=3306, user='260138', passwd='geli*1234', db='mysql')
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     c = int(x[1])
#     e = int(x[0])
#     f = int(x[5])
#     g = int(x[6])
#     print(c, e, f, g, x[2], x[3],x[4])
#     # SQL 插入语句
#     sql = '''INSERT INTO UIC_LOGIN(ID,ACCOUNT_ID, LOGIN_NAME, PASSWORD, PASSWORD_SALT,REGISTER_MODE,STATUS)VALUES(%s,%s,%s,%s,%s,%s,%s)'''%(e,c,x[2],x[3],x[4],f,g)
#
#     try:
#         # 执行sql语句
#         cursor.execute(sql)
#         # 提交到数据库执行
#         db.commit()
#         print('aaa')
#     except:
#         # Rollback in case there is any error
#         db.rollback()
#         print ('aaaa')
#         # 关闭数据库连接
#         db.close()
#
#
#
# if __name__ == '__main__':
#     a = excel("L9GCBF4BXG2CB0617_2018-04-25.xls")
#     # connection(a)



#
# # !/usr/bin/python
# # -*- coding: UTF-8 -*-
# import xlrd
# import pymysql
# #读取EXCEL中内容到数据库中
# wb = xlrd.open_workbook('L9GCBF4BXG2CB0617_2018-04-25.xls')
# sh = wb.sheet_by_index(0)
# dfun=[]
# nrows = sh.nrows  #行数
# ncols = sh.ncols  #列数
# fo=[]
#
# fo.append(sh.row_values(0))
# for i in range(1,nrows):
#       dfun.append(sh.row_values(i))
# print(len(dfun))
#
# conn=pymysql.connect(host='172.28.171.12',user='root',passwd='qwe!23',db='car_db',use_unicode=True,charset='utf8')
# # create_engine('mysql+mysqldb://USER:@SERVER:PORT/DB?charset=utf8', encoding='utf-8')
# cursor=conn.cursor()
# cursor.execute("drop table if exists test")
# #创建table
# newfo=fo[0][0].replace('-','').replace(':','').replace('：','').replace('(','').replace(')','').replace(';','').replace('+','').replace('/','')
# cursor.execute("create table test("+newfo+" varchar(100));")
# #创建table属性
# for i in range(1,ncols):
#     newfoi = fo[0][i].replace('-','').replace(':','').replace('：','').replace('(','').replace(')','').replace(';','').replace('+','').replace('/','')
#     cursor.execute("alter table test add "+newfoi+" varchar(100);")
# # val=''
# # for i in range(1,nrows):
# #     cursor.executemany("insert into test values(" + dfun[i] + ");")
# #     print("以存:",i)
#     # val = val+'%s,'
# # print(dfun)
#
# # cursor.executemany("insert into test values("+val[:-1]+");" ,dfun)
#
# for d in dfun:
#     cursor.executemany("insert into test values(" + d + ");")
#     print("以存:")
# conn.commit()


















# !/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd
import pymysql
import os
# conn=pymysql.connect(host='172.28.171.12',user='root',passwd='qwe!23',db='car_db',use_unicode=True,charset='utf8')
# cursor=conn.cursor()
# cursor.execute("drop table if exists test")
#
# path1 = '/home/260199/巴士完整'
# pathdir = os.listdir(path1)
# # pathdir.remove('error.txt')
# x=0
# for r in range(len(pathdir)):
#     if x ==0:
#         file = pathdir[r]
#         # 读取EXCEL中内容到数据库中
#         wb = xlrd.open_workbook('/home/260199/巴士完整/'+file)
#         sh = wb.sheet_by_index(0)
#         nrows = sh.nrows  # 行数
#         ncols = sh.ncols  # 列数
#         if ncols <=2:
#             x=0
#             print("此文件为空，表头为空:",file)
#             continue
#         else:
#             fo = []
#             # 创建table
#             fo.append(sh.row_values(0))
#             # 创建table属性
#             name = []
#             for i in range(0, ncols):
#                 newfoi = fo[0][i].replace('-', '').replace(':', '').replace('：', '').replace('(', '').replace(')','').replace(';', '').replace('+', '').replace('/', '')
#                 name.append(newfoi + ' varchar(100)')
#             test_na = ','.join(name)
#             cursor.execute("create table test(" + test_na + " )DEFAULT CHARSET=utf8;")
#             print('表头写入成功:',file)
#             for i in range(1, nrows):
#                 val = []
#                 for j in range(0, ncols):
#                     newfoi = sh.row_values(i)[j]
#                     val.append("'" + newfoi + "'")
#                 dd = ','.join(val)
#                 sql = "insert into test values(" + dd + ");"
#                 # print("sql:%s" % sql)
#                 cursor.execute(sql)
#             conn.commit()
#             print("%s 存入成功"%file)
#             x=1
#     elif x==1:
#         file = pathdir[r]
#         # 读取EXCEL中内容到数据库中
#         wb = xlrd.open_workbook('/home/260199/巴士完整/'+file)
#         sh = wb.sheet_by_index(0)
#         nrows = sh.nrows  # 行数
#         ncols = sh.ncols  # 列数
#         if ncols <=2:
#             print("此文件为空:",file)
#             continue
#         for i in range(1, nrows):
#             val = []
#             for j in range(0, ncols):
#                 newfoi = sh.row_values(i)[j]
#                 val.append("'" + newfoi + "'")
#             dd = ','.join(val)
#             sql = "insert into test values(" + dd + ");"
#             # print("sql:%s" % sql)
#             cursor.execute(sql)
#         conn.commit()
#         print("%s 存入成功"%file)
#
# conn.close()




#读取EXCEL中内容到数据库中
wb = xlrd.open_workbook('L9GCBF4BXG2CB0617_2018-04-25.xls')
sh = wb.sheet_by_index(0)
nrows = sh.nrows  #行数
ncols = sh.ncols  #列数
fo=[]
conn=pymysql.connect(host='172.28.171.12',user='root',passwd='qwe!23',db='car_db',use_unicode=True,charset='utf8')
cursor=conn.cursor()


#创建table
fo.append(sh.row_values(0))
#创建table属性
name = []
for i in range(0,ncols):
    newfoi = fo[0][i].replace('-','').replace(':','').replace('：','').replace('(','').replace(')','').replace(';','').replace('+','').replace('/','')
    name.append(newfoi+' varchar(100)')
test_na = ','.join(name)
cursor.execute("create table car_test("+ test_na+" )DEFAULT CHARSET=utf8;")
for i in range(1, nrows):
    val = []
    for j in range(0,ncols):
        newfoi = sh.row_values(i)[j]
        val.append("'"+newfoi+"'")
    dd = ','.join(val)
    sql = "insert into car_test values("+dd+");"
    print("sql:%s"%sql)
    cursor.execute(sql)
    conn.commit()
    print("存入第%d行 成功。"%i)