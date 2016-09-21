# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 15:05:21 2016

@author: heroin
"""
#图片椒盐效果
import cv2  
import numpy as np  
  
def salt(img, n):  
    for k in range(n):  
        i = int(np.random.random() * img.shape[1]);  
        j = int(np.random.random() * img.shape[0]);  
        if img.ndim == 2:   
            img[j,i] = 255  
        elif img.ndim == 3:   
            img[j,i,0]= 255  
            img[j,i,1]= 255  
            img[j,i,2]= 255  
    return img  
  
if __name__ == '__main__':  
    img = cv2.imread("../images/cat.jpg")  
    saltImage = salt(img, 500)  
    cv2.imshow("Salt", saltImage)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows() 