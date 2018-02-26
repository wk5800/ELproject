# -*- coding: utf-8 -*-
# file: adjust_light_contrast.py
# author: Wang Kang
# time: 2/26/2018 11:35 AM
# ----------------------------------------------------------------
import cv2
import numpy as np


def light_contrast_coef(picture):
    """
    输入图片的亮度系数、对比度系数.
    :param picture: 输入.
    :return: original_light_coef,original_contrast_coef.
    """
    standard_picture = np.array(picture)
    standard_light_coef = np.mean(standard_picture)  # 亮度，一维
    standard_contrast_coef = np.mean(np.abs(standard_picture - standard_light_coef))  # 对比度，一维
    return standard_light_coef, standard_contrast_coef


def adjust_image_info(picture, standard_light_coef, standard_contrast_coef):
    """
    输入待调图片的地址，调至目标亮度、目标对比度.
    :param picture: 输入待调图片的地址.
    :param standard_light_coef: 目标亮度系数.
    :param standard_contrast_coef: 目标对比度系数.
    :return: over_picture,
    """
    needed_image = cv2.imread(picture)
    needed_image_light_coef = light_contrast_coef(needed_image)[0]
    needed_image_contrast_coef = light_contrast_coef(needed_image)[1]  # 待调图片的亮度信息
    needed_image_contrast = needed_image - needed_image_light_coef  # 待调图片的对比度信息 数组（广播）

    m = standard_light_coef / needed_image_light_coef  # 亮度系数
    n = standard_contrast_coef / needed_image_contrast_coef  # 对比度系数
    over_picture = needed_image_light_coef * m + needed_image_contrast * n  # 修改亮度和对比度
    # new_array_picture = new_array_picture/255

    # 保存到本地注释掉，在batch_deal_el.py中保存到本地，便于批处理
    # cv2.imwrite('D://Documents//Desktop//over_picture.jpg', over_picture)
    return over_picture


if __name__ == '__main__':
    from tools import image_show

    # 图片img的亮度系数、对比度系数
    img = cv2.imread('F://2017//12//ELTD//Renamepath//1019133517922.jpg')
    # standard_light_coef = light_contrast_coef(img)[0]
    # standard_contrast_coef = light_contrast_coef(img)[1]
    # print(standard_light_coef)
    # over_picture = adjust_image_info('D://Documents//Desktop//szy2.jpg', standard_light_coef,standard_contrast_coef)
    # image_show('over picture',over_picture)
