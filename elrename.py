# -*- coding: utf-8 -*-
# file: renamefile.py
# author: Wang Kang
# time: 12/28/2017 10:14 AM
# ----------------------------------------------------------------

import os, random, shutil, re


def renamefile(path, newname):
    """
    重命名故障特征文件夹里的文件名
    :param path: 各种故障特征文件夹路径
    :param newname: 文件名的新名字
    :return: 重命名后的故障文件路径（）
    """
    i = 0
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        i += 1
        Olddir = os.path.join(path, files)  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]  # 文件名
        filetype = os.path.splitext(files)[1]  # 文件扩展名
        Newdir = os.path.join(path, newname + str(i) + filetype)  # 新的文件路径
        os.rename(Olddir, Newdir)  # 重命名
    print("故障特征重命名结束")
    return Newdir


def copy_el(need_copyel_path, copy_path):
    """
    复制文件到指定路径下
    :param need_copyel_path: EL图片原始路径
    :param copy_path:  复制到指定路径
    :return:
    """
    for i in os.listdir(need_copyel_path):
        file_path = os.path.join(need_copyel_path, i)
        new_file_path = copy_path + '//' + i
        shutil.copyfile(file_path, new_file_path)  # 把图片从"F:\\data\\EL picture\\移动测试"复制到 copy_path 路径下

def renameel(need_renameel_path):
    """
    EL重命名，命名规则为只取数字
    :param need_renameel_path: 待命名的EL图片路径
    :return:
    """
    for j in os.listdir(need_renameel_path):
        file_path = os.path.join(need_renameel_path, j)
        matching = re.compile(r'\d+\s')
        middle_i = matching.findall(j)
        new_i = middle_i[0].strip(' ') + middle_i[1].strip(' ') + middle_i[2].strip(' ') + middle_i[3].strip(' ') + \
                middle_i[4].strip(' ') + middle_i[5].strip(' ') + '.' + j.split('.')[1]
        repath = need_renameel_path +'//' + new_i
        print(new_i)
        os.rename(file_path, repath)

if __name__ == '__main__':
    need_copyel_path = 'D:/Documents/Desktop/test/1'
    copy_path = 'D:/Documents/Desktop/test/2'
    copy_el(need_copyel_path, copy_path)
    renameel(copy_path)
