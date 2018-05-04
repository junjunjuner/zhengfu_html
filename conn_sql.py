import pymysql
conn = pymysql.connect(host='172.28.171.12',port=3306,user='root',passwd='qwe!23',db='mysql')
cur = conn.cursor()
cur.execute('select version()')
for i in cur:
    print(i)
cur.close()