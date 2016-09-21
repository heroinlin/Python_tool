# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 14:32:57 2016

@author: heroin
"""
# 导入OpenCV模块
import sys
import cv2 
if __name__ == '__main__':
 
        # 载入图像，强制转化为Gray
 
        pImg = cv2.imread(sys.argv[1])
        cv2.namedWindow("Image")  
        # 显示图像
        cv2.imshow ("Image", pImg)
        cv2.waitKey(0)