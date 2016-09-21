# -*- coding: utf-8 -*-
import os
import pygame
import cv2
from pygame.locals import *
pygame.init()
  
text = u"这是一段测试文本，test 123。"
font = pygame.font.Font('msyh.ttf', 20)#当前目录下要有微软雅黑的字体文件msyh.ttc,或者去c:\Windows\Fonts目录下找
ftext = font.render(text, True, (0, 0, 0), (255, 255, 255))
pygame.image.save(ftext, "t.jpg")
