#-*- coding: utf-8 -*-
"""
rename each file in folder 
"""
import string
import os
from os import listdir, getcwd
from os.path import join
'''
重命名flodername文件夹下所有图片，0000001_old.jpg   >>  0000001.jpg  ,0000002_old.jpg   >>  0000002.jpg
'''
flodername = "/home/heroin/Dataset/labels"
# flodername1 = "/home/heroin/Dataset/labels_new"
# if not os.path.exists(flodername1):
#     os.mkdir(flodername1)
os.path.dirname(flodername)
for filename in os.listdir(flodername):
    str = string.split(filename, '_')
    newfilename = str[0]+'.'+string.split(str[1], '.')[1]
    os.renames(flodername+'/'+filename, flodername+'/'+newfilename)
