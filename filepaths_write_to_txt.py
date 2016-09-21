# -*- coding: utf-8 -*-
"""
list files path into txt
"""
import string
import os
import sys
from os import listdir, getcwd
from os.path import join
"""
将self文件夹下的所有filetype格式文件的路径写入到out_file文件中
"""
def filepaths_write_to_txt(self, out_file, filetype=None):
	#print(os.path.dirname(self))
	for filename in os.listdir(self):
		if string.find(filename,filetype or '.')!=-1:
			out_file.write('%s/%s\n'% ( self, filename)) 
			print (filename)

def main():
	foldername = str(sys.argv[1])
	out_file= open(str(sys.argv[2]),'w')
	#foldername = "/home/heroin/Dataset/images"
	#out_file = open('/home/heroin/Dataset/images_list.txt', 'w')
	filepaths_write_to_txt(foldername,out_file,'jpg')

if __name__ == '__main__':
	main()
