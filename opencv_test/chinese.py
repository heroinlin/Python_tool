# -*- coding: utf-8 -*-
#import codecs 
#start,end = (0x4E00, 0x9FA5) 
#with codecs.open("chinese.txt", "wb", encoding="utf-8") as f: 
# for codepoint in range(int(start),int(end)): 
#  f.write(unichr(codepoint)) 

import os 
import pygame 
chinese_dir = 'chinese' 
if not os.path.exists(chinese_dir): 
 os.mkdir(chinese_dir) 
 
pygame.init() 
start,end = (0x4E00, 0x9FA5)#汉字编码范围 
#for codepoint in range(int(start),int(end)): 
for codepoint in range(int(start),int(start)+2): 
 word = unichr(codepoint) 
 font = pygame.font.Font("msyh.ttf", 22)#当前目录下要有微软雅黑的字体文件msyh.ttc,或者去c:\Windows\Fonts目录下找 
 rtext = font.render(word, True, (0, 0, 0), (255, 255, 255)) 
 pygame.image.save(rtext, os.path.join(chinese_dir,word+".png")) 