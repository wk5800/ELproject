import cv2
import numpy as np
from tools import image_show


def transform_form(thresh, transform_type):  # 输入图片和模式，输出图片
    if transform_type == 'closing':  # 闭运算：先膨胀再腐蚀
        dilation_kernel = np.ones((4, 4), np.uint8)  # 增加白色区域
        dilation = cv2.dilate(thresh, dilation_kernel, iterations=1)
        erode_kernel = np.ones((10, 10), np.uint8)
        closing_image = cv2.erode(dilation, erode_kernel, iterations=1)  # 腐蚀 增加黑色区域
        return closing_image
    elif transform_type == 'opening':  # 开运算；先腐蚀再膨胀
        erode_kernel = np.ones((5, 5), np.uint8)
        erode = cv2.erode(thresh, erode_kernel, iterations=1)  # 腐蚀 增加黑色区域
        dilation_kernel = np.ones((10, 10), np.uint8)
        opening_image = cv2.dilate(erode, dilation_kernel, iterations=2)
        return opening_image


def madian(path):
    img1 = cv2.imread(path)  # 输入路径
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # 转灰度图
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 61, 3)  # 自适应均值阈值并黑白反转
    th3 = transform_form(th2, 'opening')  # 开操作
    new_image, new_contours, new_hierarchy = cv2.findContours(th3, cv2.RETR_TREE,
                                                              cv2.CHAIN_APPROX_SIMPLE)  # image
    '''
    # print('number',con.max()+1)
    for i in range(len(new_contours)):
        j = new_contours[i]
        area = cv2.contourArea(j)
        if area < 5000 and area > 100:
            x, y, w, h = cv2.boundingRect(j)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    '''
    return new_contours


if __name__ == '__main__':
    path = 'F://2017//12//ELTD//Renamepath2//1019101127101.jpg'
    print(madian(path))
