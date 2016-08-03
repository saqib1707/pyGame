import sys,os
import pygame
from pygame.locals import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((500,200),0,32)
DISPLAYSURF.fill((255,170,20))
pygame.display.set_caption('Hello World!')
pygame.draw.circle(DISPLAYSURF, (0,255,0), (300, 50), 20, 0)
pygame.draw.circle(DISPLAYSURF, (0,0,255), (150, 50), 40, 0)
pygame.draw.line(DISPLAYSURF,(0,0,0),(10,10),(10,10),1)
print pygame.Surface.get_locked(DISPLAYSURF)
pixObj=pygame.PixelArray(DISPLAYSURF)
print pygame.Surface.get_locked(DISPLAYSURF)
pixObj[490,190]=(0,0,0)
pixObj[490,192]=(0,0,0)
pixObj[490,194]=(0,0,0)
pixObj[490,196]=(0,0,0)
pixObj[490,198]=(0,0,0)
del pixObj
pygame.draw.line(DISPLAYSURF,(0,0,0),(10,10),(10,10),1)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
