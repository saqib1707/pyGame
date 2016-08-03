import pygame,sys
from pygame.locals import *

pygame.init()
fps=50                                           #frames per second to be displayed
fpsTime=pygame.time.Clock()

display_surf=pygame.display.set_mode((600,500))  # Surface Object returned which is my main  window

pygame.display.set_caption('Play wid Cat')
direction='right'                                 #direction in which cat is going to move
catImg=pygame.image.load('/home/saqib1707/Desktop/My Images/cat.png')      #loading the cat img
catx=150
<<<<<<< HEAD
caty=350

fontObj=pygame.font.Font('freesansbold.ttf',32)
textSurfaceObj=fontObj.render('One round completed',False,(0,255,0))
textRectObj=textSurfaceObj.get_rect()
textRectObj.center=(300,250)

=======
caty=350                                          # initial position of cat
>>>>>>> 63c195311dd68f32565f67021ded09f46e016f95
while True:
	display_surf.fill((128,128,128))          #color the background of main window
	if direction=='right':                     # cat moves in a rectangular path
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
<<<<<<< HEAD
	if (catx==150 and caty==350):
		display_surf.blit(textSurfaceObj,textRectObj)
	else:
		display_surf.blit(catImg,(catx,caty))
=======

	display_surf.blit(catImg,(catx,caty))       #blit basically copies the catimg on the main window
>>>>>>> 63c195311dd68f32565f67021ded09f46e016f95

	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
		pygame.display.update()
	fpsTime.tick(fps)                        # this ensures that the speed of the game is not too fast ...not mentioning it
	                                         # will make the game run at the speed of computer
