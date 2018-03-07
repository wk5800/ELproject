import cv2
import numpy as np


def bianjiaofahei(need_deal_path):
    """
    算法3 判断边角发黑 执行边角发黑判断函数
    :param need_deal_path: EL图片路径
    :return:
    """
    path_file = need_deal_path
    grey = cv2.imdecode(np.fromfile(path_file, dtype=np.uint8), 0)  # 灰度
    retval, grey = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY)  # 二值化处理，低于阈值的像素点灰度值置为0黑；高于阈值的值置为255白（参数3）
    # 闭运算：先膨胀后腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    closed = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)
    closed = cv2.dilate(closed, None, iterations=1)  # 膨胀 白色多黑色少
    grey = cv2.erode(closed, None, iterations=1)  # 腐蚀 黑色多白色少

    # 求面积
    width = grey.shape[0]
    height = grey.shape[1]
    area = 0
    for x in range(width):
        for y in range(height):
            if grey[x - 1, y - 1] == 255:
                area += 1
    return area  # 返回EL图片像素面积

if __name__ == '__main__':
    test_path = 'D:/Documents/Desktop/1019145132235_Constract.jpg'
    print(bianjiaofahei(test_path))

