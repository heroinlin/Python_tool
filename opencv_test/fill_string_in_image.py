# -*- coding: utf-8 -*-
#python font
import os, pygame
from pygame.locals import *
from sys import exit

if not pygame.font: print('Warning, fonts disabled')
pygame.init()
#SCREEN_DEFAULT_SIZE = (500, 500)
BG_IMAGE_NAME = '1.jpg'
FROG_IMAGE_NAME = 't.jpg'
TORK_FONT_NAME = 'msyh.ttf'
bg_image_path = os.path.join('../images', BG_IMAGE_NAME)
frog_image_path = os.path.join('../images', FROG_IMAGE_NAME)
tork_font_path = os.path.join('../images', TORK_FONT_NAME)
if not os.path.exists(bg_image_path):
 print('Can\'t found the background image:', bg_image_path)
if not os.path.exists(frog_image_path):
 print('Can\'t fount the frog image:', frog_image_path)
if not os.path.exists(tork_font_path):
 print('Can\'t fount the font:', tork_font_path)
SCREEN_DEFAULT_SIZE = (500, 500)
screen = pygame.display.set_mode(SCREEN_DEFAULT_SIZE, 0, 32)
bg = pygame.image.load(bg_image_path).convert()
frog = pygame.image.load(frog_image_path).convert_alpha()
tork_font = pygame.font.Font(tork_font_path, 20)

frog_x, frog_y = 0, 0
frog_move_x, frog_move_y = 0, 0
while 1:
 for event in pygame.event.get():
     if event.type == QUIT:
         exit()
     elif event.type == KEYDOWN:
         if event.key == K_LEFT:
             frog_move_x = -1
         elif event.key == K_UP:
             frog_move_y = -1
         elif event.key == K_RIGHT:
             frog_move_x = 1
         elif event.key == K_DOWN:
             frog_move_y = 1
     elif event.type == KEYUP:
         frog_move_x = 0
         frog_move_y = 0
     frog_x += frog_move_x
     frog_y += frog_move_y
 #print(frog_x, frog_y)
 screen.blit(bg, (0, 0))
 position_str = 'Position:' + str(frog_x) + ',' + str(frog_y)
 position = tork_font.render(position_str, True, (255, 255,255), (23, 43,234))
 screen.blit(position, (0, 480))
 screen.blit(frog, (frog_x, frog_y))
 pygame.display.update()
