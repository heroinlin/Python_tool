# -*- coding: utf-8 -*-
'''
translate  the  form of images  from  .jpg to .png
'''
import os
import string
from os import listdir,getcwd
from os.path import join
from skimage.io import imread, imsave
'''
将文件夹foldername文件夹下的.jpg图片转为.png格式并保存至foldername1文件夹下
'''
foldername = "/home/heroin/Dataset/labels/"
foldername1 = "/home/heroin/Dataset/labels_png/"
if not os.path.exists(foldername1):
    os.mkdir(foldername1)
os.path.dirname(foldername)
for filename in os.listdir(foldername):
    src_img = imread(foldername+filename)
    picname = string.split(filename,'.')[0]+'.png'
    imsave(foldername1+picname,src_img)
