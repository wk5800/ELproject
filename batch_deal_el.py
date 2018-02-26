# -*- coding: utf-8 -*-
# file: whole_step.py
# author: Wang Kang
# time: 02/26/2018 11:37 AM
# whole_step.py的批处理步骤
# ----------------------------------------------------------------
# 批处理多张图片。假设图片存放在'F://2017//12//ELTD//REnamepath'路径下面，则👇👇👇👇👇👇👇👇👇👇👇👇

"""
图片处理流程:
（原图）            10 月-19 日-18 时-59 分-47 秒-952 毫秒.jpg
 (原图重命名)       1019185947953.jpg                 ---->
（调整亮度对比度）	Constract_1019185947953.jpg   	 ---->
（画出边缘轮廓）		Rectangle_1019185947953.jpg  	 ---->
（EL特征全图）		1019185947953_1.jpg              ---->
（EL单一特征全图）	1019185947953_1_1.jpg
（EL单一特征全图）	1019185947953_1_2.jpg	   	     ---->
（EL单一特征）		1019185947953_1_1_s.jpg
（EL单一特征）		1019185947953_1_2_s.jpg
"""

import os, shutil
from adjust_light_contrast import light_contrast_coef, adjust_image_info
from draw_rectangle import draw_rectangle
from feature_extraction import *
import threading
import datetime, madian
import numpy as np


constract_path = 'D:/Documents/Desktop/test/3/'  # EL调整对比度后存放路径
Rectangle_path = 'D:/Documents/Desktop/test/4/'  # EL画出边缘轮廓后存放路径

# 批处理流程写为主方法函数，并引入threading线程模块，对不同路径下的待处理图片作多线程计算。
def main(need_deal_path):
    """
    :param need_deal_path: 重命名后的图片地址
    :return: 提取故障特征后相关图片
    """

    '''
    img = cv2.imread('D://Documents//Desktop//sxdhd.jpg')  # 标准图片
    standard_light_coef = light_contrast_coef(img)[0]  # 标准图片
    standard_contrast_coef = light_contrast_coef(img)[1]
    '''
    standard_light_coef = 50
    standard_contrast_coef = 63
    num = 0
    for i in os.listdir(need_deal_path):
        num += 1
        number_id = i.split('.')[0]
        need_deal_el = os.path.join(need_deal_path, i).replace('\\', '//')
        panduan_image = cv2.imread(need_deal_el)
        xx = np.array(panduan_image)
        if np.mean(xx) > 5:  # 求出原图像素平均灰度（0为黑，255为白），筛选出纯黑图片，不进行后续处理

            # 算法1  提取可能除麻点以外的故障
            over_picture = adjust_image_info(need_deal_el, standard_light_coef, standard_contrast_coef)
            cv2.imwrite(constract_path + '%s_Constract.jpg' % number_id, over_picture,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            print('待处理：%s' % number_id)  # 打印每次处理的图片名
            constract_el_path = constract_path + '%s_Constract.jpg' % number_id

            over_picture_test = cv2.imread(constract_path + '%s_Constract.jpg' % number_id)
            # 对over_picture画边缘白线，排除干扰项。处理后的图片保存到本地 'Rectangle_10100402220_1.jpg'
            add_rectangle_image = draw_rectangle(over_picture_test, panduan_image)
            cv2.imwrite(Rectangle_path + '%s_Rectangle.jpg' % number_id, add_rectangle_image,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            rectangle_el_path = Rectangle_path + '%s_Rectangle.jpg' % number_id

            # 为何直接调用变量add_rectangle_iamge 会报错？重新读路径正常？百思不得其解...
            image = cv2.imread(Rectangle_path + '%s_Rectangle.jpg' % number_id)  # 在image1的基础上增加矩形边缘、白色格栅线的图片image2
            thresh = Contours_feature(image)[0]
            transformed_image = transform_form(thresh, 'closing')
            first_image, first_contours, first_hierarchy = cv2.findContours(transformed_image, cv2.RETR_TREE,
                                                                            cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等提取
            # 算法2 提取麻点故障
            second_contours = madian.madian(need_deal_el)

            over_picture_path = constract_path + '%s_Constract.jpg' % number_id  # 改变亮度、对比度后的图片image1

            # 疑问：是在对比度/亮度处理前的图片上显示故障特征还是在对比度处理后的图片image1上显示故障特征？
            bounding_show(first_contours, second_contours, need_deal_el, number_id)  # 在image1 中展示故障特征
            save_bounding_picture(first_contours, second_contours, need_deal_el, number_id, constract_el_path,
                                  rectangle_el_path)  # 根据轮廓，提取故障特征保存在本地
            # cv2.imwrite('F://2017//12//ELTD//Original//%s' % number_id, panduan_image,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
            new_need_deal_el = need_deal_el.replace(need_deal_el.split('//')[4], 'Original')

            shutil.copyfile(need_deal_el, new_need_deal_el)
            print('%s处理完成!' % number_id)
        else:
            continue


if __name__ == '__main__':

    need_deal_path0 = 'D://Documents//Desktop//test/2'
    need_deal_path1 = 'F://2017//12//ELTD//REnamepath1'
    need_deal_path2 = 'F://2017//12//ELTD//REnamepath2'
    need_deal_path3 = 'F://2017//12//ELTD//REnamepath3'

    starttime = datetime.datetime.now()  # 程序开始时间
    threads = []
    t0 = threading.Thread(target=main, args=(need_deal_path0,))
    threads.append(t0)
    '''
    t1 = threading.Thread(target=main, args=(need_deal_path1,))
    threads.append(t1)
    t2 = threading.Thread(target=main, args=(need_deal_path2,))
    threads.append(t2)
    t3 = threading.Thread(target=main, args=(need_deal_path3,))
    threads.append(t3)
    '''

    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    endtime = datetime.datetime.now() # 程序结束时间
    runtime = (endtime - starttime).seconds
    print('一共运行：%s s' %runtime )
