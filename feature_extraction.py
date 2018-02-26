# -*- coding: utf-8 -*-
# file: feature_extraction.py
# author: Wang Kang
# time: 12/26/2017 17:23 PM
# ----------------------------------------------------------------
import cv2, pymysql
import numpy as np
# from djangoapp import models
from tools import image_show

all_tz = 'D:/Documents/Desktop/test/5/'  # EL 全特征图存放路径
dytzqt = 'D:/Documents/Desktop/test/6/'  # EL 全单一特征图存放看路径
dytz = 'D:/Documents/Desktop/test/7/'  # EL 子单一特征图存放路径


def Contours_feature(picture):
    """
    输入图片的轮廓特征等信息.
    :param picture: 输入.
    :return: thresh,image,contours,分别为转化后的二值图、转化后的二值图、轮廓.
    """
    imgray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    #  cv2.threshold() 的第二个值的设置很重要

    # 原版本
    ret, thresh = cv2.threshold(imgray, 90, 255,
                                cv2.THRESH_BINARY_INV)  # 第一个参数就是原图像，原图像应该是灰度图。第二个参数就是用来对像素值进行分类的阈值。第三个参数就是当像素值高于（有时是小于）阈值时应该被赋予的新的像素值。

    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return thresh, image, contours


def transform_form(thresh, transform_type):
    """
    二值图形态学转换，以便特征的提取.
    :param thresh: 二值图输入.
    :param transform_type: 形态转换类型.
    :return: thresh,image,contours,分别为转化后的二值图、输入图片、轮廓.
    """
    if transform_type == 'closing':  # 闭运算：先膨胀再腐蚀
        dilation_kernel = np.ones((4, 4), np.uint8)  # 增加白色区域
        dilation = cv2.dilate(thresh, dilation_kernel, iterations=1)
        erode_kernel = np.ones((7, 7), np.uint8)
        closing_image = cv2.erode(dilation, erode_kernel, iterations=1)  # 腐蚀 增加黑色区域
        return closing_image

    elif transform_type == 'opening':  # 开运算：先腐蚀再膨胀
        erode_kernel = np.ones((8, 8), np.uint8)
        erode = cv2.erode(thresh, erode_kernel, iterations=1)  # 腐蚀 增加黑色区域
        dilation_kernel = np.ones((3, 3), np.uint8)
        opening_image = cv2.dilate(erode, dilation_kernel, iterations=2)
        return opening_image


