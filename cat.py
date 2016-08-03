import pygame,sys
from pygame.locals import *

pygame.init()
fps=50
fpsTime=pygame.time.Clock()

display_surf=pygame.display.set_mode((600,500))

pygame.display.set_caption('Play wid Cat')
direction='right'
catImg=pygame.image.load('/home/saqib1707/Desktop/My Images/cat.png')
catx=150
caty=350
while True:
	display_surf.fill((128,128,128))
	if direction=='right':
		catx+=5
		if catx>=450:
			direction='up'
	elif direction=='up':
		caty-=5
		if caty<=150:
			direction='left'
	elif direction=='left':
		catx-=5
		if catx<=150:
			direction='down'
	elif direction=='down':
		caty+=5
		if caty>=350:
			direction='right'

	display_surf.blit(catImg,(catx,caty))

	for event in pygame.event.get():
		if event==QUIT:
			pygame.quit()
			sys.exit()
		pygame.display.update()
	fpsTime.tick(fps)