# import gdkeji
import caizhengbu
# import fagaiwei
# import gdshangwu
# import guowuyuan
# import kejibu
import xlwt
import os

#创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")


if __name__ == '__main__':
    #创建文件夹调用
    file = "/home/260199/政府政策公告信息/超链接"
    mkdir(file)  # 调用函数

    workbook = xlwt.Workbook()
    caizhengbu.main(workbook)
    workbook.save("/home/260199/政府政策公告信息/政府政策公告.xlsx")