def bounding_show(one_countours, two_countours, original_need_deal_el_path, number_id):
    """
    在原图中画出矩形框且包含轮廓
    :param two_valued_contours: 二值化后的轮廓列表.
    :param original_need_deal_el_path: 输入未作对比度亮度处理的EL的路径.
    :param num: 批处理时处理EL图片张数的计数.
    :return: thresh,image,contours,分别为转化后的二值图、输入图片、轮廓.
    """
    bounding_list = []
    filename = number_id
    # EL 全单一特征图绘制并写到指定目录下
    for i in range(len(one_countours)):
        j = one_countours[i]
        '''
        # 不清楚什么原因：在想要输出单一特征全图时，初始化中间变量middle_adjust_light_contrast_img为EL调整后对比度的图片，
        # 如果直接为其赋值变量adjust_light_contrast_img时，实际上每次循环后并没有重新复制对应的数据。所以为变量赋上路径
        # middle_adjust_light_contrast_img = cv2.imread('D://Documents//Desktop//over_picture.jpg')
        '''
        x, y, w, h = cv2.boundingRect(j)
        area = cv2.contourArea(j)
        if w < 900 and area > 50:
            bounding_list.append((x, y, w, h))
        else:
            continue
    for k in range(len(two_countours)):
        l = two_countours[k]
        area_l = cv2.contourArea(l)
        if area_l < 5000 and area_l > 100:
            x_2, y_2, w_2, h_2 = cv2.boundingRect(l)
            bounding_list.append((x_2, y_2, w_2, h_2))
    bounding_list = sorted(bounding_list, key=lambda x: x[0])  # 对提取的边缘 面积从小到大排序
    for m in range(len(bounding_list)):  # 对每个边缘求出图像
        global original_need_deal_el_img
        feature_bounding_box = bounding_list[m]
        m += 1
        x, y, w, h = feature_bounding_box
        original_need_deal_el_img = cv2.imread(original_need_deal_el_path)
        cv2.rectangle(original_need_deal_el_img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0),
                      2)  # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。

        # 测试完后恢复👇
        cv2.imwrite(dytzqt + '%s_%s_%s.jpg' % (filename, 1, m), original_need_deal_el_img,  # 全单一特征全图写到本地
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # EL 全特征图绘制
    for k in one_countours:
        x, y, w, h = cv2.boundingRect(k)
        area = cv2.contourArea(k)
        if w < 800 and area > 50:  # x,y 后面+10 的目的是为了让矩形框面积变大，最大化包含轮廓信息
            cv2.rectangle(original_need_deal_el_img, (x - 5, y - 5),
                          (x + w + 5, y + h + 5), (0, 255, 0), 2)  # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。
            # cv2.drawContours(original_need_deal_el_img, k, -1, (0, 0, 255), 3)  # 画出故障的轮廓形状
        else:
            continue
    for z in range(len(two_countours)):
        q = two_countours[z]
        area_q = cv2.contourArea(q)
        if area_q < 5000 and area_q > 100:
            x_2, y_2, w_2, h_2 = cv2.boundingRect(q)
            cv2.rectangle(original_need_deal_el_img, (x_2 - 5, y_2 - 5), (x_2 + w_2 + 5, y_2 + h_2 + 5), (0, 255, 0), 2)
            # 测试完后恢复👇
    # cv2.imwrite('F://untitled//media//%s_%s.jpg' % (filename,1),original_need_deal_el_img)
    cv2.imwrite(all_tz + '%s_%s.jpg' % (number_id, 1), original_need_deal_el_img,
                [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 全特征图写到本地
    return original_need_deal_el_img


def save_bounding_picture(one_countours, two_countours, original_need_deal_el_path, number_id, constract_el_path,
                          rectangle_el_path):
    """
    保存轮廓图片到本地
    :param two_valued_contours: 二值化后的轮廓列表.
    :param original_need_deal_el_path: 输入为作对比度亮度处理的EL的路径。
    :param number_id: 批处理时处理EL图片的id.
    """
    bounding_list = []
    original_need_deal_el_img = cv2.imread(original_need_deal_el_path)
    filename = number_id
    for i in one_countours:
        x, y, w, h = cv2.boundingRect(i)
        area = cv2.contourArea(i)
        if w < 900 and area > 50:
            # cv2.rectangle(adjust_light_contrast_img, (x-10, y-10), (x + w + 10, y + h + 10), (0, 255, 0), 1)  # 不注释的话会使之后的img变量表示的图片上都是绿色的线框存在，影响图片原有信息。
            bounding_list.append((x, y, w, h))
        else:
            continue
    for k in range(len(two_countours)):
        l = two_countours[k]
        area = cv2.contourArea(l)
        if area < 5000 and area > 100:
            x_2, y_2, w_2, h_2 = cv2.boundingRect(l)
            bounding_list.append((x_2, y_2, w_2, h_2))
    bounding_list = sorted(bounding_list, key=lambda x: x[0])  # 对提取的边缘 面积从小到大排序
    for j in range(len(bounding_list)):  # 对每个轮廓列表求出图像
        feature_bounding_box = bounding_list[j]
        j += 1
        x, y, w, h = feature_bounding_box  # Grab the coordinates of the letter in the image
        feature_image = original_need_deal_el_img[y - 10:y + h + 10,
                        x - 10:x + w + 10]   # Extract the letter from the original image with a 2-pixel margin around the edge
        # 测试完后恢复👇
        cv2.imwrite(dytz + '%s_%s_%s_s.jpg' % (filename, 1, j), feature_image,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 每个子故障矩形图像保存到本地


        # 读取各个文件夹下的图片地址
        tzqt_el_path = all_tz + '%s_%s.jpg' % (filename, 1)
        dytzqt_el_path = dytzqt + '%s_%s_%s.jpg' % (filename, 1, j)
        dytz_el_path = dytz + '%s_%s_%s_s.jpg' % (filename, 1, j)

        # 往表里写数据
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="test", charset="utf8")
        cur = conn.cursor()
        sql = "INSERT INTO ELimgtest (original_el_path, constract_el_path,rectangle_el_path,dytzqt_el_path,tzqt_el_path,dytz_el_path) VALUES ( '%s', '%s','%s', '%s', '%s','%s')"
        data = (
            original_need_deal_el_path, constract_el_path, rectangle_el_path, dytzqt_el_path, tzqt_el_path,
            dytz_el_path)
        cur.execute(sql % data)
        conn.commit()
        # print('边缘矩形图像已保存到本地')


if __name__ == '__main__':
    from tools import image_show

    over_picture_path = 'F://2017//12//ELTD//Renamepath2//101985314740.jpg'
    # original_image = cv2.imread('D://Documents//Desktop//over_picture.jpg')    # 改变亮度、对比度后的图片image1
    image = cv2.imread('F://2017//test//Rectangle//Rectangle_101985314740.jpg')  # 在image1的基础上增加矩形边缘、白色格栅线的图片image2

    # 图片img的二值图和轮廓等。
    thresh = Contours_feature(image)[0]
    transformed_image = transform_form(thresh, 'closing')
    image_show('transformed_image', transformed_image)  # 展示形态学转换后的二值图
    new_image, new_contours, new_hierarchy = cv2.findContours(transformed_image, cv2.RETR_EXTERNAL,
                                                              cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等提取
    bounding_show(new_contours, over_picture_path, number_id=None)  # 在image1 中展示故障特征

    # save_bounding_picture(new_contours, over_picture_path)  # 根据轮廓，提取故障特征保存在本地
