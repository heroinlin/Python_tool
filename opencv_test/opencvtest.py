# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 15:05:21 2016

@author: heroin
"""


# 图像的载入、显示、复制和保存
import sys
import cv2
import numpy as np
 
if __name__ == '__main__':
 
    # 打开图像
     img = cv2.imread(sys.argv[1])
     cv2.namedWindow("Image")    
     emptyImage = np.zeros(img.shape, np.uint8)  
     emptyImage2 = img.copy()  
     emptyImage3=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
#emptyImage3[...]=0  
     cv2.imshow("EmptyImage", emptyImage)  
     cv2.imshow("Image", img)  
     cv2.imshow("EmptyImage2", emptyImage2)  
     cv2.imshow("EmptyImage3", emptyImage3)  
     cv2.imwrite("../images/cat2.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 5])  
     cv2.imwrite("../images/cat3.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  
     cv2.imwrite("../images/cat1.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])  
     cv2.imwrite("../images/cat2.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])  
     cv2.waitKey (0)  
     cv2.destroyAllWindows()  