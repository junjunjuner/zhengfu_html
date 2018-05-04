# _*_encoding:UTF-8_*_
# import pymysql
#
# db_host = '172.28.171.12'
# db_user = 'root'
# db_pw = 'qwe!23'
# db_name = 'db'
#
#
# def cre_db(host, user, pw, name):
#     try:
#         # 数据库连接
#         db = pymysql.connect(host, user, pw, charset='utf8')
#         # 创建游标，通过连接与数据通信
#         cursor = db.cursor()
#         # 执行sql语句
#         cursor.execute('show databases')
#         rows = cursor.fetchall()
#         for row in rows:
#             tmp = "%2s" % row
#             # 判断数据库是否存在
#             if name == tmp:
#                 cursor.execute('drop database if exists ' + name)
#                 cursor.execute('create database if not exists ' + name)
#             # 提交到数据库执行
#             db.commit()
#     except pymysql.Error as e:
#         print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
#     finally:
#     # 关闭数据库连接
#         db.close()
#
#
# cre_db(db_host, db_user, db_pw,db_name)
import pymysql
conn=pymysql.connect(host='172.28.171.12',user='root',passwd='qwe!23',db='car_db',use_unicode=True,charset='utf8')
cursor=conn.cursor()
cursor.execute("SELECT * FROM test;")
print(len(cursor.fetchall()))
for r in cursor.fetchall():
    print(r)
#cur.close()
# conn.close()