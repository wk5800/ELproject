# -*- coding: utf-8 -*-
# file: draw_rectangle.py
# author: Wang Kang
# time: 01/18/2018 16:40 PM
# ----------------------------------------------------------------
import cv2
import numpy as np
from tools import image_show
from adjust_light_contrast import *


def morphology(image, threshold):
    """
    形态学转化函数
    :param image:
    :param threshold: 像素阈值
    :return:
    """
    new_contours = []
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
    result = cv2.bitwise_not(thresh)  # 反色，对二值图每个像素取反
    dilation_kernel = np.ones((5, 5), np.uint8)  # 膨胀 增加白色区域
    dilation = cv2.dilate(result, dilation_kernel, iterations=3)
    erode_kernel = np.ones((8, 8), np.uint8)  # 腐蚀 增加黑色区域
    closing_image = cv2.erode(dilation, erode_kernel, iterations=3)
    bitwise_not_closing_image = cv2.bitwise_not(closing_image)
    new_image, contours, hierarchy = cv2.findContours(bitwise_not_closing_image, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等
    # 防止电池片里面的故障特征被误认为格栅，增加面积判断条件。
    for k in range(len(contours)):
        area = cv2.contourArea(contours[k])
        if area > 200:
            new_contours.append(contours[k])
    return new_contours


def outer_morphology(image, threshold):
    """
    形态学转化函数/画出电池片外部轮廓
    :param 未经处理的el原图:
    :param threshold:设为1，即像素值小于1的转化为白255
    :return:外部轮廓contours
    """
    new_contours = []
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, threshold, 255, cv2.THRESH_BINARY)
    dilation_kernel = np.ones((5, 5), np.uint8)  # 膨胀 增加白色区域
    dilation = cv2.dilate(thresh, dilation_kernel, iterations=2)
    erode_kernel = np.ones((1, 1), np.uint8)  # 腐蚀 增加黑色区域
    closing_image = cv2.erode(dilation, erode_kernel, iterations=3)
    new_image, contours, hierarchy = cv2.findContours(closing_image, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)  # image2的二值图经过形态学转化后的轮廓等
    # 防止电池片里面的故障特征被误认为格栅，增加面积判断条件。
    for k in range(len(contours)):
        area = cv2.contourArea(contours[k])
        if area > 50000:
            new_contours.append(contours[k])
    return new_contours


def draw_rectangle(image, original):
    """
    画出EL边缘轮廓及格栅，减少不相关特征对故障特征的干扰
    :param image: 输入为 调整亮度/对比度后的图片（adjust_image_info（））
    :return:添加（白色）边缘的图片

    """
    # 版本三
    bounding_list = []
    threshold = 20  # 初始阈值
    new_contours = morphology(image, threshold)
    while len(new_contours) != 6:  # 电池片按格栅可划分为6个轮廓
        if len(new_contours) > 6:
            threshold -= 1
            new_contours = morphology(image, threshold)
        if len(new_contours) < 6:  # 一般为白色区域多（格栅与区域块未完全分离）
            threshold += 2
            new_contours = morphology(image, threshold)
    outer_contours = outer_morphology(original, 1)  # 找到电池片外部轮廓
    cv2.drawContours(image, outer_contours, -1, (255, 255, 255), 20)  # 画出电池片外部轮廓

    for i in range(len(new_contours)):
        j = new_contours[i]
        x, y, w, h = cv2.boundingRect(j)
        bounding_list.append((x, y, w, h))
    bounding_list = sorted(bounding_list, key=lambda x: x[1])  # 对提取的边缘 从上到下排（依据y的值）

    for k in range(0, 6):
        x, y, w, h = bounding_list[k]
        '''
        if k == 0:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
            if x > bounding_list[3][0]:
                x = bounding_list[3][0]
                cv2.rectangle(image, (x-5, y), (x + w, y + h +15), (255, 255, 255), 28)
            else:
                cv2.rectangle(image, (x-5, y), (x + w, y + h +15), (255, 255, 255), 28)
        '''

        if k == 1:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
            if x > bounding_list[3][0]:
                x = bounding_list[3][0]
                cv2.rectangle(image, (x - 5, y - 18), (x + w, y + h + 10), (255, 255, 255), 25)
            else:
                cv2.rectangle(image, (x - 5, y - 18), (x + w, y + h + 10), (255, 255, 255), 25)
            cv2.line(image, (x, y), (x + w, y), (255, 255, 255), 28)
        elif k == 2:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
            if x > bounding_list[3][0]:
                x = bounding_list[3][0]
                cv2.rectangle(image, (x - 5, y - 15), (x + w, y + h + 10), (255, 255, 255), 20)
            else:
                cv2.rectangle(image, (x - 5, y - 15), (x + w, y + h + 10), (255, 255, 255), 20)

        elif k == 3:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
                cv2.rectangle(image, (x - 5, y - 5), (x + w, y + h + 10), (255, 255, 255), 25)
            else:
                cv2.rectangle(image, (x - 5, y - 5), (x + w, y + h + 10), (255, 255, 255), 25)

        elif k == 4:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
            if x > bounding_list[3][0]:
                x = bounding_list[3][0]
                cv2.rectangle(image, (x - 5, y - 15), (x + w, y + h + 14), (255, 255, 255), 25)
            else:
                cv2.rectangle(image, (x - 5, y - 15), (x + w, y + h + 14), (255, 255, 255), 25)
            cv2.line(image, (x, y + h - 10), (x + w, y + h - 10), (255, 255, 255), 25)
        '''
        elif k == 5:
            if w < bounding_list[3][2]:
                w = bounding_list[3][2]
            if x > bounding_list[3][0]:
                x = bounding_list[3][0]
                cv2.rectangle(image, (x - 5, y - 18), (x + w, y + h ), (255, 255, 255), 25)
            else:
                cv2.rectangle(image, (x - 5, y - 18), (x + w, y + h ), (255, 255, 255), 25)
        '''
    return image


if __name__ == '__main__':
    original = cv2.imread('F://2017//12//ELTD//Renamepath2//101985314740.jpg')
    image = cv2.imread(
        'F://2017//12//ELTD//Constract//Constract_101985314740.jpg')  # 1019162540580  101984931331  # 101912151946   # 1019101128209  # 1019133532883  # 1019101149425   #1019133517922
    add_rectangle_image = draw_rectangle(image, original)
    image_show('add_rectangle_image', add_rectangle_image)
